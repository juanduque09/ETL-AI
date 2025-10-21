import os

def debug_estructura_facturas():
    """Debug para ver exactamente qué hay en la carpeta facturas"""
    
    print("🔍 Debug de estructura de facturas")
    print("=" * 50)
    
    # Verificar si la carpeta facturas existe
    if not os.path.exists("./facturas"):
        print("❌ Carpeta './facturas' NO existe")
        return
    
    print("✅ Carpeta './facturas' existe")
    
    # Listar todo el contenido
    try:
        contenido = os.listdir("./facturas")
        print(f"📂 Contenido de ./facturas: {contenido}")
        
        for item in contenido:
            ruta_item = os.path.join("./facturas", item)
            
            if os.path.isfile(ruta_item):
                tamaño = os.path.getsize(ruta_item)
                print(f"📄 Archivo: {item} ({tamaño:,} bytes)")
            elif os.path.isdir(ruta_item):
                print(f"📁 Carpeta: {item}/")
                try:
                    sub_contenido = os.listdir(ruta_item)
                    print(f"   Contenido: {sub_contenido}")
                    
                    for sub_item in sub_contenido:
                        ruta_sub = os.path.join(ruta_item, sub_item)
                        if os.path.isfile(ruta_sub):
                            tamaño = os.path.getsize(ruta_sub)
                            es_pdf = sub_item.lower().endswith('.pdf')
                            print(f"   📄 {sub_item} ({tamaño:,} bytes) {'✅ PDF' if es_pdf else '❌ No PDF'}")
                except PermissionError as e:
                    print(f"   ❌ Sin permisos: {e}")
            else:
                print(f"❓ Tipo desconocido: {item}")
                
    except Exception as e:
        print(f"❌ Error listando ./facturas: {e}")
    
    # Probar main.py simulado
    print("\n" + "=" * 50)
    print("🧪 Simulando lógica de main.py:")
    
    facturas_encontradas = 0
    
    for carpeta in sorted(os.listdir("./facturas")):
        ruta_carpeta = os.path.join("./facturas", carpeta)
        print(f"\n📂 Revisando: {carpeta}")
        print(f"   Ruta: {ruta_carpeta}")
        print(f"   Es directorio: {os.path.isdir(ruta_carpeta)}")
        
        if not os.path.isdir(ruta_carpeta):
            print(f"   ⏭️ Saltando (no es directorio)")
            continue
            
        try:
            archivos = os.listdir(ruta_carpeta)
            print(f"   Archivos: {archivos}")
            
            for archivo in archivos:
                es_pdf = archivo.lower().endswith('.pdf')
                print(f"   📄 {archivo} -> PDF: {es_pdf}")
                
                if es_pdf:
                    ruta_completa = os.path.join(ruta_carpeta, archivo)
                    print(f"   ✅ FACTURA ENCONTRADA: {ruta_completa}")
                    facturas_encontradas += 1
                    
        except Exception as e:
            print(f"   ❌ Error listando carpeta: {e}")
    
    print(f"\n📊 TOTAL FACTURAS ENCONTRADAS: {facturas_encontradas}")

if __name__ == "__main__":
    debug_estructura_facturas()
