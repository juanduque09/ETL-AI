import os
import random
from datetime import datetime, timedelta

def crear_facturas_demo():
    """Crea PDFs de ejemplo para probar el sistema"""
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError:
        print("❌ Error: reportlab no está instalado")
        print("🔧 Instala con: pip install reportlab")
        return
    
    # Verificar que la carpeta facturas existe
    if not os.path.exists("./facturas"):
        print("❌ Carpeta './facturas' no encontrada")
        return
    
    print("🏗️ Opciones disponibles:")
    print("1. Crear facturas fijas (predefinidas)")  
    print("2. Crear facturas aleatorias")
    print("3. Crear ambos tipos")
    
    opcion = input("\nElige una opción (1/2/3): ").strip()
    
    if opcion in ['1', '3']:
        crear_facturas_fijas()
    
    if opcion in ['2', '3']:
        cantidad = input("¿Cuántas facturas aleatorias? (default: 5): ").strip()
        try:
            cantidad = int(cantidad) if cantidad else 5
            crear_facturas_aleatorias(cantidad)
        except ValueError:
            print("⚠️ Cantidad inválida, usando 5")
            crear_facturas_aleatorias(5)

def crear_facturas_fijas():
    """Crea las facturas predefinidas de siempre"""
    
    facturas_ejemplo = [
        {
            "archivo": "./facturas/demo_servicios_web.pdf",
            "empresa": "Desarrollo Web Pro SAS",
            "nit": "901234567-8",
            "fecha": "15/01/2024",
            "concepto": "Desarrollo sitio web corporativo",
            "valor": "3.500.000",
            "moneda": "COP"
        },
        {
            "archivo": "./facturas/demo_amazon_hosting.pdf", 
            "empresa": "Amazon Web Services",
            "nit": "US123456789",
            "fecha": "20/01/2024",
            "concepto": "Servicios de hosting cloud AWS",
            "valor": "150.00",
            "moneda": "USD"
        },
        {
            "archivo": "./facturas/demo_consultoria_tech.pdf",
            "empresa": "Tech Solutions Colombia LTDA",
            "nit": "800987654-3", 
            "fecha": "05/02/2024",
            "concepto": "Consultoría en automatización de procesos",
            "valor": "5.800.000",
            "moneda": "COP"
        },
        {
            "archivo": "./facturas/demo_software_europa.pdf",
            "empresa": "European Software Solutions GmbH",
            "nit": "DE987654321", 
            "fecha": "12/02/2024",
            "concepto": "Licencia software de gestión empresarial",
            "valor": "299.99",
            "moneda": "EUR"
        }
    ]
    
    exitos = 0
    
    for factura in facturas_ejemplo:
        try:
            # Verificar si el archivo ya existe
            if os.path.exists(factura["archivo"]):
                print(f"⏭️ Ya existe: {factura['archivo']}")
                continue
                
            crear_pdf_factura(factura)
            print(f"✅ Creada: {factura['archivo']}")
            exitos += 1
        except Exception as e:
            print(f"❌ Error creando {factura['archivo']}: {e}")
    
    print(f"📄 Facturas fijas: {exitos} creadas")

def crear_facturas_aleatorias(cantidad=5):
    """Crea facturas con datos aleatorios"""
    
    empresas = [
        ("TechCorp Solutions SAS", "901000000-1", "COP"),
        ("Global Systems Inc", "US555666777", "USD"),
        ("European Tech GmbH", "DE123456789", "EUR"),
        ("Digital Services LTDA", "800999888-7", "COP"),
        ("Cloud Computing Corp", "US777888999", "USD"),
        ("Innovation Labs S.A.", "FR987654321", "EUR"),
        ("Software Development SAS", "900111222-3", "COP"),
        ("AI Solutions Inc", "US333444555", "USD"),
        ("Data Analytics GmbH", "DE555777999", "EUR"),
        ("Mobile Apps Colombia", "800777666-5", "COP")
    ]
    
    conceptos = [
        "Desarrollo de aplicación móvil",
        "Consultoría en transformación digital", 
        "Licencia de software empresarial",
        "Servicios de hosting y dominio",
        "Mantenimiento de sistemas",
        "Auditoría de seguridad informática",
        "Implementación de base de datos",
        "Diseño de arquitectura de software",
        "Soporte técnico especializado",
        "Migración a la nube",
        "Análisis de datos y reporting",
        "Desarrollo de API REST",
        "Integración de sistemas",
        "Capacitación técnica",
        "Optimización de rendimiento"
    ]
    
    exitos = 0
    
    for i in range(cantidad):
        # Datos aleatorios
        empresa, nit, moneda = random.choice(empresas)
        concepto = random.choice(conceptos)
        
        # Fecha aleatoria en los últimos 6 meses
        fecha_base = datetime.now() - timedelta(days=random.randint(1, 180))
        fecha = fecha_base.strftime("%d/%m/%Y")
        
        # Valor aleatorio según moneda
        if moneda == "COP":
            valor = f"{random.randint(500, 10000) * 1000:,}".replace(",", ".")
        elif moneda == "USD":
            valor = f"{random.randint(50, 2000)}.{random.randint(0, 99):02d}"
        else:  # EUR
            valor = f"{random.randint(100, 1500)}.{random.randint(0, 99):02d}"
        
        # Nombre único del archivo
        timestamp = int(datetime.now().timestamp())
        archivo = f"./facturas/random_{timestamp}_{i+1:03d}.pdf"
        
        factura_data = {
            "archivo": archivo,
            "empresa": empresa,
            "nit": nit,
            "fecha": fecha,
            "concepto": concepto,
            "valor": valor,
            "moneda": moneda
        }
        
        try:
            crear_pdf_factura(factura_data)
            print(f"✅ Aleatoria {i+1}/{cantidad}: {os.path.basename(archivo)}")
            exitos += 1
        except Exception as e:
            print(f"❌ Error creando factura aleatoria {i+1}: {e}")
    
    print(f"🎲 Facturas aleatorias: {exitos}/{cantidad} creadas")

def crear_pdf_factura(datos):
    """Crea un PDF de factura con los datos proporcionados"""
    
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    c = canvas.Canvas(datos["archivo"], pagesize=letter)
    width, height = letter
    
    # Título
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "FACTURA ELECTRÓNICA")
    
    # Número de factura
    c.setFont("Helvetica", 10)
    c.drawString(width - 200, height - 50, f"No: {hash(datos['archivo']) % 10000:04d}")
    
    # Datos de la empresa
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "DATOS DEL EMISOR:")
    
    c.setFont("Helvetica", 11)
    y = height - 120
    c.drawString(50, y, f"Empresa: {datos['empresa']}")
    c.drawString(50, y - 18, f"NIT/ID: {datos['nit']}")
    c.drawString(50, y - 36, f"Fecha de emisión: {datos['fecha']}")
    
    # Separador
    y -= 70
    c.setStrokeColorRGB(0.5, 0.5, 0.5)
    c.line(50, y, width - 50, y)
    c.setStrokeColorRGB(0, 0, 0)
    
    # Detalle
    y -= 25
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "DETALLE DE PRODUCTOS/SERVICIOS:")
    
    c.setFont("Helvetica", 11)
    y -= 25
    c.drawString(50, y, f"Descripción: {datos['concepto']}")
    c.drawString(50, y - 18, "Cantidad: 1 unidad")
    
    # Valores en caja
    y -= 50
    c.setStrokeColorRGB(0.3, 0.3, 0.3)
    c.rect(50, y - 40, width - 100, 60, stroke=1, fill=0)
    
    c.setFont("Helvetica-Bold", 12)
    y_box = y - 15
    
    if datos['moneda'] == 'COP':
        valor_texto = f"${datos['valor']} COP"
        moneda_completa = "Pesos Colombianos"
    elif datos['moneda'] == 'USD': 
        valor_texto = f"${datos['valor']} USD"
        moneda_completa = "Dólares Estadounidenses"
    elif datos['moneda'] == 'EUR':
        valor_texto = f"€{datos['valor']} EUR"  
        moneda_completa = "Euros"
    else:
        valor_texto = f"{datos['valor']} {datos['moneda']}"
        moneda_completa = datos['moneda']
    
    c.drawString(60, y_box, f"VALOR TOTAL: {valor_texto}")
    c.setFont("Helvetica", 10)
    c.drawString(60, y_box - 15, f"Moneda: {moneda_completa}")
    
    # Información adicional
    y -= 80
    c.setFont("Helvetica", 9)
    c.drawString(50, y, f"Método de pago: Transferencia bancaria")
    c.drawString(50, y - 12, f"Términos: Pago a 30 días")
    
    # Footer
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    tipo = "🎲 ALEATORIA" if "random_" in datos["archivo"] else "🆕 DEMO"
    c.drawString(50, 30, f"{tipo} - Factura generada para pruebas del sistema ETL")
    c.drawString(50, 18, f"Archivo: {os.path.basename(datos['archivo'])}")
    
    c.save()

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    
    dependencias = {
        'reportlab': 'reportlab',
        'pandas': 'pandas', 
        'google.generativeai': 'google-generativeai',
        'fitz': 'PyMuPDF',
        'sqlalchemy': 'sqlalchemy',
        'dotenv': 'python-dotenv'
    }
    
    print("🔍 Verificando dependencias...")
    faltantes = []
    
    for modulo, paquete in dependencias.items():
        try:
            __import__(modulo)
            print(f"✅ {paquete}")
        except ImportError:
            print(f"❌ {paquete}")
            faltantes.append(paquete)
    
    if faltantes:
        print(f"\n🔧 Instala las dependencias faltantes:")
        print(f"pip install {' '.join(faltantes)}")
        return False
    
    print("\n🎉 Todas las dependencias están instaladas!")
    return True

def mostrar_resumen():
    """Muestra resumen de todos los PDFs disponibles"""
    
    if not os.path.exists("./facturas"):
        return
        
    pdfs = [f for f in os.listdir("./facturas") if f.lower().endswith('.pdf')]
    
    if pdfs:
        print(f"\n📊 Total PDFs en ./facturas/: {len(pdfs)}")
        for pdf in sorted(pdfs):
            tamaño = os.path.getsize(os.path.join("./facturas", pdf))
            if pdf.startswith("demo_"):
                tipo = "🆕 DEMO"
            elif pdf.startswith("random_"):
                tipo = "🎲 ALEATORIA"
            else:
                tipo = "📄 Original"
            print(f"   {tipo}: {pdf} ({tamaño:,} bytes)")

if __name__ == "__main__":
    print("🏗️ Generador de facturas de demo")
    print("=" * 50)
    
    if verificar_dependencias():
        # Arreglar permisos si es necesario
        try:
            os.chmod("./facturas", 0o755)
        except:
            pass
            
        crear_facturas_demo()
        mostrar_resumen()
        
        print("\n📋 Comandos útiles:")
        print("python3 test_gemini.py        # Probar sistema completo")
        print("python3 main.py --overwrite   # Procesar todas las facturas")
        print("python3 debug_facturas.py     # Ver estructura de facturas")
    else:
        print("\n💥 Instala las dependencias faltantes primero.")
