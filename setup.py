#!/usr/bin/env python3
"""
Script simple para ejecutar pruebas
"""
import os
import sys

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_all_tests():
    """Ejecuta todas las pruebas manualmente."""
    print("=" * 60)
    print("🧪 EJECUTANDO PRUEBAS UNITARIAS - POSE DETECTION")
    print("=" * 60)
    
    # Importar y ejecutar cada archivo de prueba
    test_files = [
        'tests/test_angles.py',
        'tests/test_io_module.py',
        'tests/test_sensors.py'
    ]
    
    all_passed = True
    
    for test_file in test_files:
        print(f"\n📄 Ejecutando {test_file}...")
        print("-" * 40)
        
        try:
            # Ejecutar el archivo como módulo
            with open(test_file, 'r', encoding='utf-8') as f:
                exec(f.read(), {'__name__': '__main__', '__file__': test_file})
        except Exception as e:
            print(f"❌ Error ejecutando {test_file}: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)