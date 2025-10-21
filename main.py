import funciones
import pandas as pd
import os
import argparse
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(".env")

# Obtener tasas de conversión desde .env
FALLBACK_RATE_USD_COP = float(os.getenv("FALLBACK_RATE_USD_COP", "4500"))
FALLBACK_RATE_EUR_COP = float(os.getenv("FALLBACK_RATE_EUR_COP", "4900"))

def procesar_facturas_directas(carpeta_facturas):
    """Procesa PDFs que están directamente en la carpeta facturas"""
    facturas_procesadas = []
    
    for archivo in os.listdir(carpeta_facturas):
        if not archivo.lower().endswith('.pdf'):
            continue
            
        ruta_pdf = os.path.join(carpeta_facturas, archivo)
        
        if not os.path.isfile(ruta_pdf):
            continue
            
        print(f"📄 Procesando factura: {ruta_pdf}")
        facturas_procesadas.append(ruta_pdf)
    
    return facturas_procesadas

def procesar_facturas_subcarpetas(carpeta_facturas):
    """Procesa PDFs que están en subcarpetas dentro de facturas"""
    facturas_procesadas = []
    
    for carpeta in sorted(os.listdir(carpeta_facturas)):
        ruta_carpeta = os.path.join(carpeta_facturas, carpeta)
        
        if not os.path.isdir(ruta_carpeta):
            continue

        # Recorrer todos los archivos dentro de la carpeta
        for archivo in os.listdir(ruta_carpeta):
            if not archivo.lower().endswith('.pdf'):
                continue
                
            ruta_pdf = os.path.join(ruta_carpeta, archivo)

            print(f"📄 Procesando factura: {ruta_pdf}")
            facturas_procesadas.append(ruta_pdf)
    
    return facturas_procesadas

def main():
    # Configurar argumentos
    parser = argparse.ArgumentParser(description='Procesar facturas PDF a base de datos')
    parser.add_argument('--overwrite', action='store_true', 
                       help='Reemplazar tabla existente en lugar de anexar')
    args = parser.parse_args()

    # Verificar que existe la carpeta facturas
    if not os.path.exists("./facturas"):
        print("❌ Carpeta './facturas' no encontrada")
        return

    # Crear un DataFrame vacío para almacenar todas las facturas
    df = pd.DataFrame()

    print("🔍 Buscando facturas...")
    
    # Buscar PDFs directamente en ./facturas/
    facturas_directas = procesar_facturas_directas("./facturas")
    
    # Buscar PDFs en subcarpetas de ./facturas/
    facturas_subcarpetas = procesar_facturas_subcarpetas("./facturas")
    
    # Combinar todas las facturas encontradas
    todas_las_facturas = facturas_directas + facturas_subcarpetas
    
    if not todas_las_facturas:
        print("❌ No se encontraron archivos PDF para procesar")
        return

    print(f"✅ Encontradas {len(todas_las_facturas)} facturas para procesar")

    # Procesar cada factura encontrada
    for ruta_pdf in todas_las_facturas:
        try:
            # Extraer texto de la factura
            texto_no_estructurado = funciones.extraer_texto_pdf(ruta_pdf)

            # Estructurar el texto de la factura
            texto_estructurado = funciones.estructurar_texto(texto_no_estructurado)
            
            if texto_estructurado.lower().strip() == "error":
                print(f"❌ Error procesando {ruta_pdf}")
                continue

            # Convertir texto estructurado en dataframe
            df_factura = funciones.csv_a_dataframe(texto_estructurado)

            # Anexar el dataframe de la factura al dataframe general
            df = pd.concat([df, df_factura], ignore_index=True)

        except Exception as e:
            print(f"❌ Error procesando {ruta_pdf}: {str(e)}")
            continue

    if df.empty:
        print("❌ No se procesaron facturas exitosamente")
        return

    print(f"✅ Se procesaron {len(df)} facturas correctamente")

    # Convertir monedas a pesos colombianos (COP)
    print("💱 Convirtiendo monedas a COP...")
    
    # Convertir dólares a COP
    mask_dolares = df["moneda"] == "dolares"
    if mask_dolares.any():
        df.loc[mask_dolares, "importe"] *= FALLBACK_RATE_USD_COP
        df.loc[mask_dolares, "moneda"] = "pesos"
        print(f"   💵 Convertidas {mask_dolares.sum()} facturas de dólares a COP")
    
    # Convertir euros a COP  
    mask_euros = df["moneda"] == "euros"
    if mask_euros.any():
        df.loc[mask_euros, "importe"] *= FALLBACK_RATE_EUR_COP
        df.loc[mask_euros, "moneda"] = "pesos"
        print(f"   💶 Convertidas {mask_euros.sum()} facturas de euros a COP")

    # Mostrar resumen por monedas
    print("📊 Resumen por monedas:")
    print(df["moneda"].value_counts().to_string())

    # Eliminar las columnas no esenciales (mantener solo las primeras 4)
    df = df.iloc[:, 0:4]

    # Guardar en base de datos
    print("💾 Guardando en base de datos...")
    engine = create_engine("sqlite:///facturas.db")
    
    # Determinar si reemplazar o anexar
    if_exists = "replace" if args.overwrite else "append"
    
    df.to_sql("facturas", engine, if_exists=if_exists, index=False)
    engine.dispose()

    print("✅ Proceso completado exitosamente.")
    print(f"📊 {len(df)} facturas procesadas y guardadas en 'facturas.db'.")
    
    # Mostrar muestra de los datos guardados
    print("\n📋 Muestra de datos guardados:")
    print(df.head().to_string())

if __name__ == "__main__":
    main()
