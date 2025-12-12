# src/io.py (ya está bien estructurado)
import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path.cwd()
REGISTROS = PROJECT_ROOT / "Registros"

def neededfiles(dirc: str, names):
    for name in names:
        file_path = Path(dirc) / name
        file_path.mkdir(parents=True, exist_ok=True)

def archi(filename: str):
    f = PROJECT_ROOT / filename
    if f.exists():
        f.unlink()

def sailor(doko, op, whname=0):
    doko = Path(doko)
    initial_count = sum(1 for p in doko.iterdir() if p.is_file())
    Nvideo = max(0, initial_count - 1)
    
    if op == 0:
        namemediapipe = f'video{Nvideo}mediapipe.avi'
        namemeoriginal = f'video{Nvideo}original.avi'
        nameangle = f"angulos{Nvideo}.xlsx"
        namedat = f"videoact{Nvideo}.xlsx"
    else:
        namemediapipe = 'videomediapipe.avi'
        namemeoriginal = 'videooriginal.avi'
        nameangle = "angulos.xlsx"
        namedat = "videoact.xlsx"
    return [namemediapipe, namemeoriginal, nameangle, namedat]

def figname(direct: str, name: str):
    directp = Path(direct)
    initial_count = sum(1 for p in directp.iterdir() if p.is_file())
    N = initial_count
    namfile = f"{N}{name}"
    place = str(directp / namfile)
    return [namfile, place]

def mover_carpt():
    from tkinter import filedialog
    carp = filedialog.askdirectory()
    if carp:
        carpeta = Path(carp) / 'Registros'
        if REGISTROS.exists():
            shutil.move(str(REGISTROS), str(carpeta))
        create_files()

def create_files():
    neededfiles(str(PROJECT_ROOT), ['Registros'])
    dirc1 = REGISTROS
    neededfiles(str(dirc1), ["xy", "xz", "zy", "xyz", "sensores", "report_ac_rms", "report_deg_rms"])
    
    for plano in ["xy", "xz", "zy"]:
        dirc = dirc1 / plano
        neededfiles(str(dirc), ["datosmediapipe", 'video', "videoOriginal", 'angulosmediapipe', 
                               'grafica_angulos_tiempo', 'grafica_aceleracion_tiempo', 
                               'Report_angle_tiempo', 'Report_aceleracion_tiempo'])
    
    dircxyz = dirc1 / 'xyz'
    neededfiles(str(dircxyz), ["xy", "xz", "zy"])