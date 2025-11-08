# ETL Facturas (Gemini + COP)
Juanjo te amo
Este mini-proyecto procesa facturas en PDF usando Gemini (Google) para extraer campos en CSV, los convierte a DataFrame, transforma importes a COP y persiste en SQLite.

## Requisitos
- Python 3.10+ (probado con 3.11/3.12)
- Virtualenv o Conda
- Google API Key para Gemini
- Permisos de escritura en la carpeta del proyecto

## Instalación rápida

### Con venv (recomendado)
```bash
# Clonar el repositorio
git clone https://github.com/juanduque09/ETL-AI.git
cd ETL-AI

# Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Con conda (alternativo)
```bash
# Si prefieres usar conda
conda env create -f entorno.yml
conda activate gestor_gastos
```

## Configuración inicial

### 1. Configurar carpeta de facturas
```bash
# Crear carpeta con permisos correctos
mkdir -p facturas
chmod 755 facturas
```

### 2. Configurar variables de entorno
```bash
# Crear archivo .env (no se sube al repositorio por seguridad)
touch .env
```

Edita `.env` con tu configuración:
```bash
# Configuración principal
PROVIDER=gemini
MODEL_NAME=models/gemini-2.0-flash
GOOGLE_API_KEY=tu_api_key_aqui_desde_google_ai_studio

# Conversión de monedas (tasas de referencia)
FALLBACK_RATE_USD_COP=4500
FALLBACK_RATE_EUR_COP=4900

# Configuración avanzada (opcional)
FALLBACK_MODEL=models/gemini-2.5-flash
MAX_OUTPUT_TOKENS=512
TEMPERATURE=0.0
BACKOFF_BASE=1.0
BACKOFF_MAX=30.0
BACKOFF_JITTER=0.5
LOG_LEVEL=INFO
LLM_METRICS_CSV=llm_usage.csv
LLM_RETRIES=5
```

### 3. Obtener Google API Key
1. Ve a [Google AI Studio](https://aistudio.google.com/)
2. Crea un nuevo proyecto o usa uno existente
3. Genera una API Key
4. Cópiala en tu archivo `.env`

## Uso del sistema

### 1. Probar conexión con Gemini
```bash
python3 test_gemini.py
```

### 2. Crear facturas de prueba (opcional)
```bash
# Generar PDFs de ejemplo
python3 setup_demo.py

# Opciones disponibles:
# 1. Facturas fijas (siempre iguales)
# 2. Facturas aleatorias (diferentes cada vez)
# 3. Ambos tipos
```

### 3. Colocar tus facturas reales
```bash
# Opción A: Directamente en ./facturas/
./facturas/mi_factura.pdf
./facturas/otra_factura.pdf

# Opción B: En subcarpetas organizadas
./facturas/enero/factura1.pdf
./facturas/febrero/factura2.pdf
```

### 4. Procesar facturas
```bash
# Procesar todas las facturas y reemplazar tabla
python3 main.py --overwrite

# Procesar y anexar a datos existentes
python3 main.py

# Ver estructura de facturas disponibles
python3 debug_facturas.py
```

### 5. Inspeccionar resultados
```bash
# Consulta rápida en consola
python3 -c "
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('sqlite:///facturas.db')
df = pd.read_sql('facturas', engine)
print('Total facturas procesadas:', len(df))
print('Total en COP:', f'{df[\"importe\"].sum():,.0f}')
print('Rango de fechas:', df['fecha_factura'].min(), 'a', df['fecha_factura'].max())
print('\n Resumen por proveedor:')
print(df.groupby('proveedor')['importe'].sum().sort_values(ascending=False).head())
print('\n Muestra de datos:')
print(df.head())
"

# O usar cualquier herramienta SQLite para explorar facturas.db
```

## Estructura del proyecto
```
ETL-AI/
├── 📁 facturas/              # PDFs (no se suben a Git por seguridad)
│   ├── mi_factura.pdf
│   ├── demo_*.pdf            # Facturas de ejemplo
│   └── random_*.pdf          # Facturas aleatorias
├── 📄 .env                   # Variables de entorno (no se sube a Git)
├── 📄 main.py               # Script principal del ETL
├── 📄 funciones.py          # Funciones core (PDF→CSV→DB)
├── 📄 prompt.py             # Prompt optimizado para Gemini
├── 📄 test_gemini.py        # Tests y validación del sistema
├── 📄 setup_demo.py         # Generador de facturas de prueba
├── 📄 debug_facturas.py     # Debug estructura de facturas
├── 📄 requirements.txt      # Dependencias Python
├── 📄 entorno.yml           # Alternativa con Conda
├── 📄 facturas.db           # Base de datos SQLite (generada)
├── 📄 llm_usage.csv         # Métricas de uso de Gemini
└── 📄 README.md             # Esta documentación
```

## Características principales

**Procesamiento automático**: Extrae texto de PDFs usando PyMuPDF  
**IA integrada**: Usa Gemini para estructurar datos de facturas  
**Conversión de monedas**: USD/EUR → COP automáticamente  
**Reintentos inteligentes**: Backoff exponencial con modelo fallback  
**Métricas y logging**: Auditoría completa del uso de tokens  
**Flexible**: Soporta PDFs directos o en subcarpetas  
**Generador de pruebas**: Crea facturas de demo realistas  

## Seguridad y privacidad

**Datos protegidos**: Los PDFs y `.env` no se suben al repositorio  
**API Key segura**: Configuración local únicamente  
**Sin datos sensibles**: Solo metadatos estructurados en la DB  

## Solución de problemas

### Error de permisos
```bash
chmod 755 ./facturas
sudo chown -R $USER:$USER ./facturas  # si es necesario
```

### Error de API Key
- Verifica que `GOOGLE_API_KEY` esté correcta en `.env`
- Confirma que la API esté habilitada en Google AI Studio
- Prueba con: `python3 test_gemini.py`

### PDFs no detectados
```bash
python3 debug_facturas.py  # Ver qué encuentra el sistema
ls -la ./facturas/         # Verificar archivos y permisos
```

### Error de conversión CSV
- Revisa el archivo `llm_usage.csv` para ver errores de Gemini
- Aumenta `MAX_OUTPUT_TOKENS` en `.env` si las facturas son complejas
- Prueba con `LOG_LEVEL=DEBUG` para más detalles

## Próximas mejoras

**Interfaz web**: Streamlit para subir y procesar facturas  
**OCR mejorado**: Para PDFs escaneados o de baja calidad  
**Categorización**: Clasificación automática de gastos  
**Dashboard**: Visualización de métricas y tendencias  
**API REST**: Endpoints para integración con otros sistemas  
**Tests unitarios**: Cobertura completa de funcionalidades  

## Configuración de Git (para contribuir)
```bash
git init
git add .
git commit -m "feat: initial ETL implementation"
git branch -M main
git remote add origin https://github.com/juanduque09/ETL-AI.git
git push -u origin main
```

## Notas técnicas

- **Reintentos**: Sistema robusto con backoff exponencial y jitter
- **Fallback**: Cambia automáticamente de modelo si hay sobrecarga
- **Métricas**: Registro detallado en `llm_usage.csv` para auditoría
- **Formatos**: Soporta PDFs nativos (texto seleccionable)
- **Monedas**: Conversión configurable USD/EUR → COP
- **Logging**: Configurable desde INFO hasta DEBUG

---

