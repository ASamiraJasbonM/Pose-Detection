# src/gui.py
import tkinter as tk
from tkinter import Tk, Label, Button, Menu, Frame, StringVar
from tkinter.font import Font
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import sys

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Verificar si ttkbootstrap está instalado
try:
    from ttkbootstrap import Style
    HAS_TTKBOOTSTRAP = True
except ImportError:
    HAS_TTKBOOTSTRAP = False
    print("ttkbootstrap no está instalado. Usando tkinter estándar.")

# Importar tus módulos existentes
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

# Intentar importar gRPC para mejorar la GUI
GRPC_AVAILABLE = False
GRPC_CLIENT = None

try:
    from src.grpc.client import create_client
    GRPC_AVAILABLE = True
    print("✅ Módulos gRPC disponibles")
except ImportError as e:
    print(f"⚠️ Módulos gRPC no disponibles: {e}")
    print("   La GUI funcionará en modo local sin gRPC")

# Crear cliente gRPC si está disponible
if GRPC_AVAILABLE:
    try:
        GRPC_CLIENT = create_client('localhost:50051')
        print("✅ Cliente gRPC conectado al servidor")
    except Exception as e:
        print(f"⚠️ No se pudo conectar al servidor gRPC: {e}")
        print("   Ejecuta: python run_server.py para habilitar gRPC")
        GRPC_CLIENT = None

class GRPCEnhancedGUI:
    """Clase que mejora la GUI existente con funcionalidad gRPC"""
    
    def __init__(self, root, grpc_client=None):
        self.root = root
        self.grpc_client = grpc_client
        self.original_commands = {}  # Para almacenar comandos originales
        
        if self.grpc_client:
            print("🎯 GUI mejorada con gRPC activada")
            self._enhance_buttons()
    
    def _enhance_buttons(self):
        """Mejora los botones existentes para usar gRPC cuando sea posible"""
        print("🔧 Mejorando botones con funcionalidad gRPC...")
        
        # Buscar todos los botones en la GUI
        def find_buttons(widget):
            buttons = []
            if isinstance(widget, tk.Button) or (HAS_TTKBOOTSTRAP and isinstance(widget, ttk.Button)):
                buttons.append(widget)
            
            # Buscar recursivamente en hijos
            for child in widget.winfo_children():
                buttons.extend(find_buttons(child))
            
            return buttons
        
        all_buttons = find_buttons(self.root)
        
        for btn in all_buttons:
            try:
                btn_text = btn.cget("text")
                original_cmd = btn.cget("command")
                
                # Guardar comando original
                self.original_commands[btn] = original_cmd
                
                # Mejorar botones específicos
                if "Cargar Video" in btn_text:
                    btn.config(command=lambda b=btn: self._load_video_grpc(b))
                    print(f"   ✓ Botón 'Cargar Video' mejorado con gRPC")
                
                elif "Video Lento" in btn_text:
                    btn.config(command=lambda b=btn: self._process_slow_video_grpc(b))
                    print(f"   ✓ Botón 'Video Lento' mejorado con gRPC")
                
                elif "Múltiples Videos" in btn_text:
                    btn.config(command=lambda b=btn: self._process_multiple_videos_grpc(b))
                    print(f"   ✓ Botón 'Múltiples Videos' mejorado con gRPC")
                    
            except Exception as e:
                print(f"   ⚠️ Error mejorando botón: {e}")
    
    def _load_video_grpc(self, button):
        """Procesa video usando gRPC o fallback a local"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Seleccionar video",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        # Actualizar estado en la GUI
        self._update_status("Procesando video via gRPC...")
        
        if self.grpc_client:
            try:
                print(f"📤 Enviando {file_path} al servidor gRPC...")
                
                # Procesar via gRPC
                result = self.grpc_client.process_video_file(file_path)
                
                if result and result.success:
                    self._update_status(f"✅ Video procesado: {result.total_frames} frames")
                    self._show_success_message(
                        f"Video procesado exitosamente via gRPC\n"
                        f"Frames: {result.total_frames}\n"
                        f"Ángulo medio: {result.statistics.mean_angle_xy:.1f}°"
                    )
                    return
                else:
                    error_msg = result.error_message if result else "Error desconocido"
                    print(f"❌ Error en servidor gRPC: {error_msg}")
                    
            except Exception as e:
                print(f"❌ Error gRPC: {e}")
        
        # Fallback a procesamiento local
        self._update_status("Usando procesamiento local...")
        print("🔄 Fallback a procesamiento local")
        
        # Ejecutar comando original (método local)
        original_cmd = self.original_commands.get(button)
        if original_cmd:
            original_cmd()
    
    def _process_slow_video_grpc(self, button):
        """Procesa video lento usando gRPC o fallback a local"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Seleccionar video para cámara lenta",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
        )
        
        if not file_path:
            return
        
        self._update_status("Procesando video lento via gRPC...")
        
        if self.grpc_client:
            try:
                # En una implementación real, necesitarías un método específico para video lento
                # Por ahora usamos el mismo método pero con modo diferente
                result = self.grpc_client.process_video_file(file_path)
                
                if result and result.success:
                    self._update_status(f"✅ Video lento procesado: {result.total_frames} frames")
                    return
                    
            except Exception as e:
                print(f"❌ Error gRPC video lento: {e}")
        
        # Fallback a procesamiento local
        self._update_status("Usando procesamiento local para video lento...")
        original_cmd = self.original_commands.get(button)
        if original_cmd:
            original_cmd()
    
    def _process_multiple_videos_grpc(self, button):
        """Procesa múltiples videos usando gRPC"""
        from tkinter import filedialog
        
        file_paths = filedialog.askopenfilenames(
            title="Seleccionar múltiples videos",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
        )
        
        if not file_paths:
            return
        
        self._update_status(f"Procesando {len(file_paths)} videos via gRPC...")
        
        if self.grpc_client:
            success_count = 0
            for i, file_path in enumerate(file_paths, 1):
                try:
                    result = self.grpc_client.process_video_file(file_path)
                    if result and result.success:
                        success_count += 1
                        print(f"   ✅ ({i}/{len(file_paths)}) {os.path.basename(file_path)}")
                    else:
                        print(f"   ❌ ({i}/{len(file_paths)}) {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"   ❌ ({i}/{len(file_paths)}) Error: {e}")
            
            self._update_status(f"✅ {success_count}/{len(file_paths)} videos procesados via gRPC")
            
            if success_count < len(file_paths):
                # Algunos fallaron, preguntar si usar método local
                self._show_warning_message(
                    f"{len(file_paths) - success_count} videos fallaron con gRPC\n"
                    f"¿Desea procesarlos localmente?"
                )
        
        # Fallback a procesamiento local
        original_cmd = self.original_commands.get(button)
        if original_cmd:
            self._update_status("Usando procesamiento local para videos restantes...")
            original_cmd()
    
    def _update_status(self, message):
        """Actualiza la barra de estado"""
        # Buscar la barra de estado en la GUI
        for widget in self.root.winfo_children():
            if isinstance(widget, Frame) and widget.winfo_name() == "status_bar":
                for child in widget.winfo_children():
                    if isinstance(child, (Label, ttk.Label)):
                        if hasattr(child, 'config'):
                            child.config(text=message)
                        break
                break
        print(f"📢 Estado: {message}")
    
    def _show_success_message(self, message):
        """Muestra mensaje de éxito"""
        # En una implementación real, usarías un messagebox o un label especial
        print(f"🎉 {message}")
    
    def _show_warning_message(self, message):
        """Muestra mensaje de advertencia"""
        print(f"⚠️  {message}")

def build_main_window():
    """Función principal para construir la ventana principal"""
    create_files()
    
    # Crear ventana principal
    if HAS_TTKBOOTSTRAP:
        style = Style(theme='cosmo')
        root = style.master
    else:
        root = Tk()
    
    root.title("Tesis Maestría: Obtención de Datos de Movimiento (gRPC Enhanced)")
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
    main_frame.grid_columnconfigure(2, weight=3)
    
    if not HAS_TTKBOOTSTRAP:
        main_frame.config(bg='#f0f0f0')
    
    # ================== TÍTULO PRINCIPAL ==================
    title_text = "Sistema de Análisis de Movimiento"
    if GRPC_CLIENT:
        title_text += " (gRPC Activado)"
    
    title_label = Label(main_frame, text=title_text, font=title_font)
    title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky='n')
    
    if not HAS_TTKBOOTSTRAP:
        title_label.config(bg='#f0f0f0')
    
    # Indicador de estado gRPC
    if GRPC_CLIENT:
        grpc_status = Label(main_frame, text="✅ gRPC CONECTADO", 
                           font=("Arial", 10), fg='green')
        grpc_status.grid(row=0, column=2, pady=(0, 20), sticky='ne')
    
    # ================== MENÚ SUPERIOR ==================
    menubar = Menu(root)
    
    menu_archivo = Menu(menubar, tearoff=0)
    menu_archivo.add_command(label="Mover carpeta Registros", command=mover_carpt)
    
    # Añadir opción gRPC si está disponible
    if GRPC_CLIENT:
        menu_archivo.add_command(label="Probar conexión gRPC", 
                               command=lambda: test_grpc_connection())
    
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
    
    Label(cam_frame, text="Control de Cámara", font=section_font).pack(pady=(10, 5))
    
    cam_buttons = Frame(cam_frame)
    cam_buttons.pack(pady=(0, 10))
    
    # Botón Iniciar Cámara
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
                           bg='#4CAF50', fg='white', activebackground='#45a049',
                           command=lambda: iniciar(lblVideo, 0))
        
        btnFinalizar = Button(cam_buttons, text="Finalizar Cámara", 
                             width=20, height=2, font=button_font,
                             bg='#f44336', fg='white', activebackground='#d32f2f',
                             command=finalizar)
    
    btnIniciar.pack(side='left', padx=5)
    btnFinalizar.pack(side='left', padx=5)
    
    # ================== SECCIÓN REGISTRO INDIVIDUAL ==================
    reg_frame = Frame(left_panel)
    reg_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky='ew')
    
    if not HAS_TTKBOOTSTRAP:
        reg_frame.config(bg='#ffffff', relief='ridge', bd=2)
    
    Label(reg_frame, text="Registro desde Cámara", font=section_font).pack(pady=(10, 5))
    
    reg_buttons = Frame(reg_frame)
    reg_buttons.pack(pady=(0, 10))
    
    # Botones de registro
    buttons = [
        ("Registro XY", obtener_datosxy),
        ("Registro XZ", obtener_datosxz),
        ("Registro ZY", obtener_datoszy)
    ]
    
    for i, (text, command) in enumerate(buttons):
        row, col = divmod(i, 2)
        
        if HAS_TTKBOOTSTRAP:
            btn = ttk.Button(reg_buttons, text=text, width=18, 
                            bootstyle=PRIMARY, command=command)
        else:
            btn = Button(reg_buttons, text=text, width=18, height=2,
                        font=button_font, bg='#2196F3', fg='white',
                        activebackground='#1976D2', command=command)
        
        btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        reg_buttons.grid_columnconfigure(col, weight=1)
    
    # ================== SECCIÓN PROCESAR VIDEO ==================
    video_frame = Frame(left_panel)
    video_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky='ew')
    
    if not HAS_TTKBOOTSTRAP:
        video_frame.config(bg='#ffffff', relief='ridge', bd=2)
    
    Label(video_frame, text="Procesar Archivos de Video", font=section_font).pack(pady=(10, 5))
    
    video_buttons = Frame(video_frame)
    video_buttons.pack(pady=(0, 10))
    
    # Botones de video
    vid_buttons = [
        ("Cargar Video", cargar_video),
        ("Video Lento", video_lento),
        ("Múltiples Videos", Multiple_vid_normal)
    ]
    
    styles = ['INFO', 'WARNING', 'SUCCESS'] if HAS_TTKBOOTSTRAP else ['#9C27B0', '#FF9800', '#4CAF50']
    
    for i, (text, command) in enumerate(vid_buttons):
        if HAS_TTKBOOTSTRAP:
            style = getattr(ttk, styles[i]) if hasattr(ttk, styles[i]) else 'INFO'
            btn = ttk.Button(video_buttons, text=text, width=25,
                            bootstyle=style, command=command)
        else:
            color = styles[i]
            btn = Button(video_buttons, text=text, width=25, height=2,
                        font=button_font, bg=color, fg='white',
                        activebackground={'#9C27B0': '#7B1FA2',
                                         '#FF9800': '#F57C00',
                                         '#4CAF50': '#388E3C'}[color],
                        command=command)
        btn.pack(pady=3, padx=20, fill='x')
    
    # ================== SECCIÓN SENSORES ==================
    sensor_frame = Frame(left_panel)
    sensor_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky='ew')
    
    if not HAS_TTKBOOTSTRAP:
        sensor_frame.config(bg='#ffffff', relief='ridge', bd=2)
    
    Label(sensor_frame, text="Procesar Datos de Sensores", font=section_font).pack(pady=(10, 5))
    
    if HAS_TTKBOOTSTRAP:
        btnSensores = ttk.Button(sensor_frame, text="Cargar Sensores (CSV)", 
                                width=25, bootstyle=DARK,
                                command=get_sensor_var)
    else:
        btnSensores = Button(sensor_frame, text="Cargar Sensores (CSV)", 
                            width=25, height=2, font=button_font,
                            bg='#607D8B', fg='white', 
                            activebackground='#455A64',
                            command=get_sensor_var)
    
    btnSensores.pack(pady=(0, 10))
    
    # ================== PANEL DERECHO (VIDEO) ==================
    right_panel = Frame(main_frame)
    right_panel.grid(row=1, column=2, rowspan=9, padx=(20, 0), pady=5, sticky='nsew')
    
    right_panel.grid_rowconfigure(0, weight=1)
    right_panel.grid_columnconfigure(0, weight=1)
    
    video_display_frame = Frame(right_panel)
    video_display_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    
    if not HAS_TTKBOOTSTRAP:
        video_display_frame.config(bg='black', relief='sunken', bd=3)
    
    # Label para mostrar el video
    lblVideo = Label(video_display_frame, bg='black')
    lblVideo.place(relx=0.5, rely=0.5, anchor='center')
    
    # Etiqueta de estado del video
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
    sys.modules[__name__].iniciar = iniciar_con_estado
    
    # ================== BARRA DE ESTADO ==================
    status_bar = Frame(root, name="status_bar")
    status_bar.pack(side='bottom', fill='x')
    
    if not HAS_TTKBOOTSTRAP:
        status_bar.config(bg='#e0e0e0', height=20)
    
    status_text = StringVar()
    status_text.set("Listo" + (" (gRPC disponible)" if GRPC_CLIENT else ""))
    
    if HAS_TTKBOOTSTRAP:
        status_label = ttk.Label(status_bar, textvariable=status_text, bootstyle=INVERSE)
    else:
        status_label = Label(status_bar, textvariable=status_text,
                            bg='#e0e0e0', fg='black', anchor='w')
    
    status_label.pack(side='left', padx=10)
    
    # ================== MEJORAR GUI CON gRPC ==================
    # Crear instancia de GRPCEnhancedGUI si gRPC está disponible
    enhanced_gui = None
    if GRPC_CLIENT:
        enhanced_gui = GRPCEnhancedGUI(root, GRPC_CLIENT)
    
    # ================== CENTRAR VENTANA ==================
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    return root

def test_grpc_connection():
    """Prueba la conexión gRPC"""
    if GRPC_CLIENT:
        try:
            # Probar con un cálculo simple
            landmarks = {
                "left_shoulder": {"x": 0.5, "y": 0.3, "z": 0.1},
                "left_elbow": {"x": 0.6, "y": 0.4, "z": 0.2},
                "left_wrist": {"x": 0.7, "y": 0.5, "z": 0.3},
            }
            
            result = GRPC_CLIENT.calculate_angles(landmarks)
            if result:
                print("✅ Conexión gRPC funcionando correctamente")
                return True
        except Exception as e:
            print(f"❌ Error en conexión gRPC: {e}")
    
    return False

if __name__ == "__main__":
    print("=" * 50)
    print("INICIANDO SISTEMA DE ANÁLISIS DE MOVIMIENTO")
    print("=" * 50)
    
    if GRPC_CLIENT:
        print("✅ Modo: GUI MEJORADA con gRPC")
    else:
        print("⚠️  Modo: GUI LOCAL (sin gRPC)")
        print("   Para activar gRPC, ejecuta en otra terminal:")
        print("   python run_server.py")
    
    app = build_main_window()
    app.mainloop()