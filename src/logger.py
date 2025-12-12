"""
Módulo de logging para el sistema de detección de poses.
Configura logging centralizado para toda la aplicación.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "pose_detection", level: int = logging.INFO) -> logging.Logger:
    """
    Configura y retorna un logger para la aplicación.
    
    Args:
        name: Nombre del logger
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers si ya está configurado
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Formato de los mensajes
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"pose_detection_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "pose_detection") -> logging.Logger:
    """
    Obtiene un logger existente o crea uno nuevo.
    
    Args:
        name: Nombre del logger
    
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)