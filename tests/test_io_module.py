"""
Pruebas básicas para el módulo io_module.py
"""
import sys
import os
import tempfile
from pathlib import Path

# Añadir src al path para importar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Importar DESPUÉS de añadir al path
from io_module import neededfiles, archi, sailor, figname

def test_neededfiles_crea_directorios():
    """Prueba que neededfiles crea directorios."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        nombres = ['carpeta1', 'carpeta2']
        neededfiles(str(tmp_path), nombres)
        
        for nombre in nombres:
            ruta = tmp_path / nombre
            assert ruta.exists()

def test_archi_elimina_archivo():
    """Prueba que archi elimina un archivo."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        archivo = tmp_path / 'test.txt'
        archivo.write_text('contenido')
        
        assert archivo.exists()
        archi(str(archivo))
        assert not archivo.exists()

if __name__ == "__main__":
    test_neededfiles_crea_directorios()
    test_archi_elimina_archivo()
    print("✅ ¡Pruebas de io_module.py pasaron!")