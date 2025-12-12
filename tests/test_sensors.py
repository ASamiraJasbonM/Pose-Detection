"""
Pruebas básicas para el módulo sensors.py
"""
import sys
import os
import pandas as pd
import numpy as np

# Añadir src al path para importar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sensors import RMSdtf


def test_RMSdtf_basico():
    """Prueba básica del cálculo RMS."""
    # Crear DataFrame simple
    data = {
        'col1': [1, 2, 3, 4, 5],
        'col2': [2, 3, 4, 5, 6],
        'col3': [3, 4, 5, 6, 7]
    }
    df = pd.DataFrame(data)
    
    # Calcular RMS
    rms = RMSdtf(df)
    
    # Verificar resultados
    assert len(rms) == 5, f"RMS debe tener 5 valores, tiene {len(rms)}"
    
    # Calcular manualmente para el primer valor usando RMS = sqrt(mean(x^2))
    # mean de los cuadrados = (1^2 + 2^2 + 3^2) / 3 = 14/3
    esperado = np.sqrt((1**2 + 2**2 + 3**2) / 3.0)

    assert abs(rms.iloc[0] - esperado) < 0.001, f"RMS incorrecto: {rms.iloc[0]} vs {esperado}"


    
    # Todos los valores deben ser positivos
    assert all(rms >= 0), "Todos los valores RMS deben ser positivos"

def test_RMSdtf_con_nulos():
    """Prueba RMS con valores nulos."""
    # Crear DataFrame con NaN
    data = {
        'x': [1, np.nan, 3, None, 5],
        'y': [np.nan, 2, 3, 4, np.nan],
        'z': [1, 2, np.nan, np.nan, 5]
    }
    df = pd.DataFrame(data)
    
    # Calcular RMS (debería manejar NaN)
    rms = RMSdtf(df)
    
    # Verificar que no hay NaN en el resultado
    assert not rms.isna().any(), "RMS no debe contener NaN"
    
    # Verificar primer valor (sqrt(1² + 0² + 1²) = sqrt(2) ≈ 1.414)
    if len(rms) > 0:
        # NaN se convierten a 0
        esperado = np.sqrt((1**2 + 0**2 + 1**2) / 3.0)
        assert abs(rms.iloc[0] - esperado) < 0.001

def test_RMSdtf_dataframe_vacio():
    """Prueba RMS con DataFrame vacío."""
    df = pd.DataFrame()
    
    rms = RMSdtf(df)
    
    # Debería retornar Series vacía
    assert rms.empty, "RMS de DataFrame vacío debe estar vacío"

def test_RMSdtf_una_columna():
    """Prueba RMS con solo una columna """
    data = {'valores': [-3, -2, -1, 0, 1, 2, 3]}
    df = pd.DataFrame(data)
    
    rms = RMSdtf(df)
    
    # Con una columna, RMS = sqrt(valor² / 1) = |valor|
    # Verificamos cada valor
    valores_esperados = [3.0, 2.0, 1.0, 0.0, 1.0, 2.0, 3.0]
    
    for i, esperado in enumerate(valores_esperados):
        obtenido = rms.iloc[i]
        assert abs(obtenido - esperado) < 0.001, f"RMS de {df.iloc[i, 0]} debe ser {esperado}, es {obtenido}"
    
    print("✓ RMS con una columna funciona (valor absoluto)")

def test_RMSdtf_valores_negativos():
    """Prueba RMS con valores negativos."""
    data = {
        'x': [-1, -2, -3],
        'y': [1, 2, 3],
        'z': [0, 0, 0]
    }
    df = pd.DataFrame(data)
    
    rms = RMSdtf(df)
    
    # Comprobar que la norma no depende del signo de los componentes
    rms_abs = RMSdtf(df.abs())
    assert abs(rms.iloc[0] - rms_abs.iloc[0]) < 0.001, "RMS debería ser igual que el RMS de los valores absolutos"


if __name__ == "__main__":
    # Ejecutar pruebas manualmente
    print("🧪 Ejecutando pruebas de sensors.py...")
    
    test_RMSdtf_basico()
    print("✓ test_RMSdtf_basico pasado")
    
    test_RMSdtf_con_nulos()
    print("✓ test_RMSdtf_con_nulos pasado")
    
    test_RMSdtf_dataframe_vacio()
    print("✓ test_RMSdtf_dataframe_vacio pasado")
    
    test_RMSdtf_una_columna()
    print("✓ test_RMSdtf_una_columna pasado")
    
    test_RMSdtf_valores_negativos()
    print("✓ test_RMSdtf_valores_negativos pasado")
    
    print("\n✅ ¡Todas las pruebas de sensors.py pasaron!")