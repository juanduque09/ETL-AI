"""
Script de demostración para generar reportes visuales con datos de ejemplo
Ejecuta este script para ver cómo lucen los reportes sin necesidad de procesar facturas reales
"""

import pandas as pd
import generar_reporte
from datetime import datetime, timedelta
import random

# Generar datos de ejemplo
print("📊 Generando datos de ejemplo...")

proveedores = [
    "Tech Solutions S.A.S",
    "Suministros Industriales LTDA",
    "Comercializadora Global",
    "Servicios Profesionales",
    "Distribuidora Nacional",
    "Productos Especializados",
    "Importaciones Express",
    "Soluciones Corporativas"
]

# Generar 50 facturas de ejemplo
datos = []
fecha_inicio = datetime.now() - timedelta(days=90)

for i in range(50):
    factura = {
        'proveedor': random.choice(proveedores),
        'fecha': (fecha_inicio + timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d'),
        'importe': round(random.uniform(500000, 15000000), 2),
        'moneda': random.choices(['pesos', 'dolares', 'euros'], weights=[70, 20, 10])[0]
    }
    datos.append(factura)

# Crear DataFrame
df = pd.DataFrame(datos)

print(f"✅ Generados {len(df)} registros de ejemplo")
print("\n📋 Muestra de datos:")
print(df.head(10).to_string())

# Mostrar estadísticas
print(f"\n💰 Total importe: ${df['importe'].sum():,.0f} COP")
print(f"📊 Promedio por factura: ${df['importe'].mean():,.0f} COP")
print(f"📈 Factura más alta: ${df['importe'].max():,.0f} COP")
print(f"📉 Factura más baja: ${df['importe'].min():,.0f} COP")

# Generar reportes
print("\n🎨 Generando reportes visuales con diseño baronial...")
try:
    generar_reporte.generar_reporte_visual(df, "demo_reporte_completo.png")
    generar_reporte.generar_reporte_compacto(df, "demo_reporte_compacto.png")
    
    print("\n✨ ¡Reportes generados exitosamente!")
    print("📁 Archivos creados:")
    print("   - demo_reporte_completo.png")
    print("   - demo_reporte_compacto.png")
    print("\n💡 Abre los archivos PNG para ver los reportes con diseño baronial")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
