# test_grpc.py
import sys
import os
import time

# Añadir src y src/generated al path (asegura que Python encuentre los módulos generados)
ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "src", "generated"))

print("🧪 PRUEBA DEL SISTEMA gRPC")
print("=" * 50)

# Importar módulos protobuf/gRPC (desde src/generated)
try:
    import pose_analysis_pb2 as pb
    import pose_analysis_pb2_grpc as pb_grpc
except Exception as e:
    # Si falla aquí, el resto de pruebas de imports también fallarán; lo mostramos claramente
    print(f"❌ Error importando módulos protobuf/gRPC: {e}")

def test_imports():
    """Prueba que todos los módulos se importan correctamente"""
    print("\n1. Probando imports...")
    try:
        # Módulos generados (ya añadimos src/generated al sys.path)
        import pose_analysis_pb2  # alias pb ya importado arriba
        import pose_analysis_pb2_grpc
        print("   ✅ Módulos gRPC generados")

        # Módulos gRPC personalizados (import directo desde paquete src.grpc)
        # Asegúrate de ejecutar desde la raíz del repo con -m para que src sea paquete
        import src.grpc.client as client_mod
        import src.grpc.server as server_mod
        print("   ✅ Módulos gRPC personalizados")

        # Otros módulos del proyecto (desde src)
        import src.video as video
        import src.angles as angles
        import src.io_module as io_module
        import src.sensors as sensors
        print("   ✅ Módulos del proyecto (src/)")
        return True

    except ImportError as e:
        print(f"   ❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado durante imports: {e}")
        return False

def test_server_connection():
    """Prueba la conexión al servidor"""
    print("\n2. Probando conexión al servidor...")
    try:
        from src.grpc.client import create_client
        client = create_client('localhost:50051')
        print("   ✅ Cliente creado (servidor no necesariamente corriendo)")
        client.close()
        return True
    except Exception as e:
        print(f"   ⚠️  Error de conexión (normal si el servidor no está corriendo): {e}")
        return False

def test_protobuf_messages():
    """Prueba la creación de mensajes protobuf"""
    print("\n3. Probando mensajes protobuf...")
    try:
        # Usar el módulo pb importado al inicio
        landmark = pb.Landmark(
            name="left_shoulder",
            x=0.5, y=0.3, z=0.1,
            visibility=0.9
        )
        video_frame = pb.VideoFrame(
            frame_data=b"test",
            timestamp=123456789,
            frame_number=1
        )
        print(f"   ✅ Mensajes creados: {landmark.name}, frame #{video_frame.frame_number}")
        return True
    except Exception as e:
        print(f"   ❌ Error creando mensajes: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("📋 Ejecutando pruebas del sistema gRPC...")

    tests = [
        ("Imports", test_imports),
        ("Mensajes Protobuf", test_protobuf_messages),
        ("Conexión Servidor", test_server_connection),
    ]

    passed = []
    failed = []

    for name, test in tests:
        ok = False
        try:
            ok = test()
        except Exception as e:
            print(f"   ❌ Excepción en la prueba {name}: {e}")
            ok = False

        if ok:
            passed.append(name)
        else:
            failed.append(name)

    print("\n" + "=" * 50)
    print("📊 RESULTADOS DE PRUEBAS:")
    print(f"   ✅ Aprobadas: {len(passed)} -> {passed}")
    print(f"   ❌ Falladas: {len(failed)} -> {failed}")

    if not failed:
        print("\n🎉 ¡Todas las pruebas pasaron!")
        print("\n📝 Pasos siguientes:")
        print("   1. Ejecuta: uv run python -m src.grpc.server (en una terminal)")
        print("   2. Ejecuta: uv run python -m src.grpc.client (en otra terminal)")
        return True
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores listados arriba.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)