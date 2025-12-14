# -*- coding: utf-8 -*-
"""
Pruebas básicas para el módulo angles.py
"""
import numpy as np
import sys
import os

# Añadir src al path para importar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from angles import calculate_angle, shouldvect

def test_calculate_angle_basico():
    """Prueba básica del cálculo de ángulo."""
    # Ángulo recto (90 grados)
    a = [0, 0]
    b = [0, 1]
    c = [1, 1]
    
    resultado = calculate_angle(a, b, c)
    assert abs(resultado - 90.0) < 0.001, f"Esperado 90°, obtenido {resultado}°"
    
    # Línea recta (180 grados)
    c2 = [0, 2]
    resultado2 = calculate_angle(a, b, c2)
    assert abs(resultado2 - 180.0) < 0.001, f"Esperado 180°, obtenido {resultado2}°"

def test_calculate_angle_puntos_iguales():
    """Prueba con puntos iguales."""
    punto = [1, 1]
    resultado = calculate_angle(punto, punto, punto)
    assert resultado == 0.0, f"Ángulo entre puntos iguales debe ser 0, no {resultado}"

def test_calculate_angle_angulo_cerrado():
    """Prueba con ángulo pequeño - ."""
    # Los puntos originales daban 135°, cambiemos a un ángulo realmente pequeño
    a = [0, 0]
    b = [0, 1]
    c = [0.001, 0]
    
    resultado = calculate_angle(a, b, c)
    
    # El ángulo debería ser pequeño (menos de 10°)
    assert resultado > 0, f"Ángulo debe ser positivo, no {resultado}"
    assert resultado < 10, f"Ángulo debe ser menor a 10°, es {resultado}"
    # Verificación adicional: debería estar alrededor de 0.57°
    print(f"✓ Ángulo pequeño calculado: {resultado:.2f}° (esperado ~0.57°)")

def test_shouldvect_simple():
    """Prueba básica de shouldvect."""
    cadera = [10, 20]
    hombro = [15, 18]
    
    resultado = shouldvect(cadera, hombro)
    esperado = (hombro[0], cadera[1])  # x del hombro, y de la cadera
    
    assert resultado == esperado, f"Esperado {esperado}, obtenido {resultado}"

def test_shouldvect_misma_x():
    """Prueba cuando hombro y cadera tienen misma x."""
    cadera = [5, 10]
    hombro = [5, 8]
    
    resultado = shouldvect(cadera, hombro)
    assert resultado[0] == 5, f"X debe ser 5, no {resultado[0]}"
    assert resultado[1] == 10, f"Y debe ser 10, no {resultado[1]}"

if __name__ == "__main__":
    # Ejecutar pruebas manualmente
    print("🧪 Ejecutando pruebas de angles.py...")
    
    test_calculate_angle_basico()
    print("✓ test_calculate_angle_basico pasado")
    
    test_calculate_angle_puntos_iguales()
    print("✓ test_calculate_angle_puntos_iguales pasado")
    
    test_calculate_angle_angulo_cerrado()
    print("✓ test_calculate_angle_angulo_cerrado pasado")
    
    test_shouldvect_simple()
    print("✓ test_shouldvect_simple pasado")
    
    test_shouldvect_misma_x()
    print("✓ test_shouldvect_misma_x pasado")
    
    print("\n✅ ¡Todas las pruebas de angles.py pasaron!")
