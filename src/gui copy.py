# src/gui.py
import tkinter as tk
from tkinter import Tk, Label, Button, Menu, Frame, StringVar
from tkinter.font import Font
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Verificar si ttkbootstrap está instalado, sino usar tkinter estándar
try:
    from ttkbootstrap import Style
    HAS_TTKBOOTSTRAP = True
except ImportError:
    HAS_TTKBOOTSTRAP = False
    print("ttkbootstrap no está instalado. Usando tkinter estándar.")

from video import (
    iniciar,
    finalizar,
    obtener_datosxy,
    obtener_datosxz,
    obtener_datoszy,
    video_lento,
    Multiple_vid_normal,
    cargar_video
)
from io_module import create_files, mover_carpt
from sensors import get_sensor_var
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

# En src/gui.py, añade esto cerca del inicio:
try:
    from grpc.client import create_client
    
    class GRPCEnhancedGUI:
        def __init__(self, root):
            self.root = root
            self.grpc_client = None
            
            try:
                self.grpc_client = create_client('localhost:50051')
                print("✅ Conectado al servidor gRPC")
            except:
                print("⚠️ No se pudo conectar al servidor gRPC")
                print("   Ejecuta: python run_server.py")
            
            # Modificar botones existentes para usar gRPC
            self._enhance_buttons()
        
        def _enhance_buttons(self):
            """Reemplaza comandos de botones para usar gRPC"""
            # Encuentra y modifica botones específicos
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Button):
                    text = widget.cget("text")
                    
                    if "Cargar video" in text and self.grpc_client:
                        # Mantén el comando original pero añade gRPC
                        original_cmd = widget.cget("command")
                        widget.config(command=lambda: self._load_video_grpc(original_cmd))
                    
                    if "Iniciar cámara" in text and self.grpc_client:
                        original_cmd = widget.cget("command")
                        widget.config(command=lambda: self._start_camera_grpc(original_cmd))
        
        def _load_video_grpc(self, original_command):
            """Carga video usando gRPC + comando original"""
            from tkinter import filedialog
            file_path = filedialog.askopenfilename()
            
            if file_path and self.grpc_client:
                # Procesar via gRPC
                result = self.grpc_client.process_video_file(file_path)
                
                if result and result.success:
                    print(f"✅ Video procesado via gRPC: {result.total_frames} frames")
                else:
                    print("❌ Error procesando via gRPC, usando método local")
                    # Ejecutar comando original como fallback
                    if original_command:
                        original_command()
            elif original_command:
                # Fallback a método local
                original_command()
    
    # En tu función build_main_window(), envuelve la GUI:
    def build_main_window_grpc():
        root = tk.Tk()
        # ... tu configuración actual de la GUI ...
        
        # Crear la versión mejorada con gRPC
        enhanced_gui = GRPCEnhancedGUI(root)
        
        return root

except ImportError:
    print("⚠️ Módulos gRPC no disponibles, usando GUI normal")
    # Usa tu GUI normal sin cambios

def build_main_window():
    create_files()
    
    if HAS_TTKBOOTSTRAP:
        style = Style(theme='cosmo')  # Puedes cambiar a 'flatly', 'darkly', etc.
        root = style.master
    else:
        root = Tk()
    
    root.title("Tesis Maestría: Obtención de Datos de Movimiento")
    root.geometry("1200x700")
    root.resizable(False, False)
    
    if not HAS_TTKBOOTSTRAP:
        root.config(bg='#f0f0f0')
    
    # Fuentes personalizadas
    title_font = ("Arial", 16, "bold")
    section_font = ("Arial", 12, "bold")
    button_font = ("Arial", 10)
    
    # ================== FRAME PRINCIPAL ==================
    main_frame = Frame(root)
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Configurar grid para expansión
    for i in range(10):
        main_frame.grid_rowconfigure(i, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=3)  # Más peso para el video
    
    if not HAS_TTKBOOTSTRAP:
        main_frame.config(bg='#f0f0f0')
    
    # ================== TÍTULO PRINCIPAL ==================
    title_label = Label(main_frame, text="Sistema de Análisis de Movimiento", 
                       font=title_font)
    title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky='n')
    
    if not HAS_TTKBOOTSTRAP:
        title_label.config(bg='#f0f0f0')
    
    # ================== MENÚ SUPERIOR ==================
    if HAS_TTKBOOTSTRAP:
        menubar = Menu(root)
    else:
        menubar = Menu(root, bg='#e0e0e0', fg='black')
    
    menu_archivo = Menu(menubar, tearoff=0)
    menu_archivo.add_command(label="Mover carpeta Registros", command=mover_carpt)
    menu_archivo.add_separator()
    menu_archivo.add_command(label="Salir", command=root.quit)
    menubar.add_cascade(label="Archivo", menu=menu_archivo)
    
    root.config(menu=menubar)
    
    # ================== PANEL IZQUIERDO (CONTROLES) ==================
    left_panel = Frame(main_frame)
    left_panel.grid(row=1, column=0, columnspan=2, rowspan=9, 
                    padx=(0, 20), pady=5, sticky='nsew')
    
    if not HAS_TTKBOOTSTRAP:
        left_panel.config(bg='#f0f0f0')
    
    # Configurar grid del panel izquierdo
    for i in range(12):
        left_panel.grid_rowconfigure(i, weight=1)
    left_panel.grid_columnconfigure(0, weight=1)
    left_panel.grid_columnconfigure(1, weight=1)
    
    # ================== SECCIÓN CÁMARA ==================
    cam_frame = Frame(left_panel)
    cam_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky='ew')
    
    if not HAS_TTKBOOTSTRAP:
        cam_frame.config(bg='#ffffff', relief='ridge', bd=2)
    
    Label(cam_frame, text="Control de Cámara", 
          font=section_font).pack(pady=(10, 5))
    
    # Botones de cámara en un frame para mejor alineación
    cam_buttons = Frame(cam_frame)
    cam_buttons.pack(pady=(0, 10))
    
    if HAS_TTKBOOTSTRAP:
        btnIniciar = ttk.Button(cam_buttons, text="Iniciar Cámara", 
                               width=20, bootstyle=PRIMARY,
                               command=lambda: iniciar(lblVideo, 0))
        btnFinalizar = ttk.Button(cam_buttons, text="Finalizar Cámara", 
                                 width=20, bootstyle=SECONDARY,
                                 command=finalizar)
    else:
        btnIniciar = Button(cam_buttons, text="Iniciar Cámara", 
                           width=20, height=2, font=button_font,
                           bg='#4CAF50', fg='white', activebackground='#45a049')
        btnIniciar.config(command=lambda: iniciar(lblVideo, 0))
        
        btnFinalizar = Button(cam_buttons, text="Finalizar Cámara", 
                             width=20, height=2, font=button_font,
                             bg='#f44336', fg='white', activebackground='#d32f2f')
        btnFinalizar.config(command=finalizar)
    
    btnIniciar.pack(side='left', padx=5)
    btnFinalizar.pack(side='left', padx=5)
    
    # ================== SECCIÓN REGISTRO INDIVIDUAL ==================
    reg_frame = Frame(left_panel)
    reg_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky='ew')
    
    if not HAS_TTKBOOTSTRAP:
        reg_frame.config(bg='#ffffff', relief='ridge', bd=2)
    
    Label(reg_frame, text="Registro desde Cámara", 
          font=section_font).pack(pady=(10, 5))
    
    # Frame para botones de registro
    reg_buttons = Frame(reg_frame)
    reg_buttons.pack(pady=(0, 10))
    
    # Crear botones de registro
    if HAS_TTKBOOTSTRAP:
        buttons = [
            ("Registro XY", obtener_datosxy, PRIMARY),
            ("Registro XZ", obtener_datosxz, PRIMARY),
            ("Registro ZY", obtener_datoszy, PRIMARY)
        ]
        
        for i, (text, command, style) in enumerate(buttons):
            row, col = divmod(i, 2)
            btn = ttk.Button(reg_buttons, text=text, width=18, 
                            bootstyle=style, command=command)
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            reg_buttons.grid_columnconfigure(col, weight=1)
    else:
        buttons = [
            ("Registro XY", obtener_datosxy, '#2196F3'),
            ("Registro XZ", obtener_datosxz, '#2196F3'),
            ("Registro ZY", obtener_datoszy, '#2196F3')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            row, col = divmod(i, 2)
            btn = Button(reg_buttons, text=text, width=18, height=2, 
                        font=button_font, bg=color, fg='white',
                        activebackground='#1976D2')
            btn.config(command=command)
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            reg_buttons.grid_columnconfigure(col, weight=1)
    
    # ================== SECCIÓN PROCESAR VIDEO ==================
    video_frame = Frame(left_panel)
    video_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky='ew')
    
    if not HAS_TTKBOOTSTRAP:
        video_frame.config(bg='#ffffff', relief='ridge', bd=2)
    
    Label(video_frame, text="Procesar Archivos de Video", 
          font=section_font).pack(pady=(10, 5))
    
    # Frame para botones de video
    video_buttons = Frame(video_frame)
    video_buttons.pack(pady=(0, 10))
    
    if HAS_TTKBOOTSTRAP:
        vid_buttons = [
            ("Cargar Video", cargar_video, INFO),
            ("Video Lento", video_lento, WARNING),
            ("Múltiples Videos", Multiple_vid_normal, SUCCESS)
        ]
        
        for i, (text, command, style) in enumerate(vid_buttons):
            btn = ttk.Button(video_buttons, text=text, width=25, 
                            bootstyle=style, command=command)
            btn.pack(pady=3, padx=20, fill='x')
    else:
        vid_buttons = [
            ("Cargar Video", cargar_video, '#9C27B0'),
            ("Video Lento", video_lento, '#FF9800'),
            ("Múltiples Videos", Multiple_vid_normal, '#4CAF50')
        ]
        
        for text, command, color in vid_buttons:
            btn = Button(video_buttons, text=text, width=25, height=2,
                        font=button_font, bg=color, fg='white',
                        activebackground={'#9C27B0': '#7B1FA2',
                                         '#FF9800': '#F57C00',
                                         '#4CAF50': '#388E3C'}[color])
            btn.config(command=command)
            btn.pack(pady=3, padx=20, fill='x')
    
    # ================== SECCIÓN SENSORES ==================
    sensor_frame = Frame(left_panel)
    sensor_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky='ew')
    
    if not HAS_TTKBOOTSTRAP:
        sensor_frame.config(bg='#ffffff', relief='ridge', bd=2)
    
    Label(sensor_frame, text="Procesar Datos de Sensores", 
          font=section_font).pack(pady=(10, 5))
    
    if HAS_TTKBOOTSTRAP:
        btnSensores = ttk.Button(sensor_frame, text="Cargar Sensores (CSV)", 
                                width=25, bootstyle=DARK,
                                command=get_sensor_var)
    else:
        btnSensores = Button(sensor_frame, text="Cargar Sensores (CSV)", 
                            width=25, height=2, font=button_font,
                            bg='#607D8B', fg='white', 
                            activebackground='#455A64')
        btnSensores.config(command=get_sensor_var)
    
    btnSensores.pack(pady=(0, 10))
    
    # ================== PANEL DERECHO (VIDEO) ==================
    right_panel = Frame(main_frame)
    right_panel.grid(row=1, column=2, rowspan=9, padx=(20, 0), pady=5, sticky='nsew')
    
    # Configurar expansión del panel derecho
    right_panel.grid_rowconfigure(0, weight=1)
    right_panel.grid_columnconfigure(0, weight=1)
    
    # Frame para el video con borde
    video_display_frame = Frame(right_panel)
    video_display_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    
    if not HAS_TTKBOOTSTRAP:
        video_display_frame.config(bg='black', relief='sunken', bd=3)
    
    # Label para mostrar el video (centrado)
    lblVideo = Label(video_display_frame, bg='black')
    lblVideo.place(relx=0.5, rely=0.5, anchor='center')
    
    # Etiqueta de estado del video (solo se muestra cuando no hay video)
    video_status = StringVar()
    video_status.set("Cámara no iniciada")
    
    if not HAS_TTKBOOTSTRAP:
        status_label = Label(video_display_frame, textvariable=video_status,
                            bg='black', fg='white', font=("Arial", 10))
        status_label.place(relx=0.5, rely=0.5, anchor='center')
    
    # Función para actualizar estado
    def update_video_status(status):
        video_status.set(status)
        if status == "Mostrando video":
            if not HAS_TTKBOOTSTRAP and 'status_label' in locals():
                status_label.place_forget()
        else:
            if not HAS_TTKBOOTSTRAP and 'status_label' in locals():
                status_label.place(relx=0.5, rely=0.5, anchor='center')
    
    # Modificar la función iniciar para actualizar estado
    original_iniciar = iniciar
    def iniciar_con_estado(label_widget, cam_index):
        update_video_status("Iniciando cámara...")
        original_iniciar(label_widget, cam_index)
        update_video_status("Mostrando video")
    
    # Sobrescribir la función
    import sys
    sys.modules[__name__].iniciar = iniciar_con_estado
    
    # ================== BARRA DE ESTADO ==================
    status_bar = Frame(root)
    status_bar.pack(side='bottom', fill='x')
    
    if not HAS_TTKBOOTSTRAP:
        status_bar.config(bg='#e0e0e0', height=20)
    
    status_text = StringVar()
    status_text.set("Listo")
    
    if HAS_TTKBOOTSTRAP:
        status_label = ttk.Label(status_bar, textvariable=status_text, 
                                bootstyle=INVERSE)
    else:
        status_label = Label(status_bar, textvariable=status_text,
                            bg='#e0e0e0', fg='black', anchor='w')
    
    status_label.pack(side='left', padx=10)
    
    # ================== CENTRAR VENTANA ==================
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    return root

if __name__ == "__main__":
    app = build_main_window()
    app.mainloop()