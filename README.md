# Perfect-Tesis-pose-detection

Este proyecto es una aplicación de escritorio para la detección y análisis de poses corporales en tiempo real y desde archivos de video. Utiliza MediaPipe para la detección de puntos de referencia del cuerpo y calcula ángulos en las articulaciones para generar reportes y gráficas del movimiento.

## Características

- Detección de pose en tiempo real desde la cámara web.
- Análisis de pose desde archivos de video.
- Cálculo de ángulos para hombros, codos y muñecas en diferentes planos (XY, XZ, ZY).
- Generación de reportes detallados con estadísticas de los ángulos y aceleraciones (media, std, min, max, etc.).
- Creación de gráficas para visualizar los ángulos y aceleraciones a lo largo del tiempo.
- Interfaz gráfica de usuario (GUI) para un manejo sencillo de las funcionalidades.

## Instalación

1.  **Clona el repositorio (si aplica):**
    ```bash
    git clone <URL-del-repositorio>
    cd <nombre-del-repositorio>
    ```

2.  **Crea un entorno virtual:**
    ```bash
    python -m venv venv
    ```

3.  **Activa el entorno virtual:**
    -   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

## Uso

Para ejecutar la aplicación, asegúrate de tener el entorno virtual activado y luego ejecuta el siguiente comando:

```bash
python Perfect-Tesis-pose-detection.py
```

Esto abrirá la interfaz gráfica de usuario desde donde podrás acceder a todas las funcionalidades.

## Docker

También puedes construir una imagen de Docker para este proyecto.

1.  **Construye la imagen:**
    ```bash
    docker build -t pose-detection-app .
    ```

2.  **Ejecuta el contenedor:**
    ```bash
    docker run -it pose-detection-app
    ```

**Nota Importante sobre Docker:**

La aplicación utiliza una interfaz gráfica (Tkinter) y requiere acceso a la cámara web, lo cual no es soportado por defecto en los contenedores de Docker. Para que la GUI y la cámara funcionen, se necesita configuración avanzada como reenvío de X11 y pasar el dispositivo de la cámara al contenedor. Los comandos anteriores crearán y ejecutarán el contenedor, pero es probable que la aplicación falle debido a estas limitaciones.

## Dependencias Principales

- `opencv-python`
- `mediapipe`
- `numpy`
- `pandas`
- `matplotlib`
- `moviepy`
- `Pillow`
- `scikit-learn`
- `openpyxl`
