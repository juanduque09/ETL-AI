import google.generativeai as genai
import fitz  # PyMuPDF
from dotenv import load_dotenv
import os
import pandas as pd
from io import StringIO
from prompt import prompt
import logging
import time
import random
import csv
from datetime import datetime

# Cargar variables de entorno desde el archivo .env
load_dotenv(".env")

# Configurar logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL), 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurar Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "models/gemini-2.0-flash")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL")
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "512"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))

# Configuración de reintentos
LLM_RETRIES = int(os.getenv("LLM_RETRIES", "5"))
BACKOFF_BASE = float(os.getenv("BACKOFF_BASE", "1.0"))
BACKOFF_MAX = float(os.getenv("BACKOFF_MAX", "30.0"))
BACKOFF_JITTER = float(os.getenv("BACKOFF_JITTER", "0.5"))

# Archivo de métricas
LLM_METRICS_CSV = os.getenv("LLM_METRICS_CSV", "llm_usage.csv")

genai.configure(api_key=GOOGLE_API_KEY)

def log_llm_usage(model_name, prompt_tokens, completion_tokens, total_tokens, success=True):
    """Registra métricas de uso del LLM en CSV"""
    try:
        file_exists = os.path.exists(LLM_METRICS_CSV)
        
        with open(LLM_METRICS_CSV, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'model', 'prompt_tokens', 'completion_tokens', 
                         'total_tokens', 'success']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'timestamp': datetime.now().isoformat(),
                'model': model_name,
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': total_tokens,
                'success': success
            })
    except Exception as e:
        logger.warning(f"No se pudo registrar métricas LLM: {e}")

def extraer_texto_pdf(ruta_pdf):
    """Extrae texto de un archivo PDF"""
    try:
        doc = fitz.open(ruta_pdf)
        text = "\n".join([page.get_text("text") for page in doc])
        doc.close()
        logger.debug(f"Texto extraído de {ruta_pdf}: {len(text)} caracteres")
        return text
    except Exception as e:
        logger.error(f"Error extrayendo texto de {ruta_pdf}: {e}")
        raise

def estructurar_texto(texto):
    """Envía el texto a Gemini con reintentos y fallback"""
    
    current_model = MODEL_NAME
    
    for attempt in range(LLM_RETRIES):
        try:
            logger.debug(f"Intento {attempt + 1}/{LLM_RETRIES} con modelo {current_model}")
            
            model = genai.GenerativeModel(
                current_model,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=MAX_OUTPUT_TOKENS,
                    temperature=TEMPERATURE
                )
            )
            
            full_prompt = prompt + "\n Este es el texto a parsear:\n" + texto
            
            respuesta = model.generate_content(full_prompt)
            
            # Intentar extraer métricas de uso si están disponibles
            try:
                usage = respuesta.usage_metadata
                if usage:
                    log_llm_usage(
                        current_model,
                        usage.prompt_token_count,
                        usage.candidates_token_count,
                        usage.total_token_count,
                        True
                    )
            except AttributeError:
                logger.debug("Métricas de uso no disponibles")
            
            csv_respuesta = respuesta.text.strip()
            logger.debug(f"Respuesta obtenida: {len(csv_respuesta)} caracteres")
            
            return csv_respuesta
            
        except Exception as e:
            logger.warning(f"Intento {attempt + 1} falló: {e}")
            
            # Si hay error de sobrecarga y tenemos modelo fallback
            if ("503" in str(e) or "unavailable" in str(e).lower()) and FALLBACK_MODEL and current_model != FALLBACK_MODEL:
                logger.info(f"Cambiando a modelo fallback: {FALLBACK_MODEL}")
                current_model = FALLBACK_MODEL
            
            # Registrar fallo en métricas
            log_llm_usage(current_model, 0, 0, 0, False)
            
            if attempt < LLM_RETRIES - 1:
                # Backoff exponencial con jitter
                delay = min(BACKOFF_BASE * (2 ** attempt), BACKOFF_MAX)
                jitter = random.uniform(0, BACKOFF_JITTER)
                sleep_time = delay + jitter
                
                logger.info(f"Esperando {sleep_time:.1f}s antes del siguiente intento...")
                time.sleep(sleep_time)
            else:
                logger.error(f"Todos los intentos fallaron para estructurar texto")
                return "error"
    
    return "error"

def csv_a_dataframe(csv):
    """Convierte el texto CSV en un DataFrame de pandas, asegurando que 'importe' sea numérico."""
    
    try:
        # Definir los tipos de datos para cada columna
        dtype_cols = {
            "fecha_factura": str,
            "proveedor": str,
            "concepto": str,
            "importe": str,  # Se leerá primero como str para poder limpiar comas
            "moneda": str,
        }

        # Leer el CSV en un DataFrame con los tipos especificados
        df_temp = pd.read_csv(StringIO(csv), delimiter=";", dtype=dtype_cols)

        # Convertir 'importe' a float, asegurando que los valores con coma se conviertan correctamente
        df_temp["importe"] = pd.to_numeric(
            df_temp["importe"].str.replace(",", "."), errors="coerce"
        )
        
        logger.debug(f"DataFrame creado con {len(df_temp)} filas")
        return df_temp
        
    except Exception as e:
        logger.error(f"Error convirtiendo CSV a DataFrame: {e}")
        raise
