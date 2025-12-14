from setuptools import setup, find_packages

setup(
    name="PoseDetection",
    version="0.1.0",
    description="Proyecto de Detección de Pose",
    author="ASamiraJasbonM",
    # Encuentra automáticamente los paquetes en la carpeta 'src'
    packages=find_packages(where='src'),
    # Especifica que la raíz del paquete está en 'src'
    package_dir={'': 'src'},
    # No es necesario listar los requerimientos aquí,
    # ya que los instalamos desde requirements.txt en el CI.
    install_requires=[],
    python_requires='>=3.8',
)
