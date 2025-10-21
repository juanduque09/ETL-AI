import os
from dotenv import load_dotenv
import google.generativeai as genai
from prompt import prompt
import funciones

# Cargar variables de entorno
load_dotenv(".env")

def test_gemini_connection():
    """Prueba la conexión con Gemini usando un texto de factura de ejemplo"""
    
    # Configurar Gemini
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "models/gemini-2.0-flash")
    
    if not GOOGLE_API_KEY:
        print("❌ Error: GOOGLE_API_KEY no encontrada en .env")
        return False
    
    print(f"🔑 API Key configurada: {GOOGLE_API_KEY[:10]}...")
    print(f"🤖 Modelo: {MODEL_NAME}")
    
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Texto de factura de ejemplo
    texto_ejemplo = """
    FACTURA ELECTRONICA
    Empresa: Tech Solutions SAS
    NIT: 900123456-7
    Fecha: 15/01/2024
    
    DETALLE:
    Servicio de consultoría técnica
    Cantidad: 1
    Valor unitario: $2.500.000 COP
    Total: $2.500.000 COP
    
    Forma de pago: Transferencia bancaria
    """
    
    try:
        print("\n🚀 Probando conexión con Gemini...")
        print("📄 Texto de ejemplo enviado:")
        print("-" * 50)
        print(texto_ejemplo)
        print("-" * 50)
        
        model = genai.GenerativeModel(MODEL_NAME)
        
        respuesta = model.generate_content(
            prompt + "\n Este es el texto a parsear:\n" + texto_ejemplo
        )
        
        print("\n✅ Respuesta de Gemini:")
        print("-" * 50)
        print(respuesta.text)
        print("-" * 50)
        
        # Verificar que la respuesta tenga formato CSV
        lines = respuesta.text.strip().split('\n')
        if len(lines) >= 2 and 'fecha_factura;proveedor;concepto;importe;moneda' in lines[0]:
            print("✅ Formato CSV correcto detectado")
            print("✅ Conexión con Gemini exitosa!")
            return True
        else:
            print("⚠️ Formato inesperado en la respuesta")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando con Gemini: {str(e)}")
        return False

def listar_facturas_disponibles():
    """Lista todas las facturas PDF disponibles"""
    
    print("\n📁 Facturas disponibles:")
    
    if not os.path.exists("./facturas"):
        print("❌ Carpeta './facturas' no encontrada")
        return []
    
    facturas = []
    
    # Buscar PDFs directamente en ./facturas/
    archivos_directos = [f for f in os.listdir("./facturas") 
                        if f.lower().endswith('.pdf') and os.path.isfile(os.path.join("./facturas", f))]
    
    if archivos_directos:
        print("📂 Facturas en carpeta raíz:")
        for archivo in sorted(archivos_directos):
            ruta_completa = os.path.join("./facturas", archivo)
            tamaño = os.path.getsize(ruta_completa)
            print(f"   📄 {archivo} ({tamaño:,} bytes)")
            facturas.append(ruta_completa)
    
    # Buscar en subcarpetas
    for item in sorted(os.listdir("./facturas")):
        ruta_item = os.path.join("./facturas", item)
        if os.path.isdir(ruta_item):
            archivos_pdf = [f for f in os.listdir(ruta_item) if f.lower().endswith('.pdf')]
            if archivos_pdf:
                print(f"📂 {item}/:")
                for archivo in sorted(archivos_pdf):
                    ruta_completa = os.path.join(ruta_item, archivo)
                    tamaño = os.path.getsize(ruta_completa)
                    print(f"   📄 {archivo} ({tamaño:,} bytes)")
                    facturas.append(ruta_completa)
    
    if not facturas:
        print("❌ No se encontraron archivos PDF")
    else:
        print(f"\n✅ Total: {len(facturas)} facturas encontradas")
    
    return facturas

def test_pipeline_completo():
    """Prueba el pipeline completo con una factura real existente"""
    
    print("\n🧪 Probando pipeline completo...")
    
    # Buscar facturas disponibles
    facturas_encontradas = listar_facturas_disponibles()
    
    if not facturas_encontradas:
        print("📝 No se encontraron PDFs. Probando con texto de ejemplo...")
        return test_pipeline_con_texto()
    
    # Usar la primera factura encontrada
    ruta_pdf = facturas_encontradas[0]
    print(f"📄 Usando para prueba: {ruta_pdf}")
    
    try:
        print("📖 Extrayendo texto del PDF...")
        texto_extraido = funciones.extraer_texto_pdf(ruta_pdf)
        
        if not texto_extraido or len(texto_extraido) < 10:
            print("❌ Texto extraído muy corto o vacío")
            return False
        
        print(f"✅ Texto extraído: {len(texto_extraido)} caracteres")
        print("📝 Primeros 200 caracteres:")
        print("-" * 30)
        print(texto_extraido[:200] + "...")
        print("-" * 30)
        
        print("🤖 Estructurando texto con Gemini...")
        csv_resultado = funciones.estructurar_texto(texto_extraido)
        
        if csv_resultado.lower().strip() == "error":
            print("❌ Gemini devolvió error")
            return False
        
        print("✅ CSV generado:")
        print("-" * 30)
        print(csv_resultado)
        print("-" * 30)
        
        print("📊 Convirtiendo a DataFrame...")
        df = funciones.csv_a_dataframe(csv_resultado)
        
        print("✅ DataFrame creado:")
        print(df)
        print("\n📋 Información del DataFrame:")
        print(f"- Filas: {len(df)}")
        print(f"- Columnas: {list(df.columns)}")
        print(f"- Tipos: {df.dtypes.to_dict()}")
        
        # Verificar datos
        if len(df) > 0:
            print("✅ Pipeline completo funcionando correctamente!")
            return True
        else:
            print("❌ DataFrame vacío")
            return False
            
    except Exception as e:
        print(f"❌ Error en pipeline: {str(e)}")
        return False

def test_pipeline_con_texto():
    """Fallback para probar pipeline solo con texto"""
    
    texto_factura_ejemplo = """
    FACTURA DE VENTA
    
    DATOS DEL EMISOR:
    Empresa: Servicios Digitales LTDA
    NIT: 901234567-8
    
    DATOS DE LA FACTURA:
    Número: FV-001-2024
    Fecha de emisión: 25/01/2024
    Fecha de vencimiento: 25/02/2024
    
    DETALLE DE PRODUCTOS/SERVICIOS:
    Descripción: Desarrollo de aplicación web
    Cantidad: 1
    Valor unitario: $8.750.000 COP
    Subtotal: $8.750.000 COP
    IVA (19%): $1.662.500 COP
    TOTAL A PAGAR: $10.412.500 COP
    
    Moneda: Pesos Colombianos (COP)
    """
    
    try:
        print("📝 Estructurando texto con Gemini...")
        csv_resultado = funciones.estructurar_texto(texto_factura_ejemplo)
        
        if csv_resultado.lower().strip() == "error":
            print("❌ Gemini devolvió error")
            return False
        
        print("✅ CSV generado:")
        print("-" * 30)
        print(csv_resultado)
        print("-" * 30)
        
        print("📊 Convirtiendo a DataFrame...")
        df = funciones.csv_a_dataframe(csv_resultado)
        
        print("✅ DataFrame creado:")
        print(df)
        print("\n📋 Información del DataFrame:")
        print(f"- Filas: {len(df)}")
        print(f"- Columnas: {list(df.columns)}")
        print(f"- Tipos: {df.dtypes.to_dict()}")
        
        # Verificar datos
        if len(df) > 0:
            print("✅ Pipeline completo funcionando correctamente!")
            return True
        else:
            print("❌ DataFrame vacío")
            return False
            
    except Exception as e:
        print(f"❌ Error en pipeline: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Test de conexión con Gemini")
    print("=" * 50)
    
    # Test 1: Conexión básica
    success1 = test_gemini_connection()
    
    # Test 2: Pipeline completo
    success2 = test_pipeline_completo()
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE TESTS:")
    print(f"✅ Conexión Gemini: {'OK' if success1 else 'FAIL'}")
    print(f"✅ Pipeline completo: {'OK' if success2 else 'FAIL'}")
    
    if success1 and success2:
        print("\n🎉 ¡Todos los tests pasaron! Sistema listo para usar.")
        print("\n📝 Pasos siguientes:")
        print("1. Ejecuta: python3 main.py --overwrite")
        print("2. Verifica resultados en facturas.db")
        print("3. O crea más PDFs de prueba: python3 setup_demo.py")
    else:
        print("\n💥 Algunos tests fallaron. Revisa la configuración.")
