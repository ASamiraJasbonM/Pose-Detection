# Pose Detection - Sistema de Análisis de Posturas

Sistema de detección y análisis de poses corporales en tiempo real utilizando MediaPipe y OpenCV. Proyecto refactorizado con arquitectura modular para mejor mantenibilidad.

## Características

- Detección de pose en tiempo real desde cámara web
- Análisis de pose desde archivos de video
- Cálculo de ángulos para articulaciones en diferentes planos (XY, XZ, ZY)
- Generación de reportes estadísticos detallados
- Visualización de datos con gráficas interactivas
- Interfaz gráfica moderna con ttkbootstrap
- Suite de tests automatizados
- Soporte para Docker

## Requisitos

- Python 3.9+
- Webcam (para detección en tiempo real)
- Sistema operativo: Windows, macOS o Linux

## Instalación

### Opción 1: Usando uv (Recomendado - Más rápido)

```bash
# 1. Clonar el repositorio
git clone https://github.com/ASamiraJasbonM/Pose-Detection.git
cd Pose-Detection

# 2. Cambiar a la rama refactor
git checkout refactor

# 3. Instalar uv (si no lo tienes)
# Windows PowerShell:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 4. Crear ambiente virtual e instalar dependencias
uv venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

uv pip install -r requirements.txt
```

### Opción 2: Usando pip tradicional

```bash
# 1-2. Igual que arriba

# 3. Crear ambiente virtual
python -m venv .venv

# 4. Activar ambiente virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 5. Instalar dependencias
pip install -r requirements.txt
```

## Uso

### Interfaz Gráfica

```bash
python -m src.main
```

Esto abrirá la interfaz gráfica desde donde podrás:
- Detectar poses en tiempo real
- Analizar videos pregrabados
- Generar reportes y gráficas
- Exportar resultados

### Línea de Comandos (próximamente)

```bash
# Procesar un video específico
python -m src.main --input mi_video.mp4 --output resultados/

# Modo batch (sin GUI)
python -m src.main --no-gui --input video.avi
```

## Estructura del Proyecto

```
Pose-Detection/
├── src/                    # Código fuente modular
│   ├── __init__.py
│   ├── main.py            # Punto de entrada principal
│   ├── gui.py             # Interfaz gráfica
│   ├── video.py           # Procesamiento de video
│   ├── angles.py          # Cálculo de ángulos
│   ├── sensors.py         # Detección con MediaPipe
│   ├── plots.py           # Visualización de datos
│   └── io.py              # Entrada/salida de archivos
├── test/                  # Tests automatizados
│   ├── test_processing.py
│   └── test_utils.py
├── Registros/             # Reportes y datos generados
├── requirements.txt       # Dependencias del proyecto
├── Dockerfile            # Configuración Docker
└── README.md             # Este archivo
```

## Tests

Ejecutar la suite de tests:

```bash
pytest test/
```

Ejecutar tests con cobertura:

```bash
pytest test/ --cov=src
```

## Docker

### Construir imagen:

```bash
docker build -t pose-detection-app .
```

### Ejecutar contenedor:

```bash
docker run -it pose-detection-app
```

**NOTA sobre Docker:**
La aplicación usa GUI (Tkinter) y requiere acceso a cámara. Para usar en Docker necesitas:
- Configurar X11 forwarding para GUI
- Pasar dispositivo de cámara al contenedor con `--device=/dev/video0`

## Dependencias Principales

- **opencv-python** / **opencv-contrib-python**: Procesamiento de video
- **mediapipe**: Detección de poses
- **numpy**: Operaciones numéricas
- **pandas**: Análisis de datos
- **matplotlib**: Visualización
- **ttkbootstrap**: Interfaz gráfica moderna
- **moviepy**: Edición de video
- **pillow**: Procesamiento de imágenes

## Funcionalidades Detalladas

### Detección de Ángulos

El sistema calcula ángulos en las siguientes articulaciones:
- **Hombros** (izquierdo y derecho)
- **Codos** (izquierdo y derecho)
- **Muñecas** (izquierda y derecha)

En tres planos diferentes:
- **XY** (plano frontal)
- **XZ** (plano sagital)
- **ZY** (plano transversal)

### Reportes Estadísticos

Para cada articulación y plano, se generan:
- Media y desviación estándar
- Valores mínimos y máximos
- Aceleraciones calculadas
- Gráficas de evolución temporal

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Haz commit de tus cambios:
   ```bash
   git commit -m 'Agrega nueva funcionalidad'
   ```
4. Push a la rama:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. Abre un Pull Request

### Guidelines para contribuir:

- Escribe tests para nuevas funcionalidades
- Documenta funciones con docstrings
- Sigue PEP 8 para estilo de código
- Actualiza el README si es necesario

## Changelog

### v2.0.0 - Refactorización (rama refactor)
- Reorganización en arquitectura modular
- Implementación de tests automatizados
- Limpieza y optimización de dependencias
- Interfaz gráfica mejorada con ttkbootstrap
- Corrección de bugs de versiones anteriores
- Documentación actualizada

### v1.0.0 - Versión inicial (rama main)
- Detección básica de poses
- Interfaz gráfica inicial
- Cálculo de ángulos básicos

## Autores

- **Adriana Samira** - Desarrollo Sistema 
- **Camilo Guerrero** - Refactorización - GRPC
- **Cesar Nieto** - CI/CD

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Agradecimientos

- [MediaPipe](https://google.github.io/mediapipe/) por la tecnología de detección de poses
- [OpenCV](https://opencv.org/) por el procesamiento de video
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) por la interfaz moderna
- Comunidad open source por las herramientas y librerías

## Soporte

Si encuentras algún bug o tienes sugerencias:
- Abre un [Issue](https://github.com/ASamiraJasbonM/Pose-Detection/issues)
- Contacta a los maintainers

