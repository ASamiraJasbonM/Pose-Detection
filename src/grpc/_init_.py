# src/grpc/__init__.py
"""
Módulos gRPC para comunicación cliente-servidor.
"""

from .client import PoseAnalysisClient, create_client
from .server import serve, PoseAnalysisServicer

__all__ = [
    'PoseAnalysisClient',
    'create_client', 
    'serve',
    'PoseAnalysisServicer'
]