# run_server.py
import sys
import os

# Añadir src al path de Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 50)
print("SERVIDOR gRPC - ANÁLISIS DE MOVIMIENTO")
print("=" * 50)
print("📂 Estructura de imports:")
print(f"   Directorio actual: {os.getcwd()}")
print(f"   src/ disponible: {os.path.exists('src')}")
print(f"   generated/ disponible: {os.path.exists('src/generated')}")
print("=" * 50)

try:
    # Verificar que existen los módulos generados
    from generated import pose_analysis_pb2
    print("✅ Módulos gRPC importados correctamente")
    
    from src.grpc.server import serve 
    print("✅ Servidor gRPC importado correctamente")
    
    # Iniciar servidor
    serve(port=50051)
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\n⚠️ Solución:")
    print("1. Verifica que los archivos .proto están en src/proto/")
    print("2. Ejecuta: python generate_proto.py")
    print("3. Asegúrate de que src/generated/ existe")
except Exception as e:
    print(f"❌ Error: {e}")