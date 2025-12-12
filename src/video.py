# src/video.py
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os
import shutil
from pathlib import Path
from datetime import datetime
from tkinter import filedialog
from PIL import Image, ImageTk
import imutils
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video import fx as vfx
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from io_module import sailor, figname, archi, REGISTROS, PROJECT_ROOT
from angles import angulosxy, angulosxz, anguloszy
from plots import grafangle

# Variables globales (necesarias para compartir estado)
cap = None
filename = None

# Variables para datos procesados (compartidas con sensors.py)
XY_AC = XY_DEG = XZ_AC = XZ_DEG = ZY_AC = ZY_DEG = None

# ================= FUNCIONES DE CÁMARA =================
def iniciar(lblVideo=None, cam_index=0):
    """Inicia la cámara y muestra en el Label de Tkinter"""
    global cap
    cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
    if lblVideo:
        visualizar(lblVideo)

def visualizar(lblVideo):
    """Actualiza el Label con frames de la cámara"""
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, lambda: visualizar(lblVideo))
        else:
            if hasattr(lblVideo, 'image'):
                lblVideo.image = ""
            cap.release()

def finalizar():
    """Detiene la cámara"""
    global cap
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()

# ================= FUNCIONES DE GRABACIÓN DESDE CÁMARA =================
def obtener_datos_plano(plano: str):
    """Función genérica para grabar desde cámara en un plano específico"""
    print(f'plano {plano}')
    
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    
    cap = cv2.VideoCapture(0)
    
    # Configurar rutas según el plano
    dirc = PROJECT_ROOT
    doko = REGISTROS / plano / "videoOriginal"
    doko.mkdir(parents=True, exist_ok=True)
    
    [namemediapipe, namemeoriginal, nameangle, namedat] = sailor(str(doko), 0, 0)
    
    # Rutas completas
    pathvM = REGISTROS / plano / "video" / namemediapipe
    pathvO = REGISTROS / plano / "videoOriginal" / namemeoriginal
    pathvA = REGISTROS / plano / "angulosmediapipe" / nameangle
    
    allangle = []
    
    # Configurar video writers
    salida = cv2.VideoWriter(str(pathvM), cv2.VideoWriter_fourcc(*'XVID'), 10, (640, 480))
    original = cv2.VideoWriter(str(pathvO), cv2.VideoWriter_fourcc(*'XVID'), 10, (640, 480))
    
    start_time = datetime.now()
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            try:
                landmarks = results.pose_landmarks.landmark
                # Seleccionar función de ángulo según plano
                if plano == 'xy':
                    [allangle, _] = angulosxy(image, mp_pose, landmarks, allangle, start_time)
                elif plano == 'xz':
                    [allangle, _] = angulosxz(image, mp_pose, landmarks, allangle, start_time)
                elif plano == 'zy':
                    [allangle, _] = anguloszy(image, mp_pose, landmarks, allangle, start_time)
            except:
                pass
            
            # Dibujar landmarks
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
            )
            
            cv2.imshow('Mediapipe Feed', image)
            salida.write(image)
            original.write(frame)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    
    cap.release()
    salida.release()
    original.release()
    cv2.destroyAllWindows()
    
    # Guardar ángulos
    df2 = pd.DataFrame(allangle)
    df2.to_excel(str(pathvA))
    print(f"Video guardado en {pathvM}")
    print(f"Ángulos guardados en {pathvA}")

def obtener_datosxy():
    obtener_datos_plano('xy')

def obtener_datosxz():
    obtener_datos_plano('xz')

def obtener_datoszy():
    obtener_datos_plano('zy')

# ================= FUNCIONES DE PROCESAMIENTO DE ARCHIVOS =================
def procesar_video_plano(plano: str, archivo_video: str):
    """Procesa un archivo de video en un plano específico"""
    global XY_AC, XY_DEG, XZ_AC, XZ_DEG, ZY_AC, ZY_DEG
    
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    
    cap = cv2.VideoCapture(archivo_video)
    
    # Configurar rutas
    dirc = PROJECT_ROOT
    doko = REGISTROS / plano / "angulosmediapipe"
    doko.mkdir(parents=True, exist_ok=True)
    
    [namemediapipe, namemeoriginal, nameangle, namedat] = sailor(str(doko), 0, 0)
    
    pathvA = REGISTROS / plano / "angulosmediapipe" / nameangle
    pathvD = REGISTROS / plano / "datosmediapipe" / namedat
    
    allangle = []
    start_time = datetime.now()
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            try:
                landmarks = results.pose_landmarks.landmark
                if plano == 'xy':
                    [allangle, _] = angulosxy(image, mp_pose, landmarks, allangle, start_time)
                elif plano == 'xz':
                    [allangle, _] = angulosxz(image, mp_pose, landmarks, allangle, start_time)
                elif plano == 'zy':
                    [allangle, _] = anguloszy(image, mp_pose, landmarks, allangle, start_time)
            except:
                pass
            
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
            )
            
            cv2.imshow(f'Mediapipe Feed - {plano}', image)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Guardar datos
    df2 = pd.DataFrame(allangle)
    df2.to_excel(str(pathvA))
    
    # Calcular aceleración
    dfdev = df2.diff()
    acang = pd.DataFrame()
    acang[0] = dfdev[0]
    for i in range(1, 7):
        acang[i] = dfdev[i] / dfdev[0]
    
    Ac_ang = pd.DataFrame()
    Ac_ang[0] = df2[0]
    for i in range(1, 7):
        Ac_ang[i] = acang[i].diff() / dfdev[0]
    
    Ac_ang.to_excel(str(pathvD))
    
    # Actualizar variables globales
    df2.drop(df2.index[0:9], inplace=True)
    Ac_ang.drop(Ac_ang.index[0:9], inplace=True)
    
    if plano == 'xy':
        XY_DEG, XY_AC = df2, Ac_ang
    elif plano == 'xz':
        XZ_DEG, XZ_AC = df2, Ac_ang
    elif plano == 'zy':
        ZY_DEG, ZY_AC = df2, Ac_ang
    
    # Generar gráficos
    da = REGISTROS / plano / 'grafica_angulos_tiempo'
    dg = REGISTROS / plano / 'grafica_aceleracion_tiempo'
    [acel, acelplace] = figname(str(dg), 'aceleracion.png')
    [angl, anglplace] = figname(str(da), 'angulos.png')
    
    grafangle(df2, f'Ángulos en plano {plano}', str(da / angl))
    grafangle(Ac_ang, f'Aceleración en plano {plano}', str(dg / acel))
    
    # Mover archivos
    shutil.move(acel, acelplace)
    archi(acel)
    shutil.move(angl, anglplace)
    archi(angl)
    
    return df2, Ac_ang

def vid_obtener_datosxy():
    global filename
    if filename:
        procesar_video_plano('xy', filename)

def vid_obtener_datosxz():
    global filename
    if filename:
        procesar_video_plano('xz', filename)

def vid_obtener_datoszy():
    global filename
    if filename:
        procesar_video_plano('zy', filename)

def cargar_video():
    """Carga un video para procesar"""
    global filename
    filename = filedialog.askopenfilename(
        title="Seleccionar video",
        filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")]
    )
    if filename:
        vid_obtener_datosxy()
        vid_obtener_datosxz()
        vid_obtener_datoszy()
        print(f"Video {filename} procesado completamente")

def video_lento():
    """Procesa un video en cámara lenta"""
    global filename
    filename = filedialog.askopenfilename(
        title="Seleccionar video para cámara lenta",
        filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
    )
    if filename:
        video = VideoFileClip(filename).fx(vfx.speedx, 0.5)
        slow_file = "lento_temp.mp4"
        video.write_videofile(slow_file)
        filename = slow_file
        cargar_video()
        os.remove(slow_file) if os.path.exists(slow_file) else None

def Multiple_vid_normal():
    """Procesa múltiples videos"""
    global filename
    filez = filedialog.askopenfilenames(
        multiple=True,
        title='Seleccionar videos',
        filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
    )
    
    if filez:
        with open("archivo.txt", "w") as archivo:
            archivo.write(str(list(filez)))
        
        for f in filez:
            print(f'Procesando: {f}')
            filename = f
            cargar_video()
        
        shutil.move("archivo.txt", str(REGISTROS / "archivo.txt"))
        print("Todos los videos procesados")