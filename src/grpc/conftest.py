"""
Configuración global para pytest
"""
import sys
import os

# Añadir el directorio src al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Añadir también el directorio raíz por si acaso
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))