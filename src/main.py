# src/main.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gui import build_main_window
from logger import setup_logger

# Configurar logger
logger = setup_logger()

def main():
    logger.info("Iniciando aplicación de detección de poses")
    try:
        app = build_main_window()
        logger.info("Ventana principal construida exitosamente")
        app.mainloop()
    except Exception as e:
        logger.error(f"Error al iniciar la aplicación: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()