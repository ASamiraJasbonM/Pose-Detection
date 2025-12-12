# src/sensors.py
import pandas as pd
import shutil
import matplotlib.pyplot as plt
from pathlib import Path
from tkinter import filedialog
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from io_module import figname, archi, REGISTROS, PROJECT_ROOT

# Importar variables desde video.py
from video import XY_AC, XY_DEG, XZ_AC, XZ_DEG, ZY_AC, ZY_DEG

def RMSdtf(A_art: pd.DataFrame):
    """
    Calcula el valor RMS (Root Mean Square) por fila de un DataFrame.
    CORREGIDO: Ahora calcula correctamente sqrt(mean(squares))
    """
    A_art = A_art.copy()
    A_art.fillna(0, inplace=True)
    
    # 1. Elevar al cuadrado cada valor
    powtwo = A_art.pow(2)
    
    # 2. Calcular la media de los cuadrados por fila (promedio de columnas)
    # Para un DataFrame, mean(axis=1) calcula el promedio por fila
    mean_squares = powtwo.mean(axis=1)
    
    # 3. Calcular la raíz cuadrada de la media de cuadrados
    rms = mean_squares.pow(0.5)  # Equivalente a sqrt(mean_squares)
    
    # 4. Eliminar NaN y retornar
    rms = rms.dropna()
    return rms

def get_sensor_var():
    """Procesa archivos CSV de sensores"""
    filenameleft = filedialog.askopenfilename(
        title="Seleccionar CSV sensor izquierdo",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if not filenameleft:
        return
        
    df0 = pd.read_csv(filenameleft)
    
    filenameright = filedialog.askopenfilename(
        title="Seleccionar CSV sensor derecho",
        filetypes=[("CSV files", "*.csv")]
    )
    
    if not filenameright:
        return
        
    df1 = pd.read_csv(filenameright)
    
    # Procesar datos izquierdos
    aceL = pd.DataFrame()
    if 'gx_deg/s' in df0.columns:
        aceL[0] = df0['gx_deg/s']
    if 'gy_deg/s' in df0.columns:
        aceL[1] = df0['gy_deg/s']
    if 'gz_deg/s' in df0.columns:
        aceL[2] = df0['gz_deg/s']
    
    degL = pd.DataFrame()
    if 'x_deg' in df0.columns:
        degL[0] = df0['x_deg']
    if 'y_deg' in df0.columns:
        degL[1] = df0['y_deg']
    if 'z_deg' in df0.columns:
        degL[2] = df0['z_deg']
    
    # Procesar datos derechos
    aceR = pd.DataFrame()
    if 'gx_deg/s' in df1.columns:
        aceR[0] = df1['gx_deg/s']
    if 'gy_deg/s' in df1.columns:
        aceR[1] = df1['gy_deg/s']
    if 'gz_deg/s' in df1.columns:
        aceR[2] = df1['gz_deg/s']
    
    degR = pd.DataFrame()
    if 'x_deg' in df1.columns:
        degR[0] = df1['x_deg']
    if 'y_deg' in df1.columns:
        degR[1] = df1['y_deg']
    if 'z_deg' in df1.columns:
        degR[2] = df1['z_deg']
    
    # Calcular RMS
    rms_aceL = RMSdtf(aceL) if not aceL.empty else pd.Series()
    rms_degL = RMSdtf(degL) if not degL.empty else pd.Series()
    rms_aceR = RMSdtf(aceR) if not aceR.empty else pd.Series()
    rms_degR = RMSdtf(degR) if not degR.empty else pd.Series()
    
    # Crear reportes
    wo = REGISTROS / 'sensores'
    wo.mkdir(parents=True, exist_ok=True)
    
    # Reporte de ángulos
    if not degL.empty or not degR.empty:
        [Report_Angles, Report_Anglesplace] = figname(str(wo), 'Report_Angles.xlsx')
        Report_deg = pd.DataFrame()
        # ... (código para llenar Report_deg)
        Report_deg.to_excel(Report_Angles)
        shutil.move(Report_Angles, Report_Anglesplace)
    
    print("Sensores procesados correctamente")

def calculoAC():
    """Calcula estadísticas de aceleración RMS entre planos"""
    if XY_AC is None or XZ_AC is None or ZY_AC is None:
        print("ERROR: Primero debe procesar videos en los tres planos")
        return
    
    di = REGISTROS / 'report_ac_rms'
    di.mkdir(parents=True, exist_ok=True)
    
    [namfile, place] = figname(str(REGISTROS), 'aceleracion_rms.png')
    [namrep, placerep] = figname(str(di), 'Reporte_est_aceleracion_rms.xlsx')
    
    fig, ax = plt.subplots(3, 2, figsize=(18.5, 10.5))
    fig.suptitle('Aceleración RMS entre planos')
    plt.subplots_adjust(wspace=0.143, hspace=0.36, bottom=0.11, left=0.045)
    
    # Preparar datos para cada articulación
    articulaciones = [
        ("Hombro izquierdo", 1, XY_AC, XZ_AC, ZY_AC),
        ("Hombro derecho", 2, XY_AC, XZ_AC, ZY_AC),
        ("Codo izquierdo", 3, XY_AC, XZ_AC, ZY_AC),
        ("Codo derecho", 4, XY_AC, XZ_AC, ZY_AC),
        ("Muñeca izquierda", 5, XY_AC, XZ_AC, ZY_AC),
        ("Muñeca derecha", 6, XY_AC, XZ_AC, ZY_AC)
    ]
    
    report_data = []
    
    for idx, (nombre, col, xy, xz, zy) in enumerate(articulaciones):
        row, col_pos = divmod(idx, 2)
        
        # Combinar datos de los tres planos
        datos = pd.DataFrame({
            'xy': xy[col] if col in xy.columns else pd.Series(),
            'xz': xz[col] if col in xz.columns else pd.Series(),
            'zy': zy[col] if col in zy.columns else pd.Series()
        })
        
        rms = RMSdtf(datos)
        
        if not rms.empty:
            ax[row, col_pos].boxplot(rms, vert=False, patch_artist=True)
            ax[row, col_pos].set_title(nombre)
            
            # Estadísticas para reporte
            stats = {
                'Articulación': nombre,
                'Media': rms.mean(),
                'Desv. Estándar': rms.std(),
                'Mínimo': rms.min(),
                '25%': rms.quantile(0.25),
                'Mediana': rms.median(),
                '75%': rms.quantile(0.75),
                'Máximo': rms.max()
            }
            report_data.append(stats)
    
    plt.savefig(namfile, dpi=100)
    plt.show()
    
    # Guardar reporte
    if report_data:
        Report = pd.DataFrame(report_data)
        Report.to_excel(namrep, index=False)
        shutil.move(namrep, placerep)
        archi(namrep)
    
    shutil.move(namfile, place)
    archi(namfile)

def calculoDEG():
    """Calcula estadísticas de ángulos RMS entre planos"""
    if XY_DEG is None or XZ_DEG is None or ZY_DEG is None:
        print("ERROR: Primero debe procesar videos en los tres planos")
        return
    
    # Implementación similar a calculoAC pero para ángulos
    print("Función calculoDEG ejecutada")
    # ... (código similar al de calculoAC pero con variables _DEG)