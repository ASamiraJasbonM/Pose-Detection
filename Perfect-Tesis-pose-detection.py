from multiprocessing.resource_sharer import stop
import cv2
import mediapipe as mp
import numpy as np
import shutil
import pandas as pd
import sys
import time
import matplotlib
import matplotlib.pylab as plt
import os
from pathlib import Path
from os import path
from os import remove
from tkinter import *
from PIL import Image
from PIL import ImageTk
import imutils
import threading
from tkinter import filedialog
from datetime import datetime
import math
from sklearn.metrics import mean_squared_error
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video import fx as vfx

def neededfiles(dirc,names):
    for name in names:
        file=dirc+"/"+name
        path.exists(file)
        place=path.exists(file)
        if place==True:
            print('existe carpeta'+name)
        else:
            os.mkdir(file)
            print('Carpeta '+name+"creada")
        

def archi(filename):
    
    dirc=os.getcwd()
    file=dirc+'/'+filename
    if path.exists(file):
        remove(file)
        print('removido')


def sailor(doko, op, whname):
    initial_count = 0

    for path in os.listdir(doko):
        if os.path.isfile(os.path.join(doko, path)):
            initial_count += 1

    Nvideo=initial_count-1
    if op==0:
            
        namemediapipe='video'+ str(Nvideo)+'mediapipe'+'.avi'
        namemeoriginal='video'+ str(Nvideo)+'original'+'.avi'
        nameangle="angulos"+str(Nvideo)+".xlsx"
        namedat="videoact"+str(Nvideo)+".xlsx"
    if op==1:
            
        namemediapipe='videomediapipe.avi'
        namemeoriginal='videooriginal.avi'
        nameangle="angulos.xlsx"
        namedat="videoact.xlsx"

    return [namemediapipe,namemeoriginal,nameangle,namedat]

def nameanglexyz(doko, op):
 #   initial_count = 0

    #for path in os.listdir(doko):
     #   if os.path.isfile(os.path.join(doko, path)):
      #      initial_count += 1

#    Nvideo=initial_count-1
    if op==0:
            
        xy='angulos_xy'+ str(1)+".xlsx"
        xz='angulos_xz'+ str(1)+".xlsx"
        zy="angulos_zy"+str(1)+".xlsx"
    if op==1:
        xy="angulos_xy.xlsx"
        xz="angulos_xz.xlsx"
        zy="angulos_zy.xlsx"

    return [xy,xz,zy]

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def shouldvect(hip, should):
    #x=hip[0]+(should[0]-hip[0])# tonto
    x=should[0]# Se usa coordenada X de hombro paraque esté al msmo nivel
    y=hip[1]
    return (x,y)

def angulosxy(image,mp_pose, landmarks,allangle, start_time):

    hipL=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    shoulderL = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbowL = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wristL = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    indexl=[landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y]

    VLeft=shouldvect(hipL,shoulderL)
    
    hipR=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    shoulderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbowR = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    wristR = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    indexR=[landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y]

    VRight=shouldvect(hipR,shoulderR)
    Elz=[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    shlz=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    hlz=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

    # Calculate angle
    angl_sL = calculate_angle(VLeft,shoulderL, elbowL)
    angl_sR = calculate_angle(VRight,shoulderR, elbowR)
    angl_eL = calculate_angle(shoulderL, elbowL, wristL)
    angl_eR = calculate_angle(shoulderR, elbowR, wristR)
    angl_wL = calculate_angle(elbowR, wristR, indexR)
    angl_wR = calculate_angle(elbowL, wristL, indexl)
    end_time=datetime.now()
    time_dif= (end_time-start_time).total_seconds()
    
    # Visualize angle
    cv2.putText(image, str(round(angl_sL,2)), 
        tuple(np.multiply(shoulderL, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_sR,2)), 
        tuple(np.multiply(shoulderR, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_eL,2)), 
        tuple(np.multiply(elbowL, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_eR,2)), 
        tuple(np.multiply(elbowR, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_wL,2)), 
        tuple(np.multiply(wristL, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_wR,2)), 
        tuple(np.multiply(wristR, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(time_dif), 
        tuple(np.multiply([100,100], [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    angulosT=[time_dif,angl_sL,angl_sR, angl_eL, angl_eR, angl_wL, angl_wR]
    allangle.append(angulosT)
    
    return [allangle,time_dif]

def anguloszy(image,mp_pose, landmarks,allangle,start_time):

    hipL=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].z,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    shoulderL = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbowL = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wristL = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    indexl=[landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].z,landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y]

    hipLxy=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    shoulderLxy = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbowLxy = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wristLxy = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    indexlxy=[landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y]   

    hipR=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].z,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    shoulderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbowR = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    wristR = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].z,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    indexR=[landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].z,landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y]
    
    hipRxy=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    shoulderRxy = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbowRxy = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    wristRxy = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    indexRxy=[landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y]


    VLeft=shouldvect(hipL,shoulderL)
    VRight=shouldvect(hipR,shoulderR)

    # Calculate angle
    angl_sL = calculate_angle(VLeft,shoulderL, elbowL)
    angl_sR = calculate_angle(VRight,shoulderR, elbowR)
    angl_eL = calculate_angle(shoulderL, elbowL, wristL)
    angl_eR = calculate_angle(shoulderR, elbowR, wristR)
    angl_wL = calculate_angle(elbowR, wristR, indexR)
    angl_wR = calculate_angle(elbowL, wristL, indexl)

    # Visualize angle
    cv2.putText(image, str(round(angl_sL,2)), 
        tuple(np.multiply(shoulderLxy, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_sR,2)), 
        tuple(np.multiply(shoulderRxy, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_eL,2)), 
        tuple(np.multiply(elbowLxy, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_eR,2)), 
        tuple(np.multiply(elbowRxy, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_wL,2)), 
        tuple(np.multiply(wristLxy, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_wR,2)), 
        tuple(np.multiply(wristRxy, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    end_time=datetime.now()
    time_dif= (end_time-start_time).total_seconds()
    
    angulosT=[time_dif,angl_sL,angl_sR, angl_eL, angl_eR, angl_wL, angl_wR]
    allangle.append(angulosT)

    return [allangle,time_dif]
 
def angulosxz(image,mp_pose, landmarks,allangle,start_time):

    hipL=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].z]
    shoulderL = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z]
    elbowL = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z]
    wristL = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z]
    indexl=[landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].z]

    hipLxy=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    shoulderLxy = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbowLxy = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wristLxy = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    indexlxy=[landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y]   

    hipR=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].z]
    shoulderR = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z]
    elbowR = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z]
    wristR = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].z]
    indexR=[landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].z]
    
    hipRxy=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    shoulderRxy = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbowRxy = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    wristRxy = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    indexRxy=[landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y]


    VLeft=shouldvect(hipL,shoulderL)
    VRight=shouldvect(hipR,shoulderR)

    # Calculate angle
    angl_sL = calculate_angle(VLeft,shoulderL, elbowL)
    angl_sR = calculate_angle(VRight,shoulderR, elbowR)
    angl_eL = calculate_angle(shoulderL, elbowL, wristL)
    angl_eR = calculate_angle(shoulderR, elbowR, wristR)
    angl_wL = calculate_angle(elbowR, wristR, indexR)
    angl_wR = calculate_angle(elbowL, wristL, indexl)

    # Visualize angle
    cv2.putText(image, str(round(angl_sL,2)), 
        tuple(np.multiply(shoulderLxy, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_sR,2)), 
        tuple(np.multiply(shoulderRxy, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_eL,2)), 
        tuple(np.multiply(elbowLxy, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_eR,2)), 
        tuple(np.multiply(elbowRxy, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_wL,2)), 
        tuple(np.multiply(wristLxy, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    cv2.putText(image, str(round(angl_wR,2)), 
        tuple(np.multiply(wristRxy, [640, 480]).astype(int)), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 228, 42), 2, cv2.LINE_AA
        )
    end_time=datetime.now()
    time_dif= (end_time-start_time).total_seconds()

    angulosT=[time_dif, angl_sL,angl_sR, angl_eL, angl_eR, angl_wL, angl_wR]
    allangle.append(angulosT)

    return [allangle,time_dif]
 
def obtener_datosxy():
    print('plano xy')
    MpipeF="video"
    Vori="videoOriginal"
    VAng="angulosmediapipe"
    vdat="datosmediapipe"

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    # VIDEO FEED
    cap = cv2.VideoCapture(0)
    dirc=os.getcwd()
    doko=dirc+"/"+'registros'+"/"+'xy'+"/"+"/videoOriginal/"

    [namemediapipe,namemeoriginal,nameangle,namedat]=sailor(doko,0,0)

    pathvM=dirc+"/"+'registros'+"/"+'xy'+"/"+MpipeF+"/"+namemediapipe
    pathvO=dirc+"/"+'registros'+"/"+'xy'+"/"+Vori+"/"+namemeoriginal
    pathvA=dirc+"/"+'registros'+"/"+'xy'+"/"+VAng+"/"+nameangle
    pathvD=dirc+"/"+'registros'+"/"+'xy'+"/"+vdat+"/"+namedat
    alldata = []
    allangle=[]

    salida=cv2.VideoWriter(namemediapipe, cv2.VideoWriter_fourcc(*'XVID'),10,(640,480))
    original=cv2.VideoWriter(namemeoriginal, cv2.VideoWriter_fourcc(*'XVID'),10,(640,480))

    ## Setup mediapipe instance
    line1=0
    x_vec=0

    start_time=datetime.now()

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            
            ret, frame = cap.read()
            if ret:
                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                #end_time=datetime.now()
                #time_dif= end_time-start_time
                #print(time_dif)
                
                # Make detection
                results = pose.process(image)
            
                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark
                    
                    # Get coordinates
                    [allangle]=angulosxy(image,mp_pose, landmarks,allangle,start_time)
                    
                            
                except:
                    pass
                
                
                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
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
        cv2.destroyAllWindows()
             
    df2 = pd.DataFrame(allangle)
    df2.to_excel(nameangle)
    shutil.move(nameangle, pathvA)
    archi(nameangle)
    shutil.move(namemediapipe, pathvM)
    archi(namemediapipe)
    shutil.move(namemeoriginal, pathvO)
    archi(namemeoriginal)

def obtener_datoszy():
    print('plano zy')
    MpipeF="video"
    Vori="videoOriginal"
    VAng="angulosmediapipe"
    vdat="datosmediapipe"

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    # VIDEO FEED
    cap = cv2.VideoCapture(0)
    dirc=os.getcwd()
    doko=dirc+"/"+'Registros'+"/"+'zy'+"/videoOriginal/"

    [namemediapipe,namemeoriginal,nameangle,namedat]=sailor(doko,0,0)

    pathvM=dirc+"/"+'Registros'+"/"+'zy'+"/"+MpipeF+"/"+namemediapipe
    pathvO=dirc+"/"+'Registros'+"/"+'zy'+"/"+Vori+"/"+namemeoriginal
    pathvA=dirc+"/"+'Registros'+"/"+'zy'+"/"+VAng+"/"+nameangle

    allangle=[]

    salida=cv2.VideoWriter(namemediapipe, cv2.VideoWriter_fourcc(*'XVID'),10,(640,480))
    original=cv2.VideoWriter(namemeoriginal, cv2.VideoWriter_fourcc(*'XVID'),10,(640,480))

    ## Setup mediapipe instance
    line1=0
    x_vec=0
    start_time=datetime.now()
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                allangle=anguloszy(image,mp_pose, landmarks,allangle,start_time)
                
                        
            except:
                pass
            
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
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
        cv2.destroyAllWindows()
             
    df2 = pd.DataFrame(allangle)
    df2.to_excel(nameangle)
    shutil.move(nameangle, pathvA)
    archi(nameangle)
    shutil.move(namemediapipe, pathvM)
    archi(namemediapipe)
    shutil.move(namemeoriginal, pathvO)
    archi(namemeoriginal)

def obtener_datosxz():
    print('plano xz')
    MpipeF="video"
    Vori="videoOriginal"
    VAng="angulosmediapipe"
    vdat="datosmediapipe"

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    # VIDEO FEED
    cap = cv2.VideoCapture(0)
    dirc=os.getcwd()
    doko=dirc+"/"+'Registros'+"/"+'xz'+"/videoOriginal/"

    [namemediapipe,namemeoriginal,nameangle,namedat]=sailor(doko,0,0)

    pathvM=dirc+"/"+'Registros'+"/"+'xz'+"/"+MpipeF+"/"+namemediapipe
    pathvO=dirc+"/"+'Registros'+"/"+'xz'+"/"+Vori+"/"+namemeoriginal
    pathvA=dirc+"/"+'Registros'+"/"+'xz'+"/"+VAng+"/"+nameangle
    pathvD=dirc+"/"+'Registros'+"/"+'xz'+"/"+vdat+"/"+namedat

    allangle=[]

    salida=cv2.VideoWriter(namemediapipe, cv2.VideoWriter_fourcc(*'XVID'),10,(640,480))
    original=cv2.VideoWriter(namemeoriginal, cv2.VideoWriter_fourcc(*'XVID'),10,(640,480))

    ## Setup mediapipe instance
    line1=0
    x_vec=0
    start_time=datetime.now()
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                allangle=angulosxz(image,mp_pose, landmarks,allangle,start_time)
                         
            except:
                pass
            
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
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
        cv2.destroyAllWindows()
             
    df2 = pd.DataFrame(allangle)
    df2.to_excel(nameangle)
    shutil.move(nameangle, pathvA)
    archi(nameangle)
    shutil.move(namemediapipe, pathvM)
    archi(namemediapipe)
    shutil.move(namemeoriginal, pathvO)
    archi(namemeoriginal)

def aceleracion(df):
    dfdev = df.diff()
    acang=pd.DataFrame()
    acang[0]=dfdev[0]
    acang[1]=dfdev[1]/dfdev[0]
    acang[2]=dfdev[2]/dfdev[0]
    acang[3]=dfdev[3]/dfdev[0]
    acang[4]=dfdev[4]/dfdev[0]
    acang[5]=dfdev[5]/dfdev[0]
    acang[6]=dfdev[6]/dfdev[0]
    Ac_ang=pd.DataFrame()
    Ac_ang[1]=acang[1].diff()/dfdev[0]
    Ac_ang[2]=acang[2].diff()/dfdev[0]
    Ac_ang[3]=acang[3].diff()/dfdev[0]
    Ac_ang[4]=acang[4].diff()/dfdev[0]
    Ac_ang[5]=acang[5].diff()/dfdev[0]
    Ac_ang[6]=acang[6].diff()/dfdev[0]
    return Ac_ang

def grafangle(df2, name_fig, nameim):
    
    fig, ax = plt.subplots(3, 2)
    fig.suptitle(name_fig)
    fig.set_size_inches(18.5, 10.5)
    plt.subplots_adjust(wspace=0.143, hspace= 0.36,bottom=0.11, left=0.045)
    ax[0, 0].plot(df2[0], df2[1],'g')
    ax[0, 0].set_title("Hombro izquierdo")
    ax[0, 1].plot(df2[0], df2[2],'r')
    ax[0, 1].set_title("Hombro derecho")
    ax[1, 0].plot(df2[0], df2[3],'g')
    ax[1, 0].set_title("Codo izquierdo")
    ax[1,1].plot(df2[0], df2[4], 'r')
    ax[1,1].set_title("Codo derecho")
    ax[2,0].plot(df2[0], df2[5], 'g')
    ax[2,0].set_title("Muñeca izquierda")
    ax[2,1].plot(df2[0], df2[6], 'r')
    ax[2,1].set_title("Muñeca derecha")
    plt.setp(ax[-1, :], xlabel='Tiempo (segundos)')
    plt.setp(ax[:, 0], ylabel='Ángulos (grados)')
    plt.show()
    fig.savefig(nameim, dpi=100)
    print('figura'+nameim+'ha sido guardada')

def bx_plot_rms(df2, name_fig):
    
    fig, ax = plt.subplots(3, 2)
    fig.suptitle(name_fig)
    plt.subplots_adjust(wspace=0.143, hspace= 0.36,bottom=0.11, left=0.045)
    ax[0, 0].boxplot(df2[1])
    ax[0, 0].set_title("left shoulder")
    ax[0, 1].boxplot(df2[2])
    ax[0, 1].set_title("Right shoulder")
    ax[1, 0].boxplot(df2[3])
    ax[1, 0].set_title("left Elbow")
    ax[1,1].boxplot(df2[4], 'g')
    ax[1,1].set_title("Right Elbow")
    ax[2,0].boxplot(df2[5], 'g')
    ax[2,0].set_title("left wrist")
    ax[2,1].boxplot(df2[6], 'g')
    ax[2,1].set_title("Right wrist")
    plt.show()

def vid_obtener_datosxy():

    VAng="angulosmediapipe"
    vdat="datosmediapipe"

    # VIDEO FEED
    cap = cv2.VideoCapture(filename)
    dirc=os.getcwd()
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    doko=dirc+"/"+'Registros'+"/"+'xy'+"/angulosmediapipe/"
    da=dirc+"/"+'Registros'+"/"+'xy'+'/grafica_angulos_tiempo'
    dg=dirc+"/"+'Registros'+"/"+'xy'+'/grafica_aceleracion_tiempo'
    [acel,acelplace]=figname(dg, 'aceleracion.png')
    [angl,anglplace]=figname(da, 'angulos.png')
    [namemediapipe,namemeoriginal,nameangle,namedat]=sailor(doko,0,0)

    pathvA=dirc+"/"+'Registros'+"/"+'xy'+"/"+VAng+"/"+nameangle
    pathvD=dirc+"/"+'Registros'+"/"+'xy'+"/"+vdat+"/"+namedat
    allangle=[]

    ## Setup mediapipe instance
    line1=0
    x_vec=0
    start_time=datetime.now()
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                [allangle,time_dif]=angulosxy(image,mp_pose, landmarks,allangle,start_time)
                
                        
            except:
                pass
            
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            

            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                
                break

        cap.release()
        
        cv2.destroyAllWindows()  
    df2 = pd.DataFrame(allangle)
    df2.to_excel(nameangle)

    dfdev = df2.diff()
    acang=pd.DataFrame()
    acang[0]=dfdev[0]
    acang[1]=dfdev[1]/dfdev[0]
    acang[2]=dfdev[2]/dfdev[0]
    acang[3]=dfdev[3]/dfdev[0]
    acang[4]=dfdev[4]/dfdev[0]
    acang[5]=dfdev[5]/dfdev[0]
    acang[6]=dfdev[6]/dfdev[0]
    Ac_ang=pd.DataFrame()
    Ac_ang[0]=df2[0]
    Ac_ang[1]=acang[1].diff()/dfdev[0]
    Ac_ang[2]=acang[2].diff()/dfdev[0]
    Ac_ang[3]=acang[3].diff()/dfdev[0]
    Ac_ang[4]=acang[4].diff()/dfdev[0]
    Ac_ang[5]=acang[5].diff()/dfdev[0]
    Ac_ang[6]=acang[6].diff()/dfdev[0]
    shutil.move(nameangle, pathvA)
    archi(nameangle)
    Ac_ang.to_excel(namedat)
    shutil.move(namedat, pathvD)
    archi(namedat)
    df2.drop(df2.index[0:9], inplace=True)
    global XY_AC
    global XY_DEG

    grafangle(df2,'Angulos en plano xy',angl)

    Ac_ang.drop(Ac_ang.index[0:9], inplace=True)
    XY_DEG=df2
    XY_AC=Ac_ang
    grafangle(Ac_ang,'Aceleracion en plano xy',acel)

    shutil.move(angl, anglplace)
    archi(angl)
    shutil.move(acel, acelplace)
    archi(acel)
    Report=pd.DataFrame()
    Report['mean']=[df2[1].mean(),df2[2].mean(),df2[3].mean(),df2[4].mean(),df2[5].mean(),df2[6].mean()]
    Report['std']=[df2[1].std(),df2[2].std(),df2[3].std(),df2[4].std(),df2[5].std(),df2[6].std()]
    Report['min']=[df2[1].min(),df2[2].min(),df2[3].min(),df2[4].min(),df2[5].min(),df2[6].min()]
    Report['25%']=[df2[1].quantile(0.25),df2[2].quantile(0.25),df2[3].quantile(0.25),df2[4].quantile(0.25),df2[5].quantile(0.25),df2[6].quantile(0.25)]
    Report['50%']=[df2[1].quantile(0.50),df2[2].quantile(0.50),df2[3].quantile(0.50),df2[4].quantile(0.50),df2[5].quantile(0.50),df2[6].quantile(0.50)]
    Report['75%']=[df2[1].quantile(0.75),df2[2].quantile(0.75),df2[3].quantile(0.75),df2[4].quantile(0.75),df2[5].quantile(0.75),df2[6].quantile(0.75)]
    Report['max']=[df2[1].max(),df2[2].max(),df2[3].max(),df2[4].max(),df2[5].max(),df2[6].max()]
    Report.index=["left shoulder","Right shoulder","left Elbow","Right Elbow","left wrist","Right wrist"]
    diR=dirc+"/"+'Registros'+"/"+'xy'+'/Report_angle_tiempo'
    diA=dirc+"/"+'Registros'+"/"+'xy'+'/Report_aceleracion_tiempo'
    [Rangle,Rangleplace]=figname(diR, 'report_angles.xlsx')
    [Racel,Raceleplace]=figname(diA, 'report_aceleracion.xlsx')
    print('Report xy')
    print(Report)
    Report.to_excel(Rangle)
    shutil.move(Rangle, Rangleplace)
    archi(Rangle)
    ReportA=pd.DataFrame()
    ReportA['mean']=[Ac_ang[1].mean(),Ac_ang[2].mean(),Ac_ang[3].mean(),Ac_ang[4].mean(),Ac_ang[5].mean(),Ac_ang[6].mean()]
    ReportA['std']=[Ac_ang[1].std(),Ac_ang[2].std(),Ac_ang[3].std(),Ac_ang[4].std(),Ac_ang[5].std(),Ac_ang[6].std()]
    ReportA['min']=[Ac_ang[1].min(),Ac_ang[2].min(),Ac_ang[3].min(),Ac_ang[4].min(),Ac_ang[5].min(),Ac_ang[6].min()]
    ReportA['25%']=[Ac_ang[1].quantile(0.25),Ac_ang[2].quantile(0.25),Ac_ang[3].quantile(0.25),Ac_ang[4].quantile(0.25),Ac_ang[5].quantile(0.25),Ac_ang[6].quantile(0.25)]
    ReportA['50%']=[Ac_ang[1].quantile(0.50),Ac_ang[2].quantile(0.50),Ac_ang[3].quantile(0.50),Ac_ang[4].quantile(0.50),Ac_ang[5].quantile(0.50),Ac_ang[6].quantile(0.50)]
    ReportA['75%']=[Ac_ang[1].quantile(0.75),Ac_ang[2].quantile(0.75),Ac_ang[3].quantile(0.75),Ac_ang[4].quantile(0.75),Ac_ang[5].quantile(0.75),Ac_ang[6].quantile(0.75)]
    ReportA['max']=[Ac_ang[1].max(),Ac_ang[2].max(),Ac_ang[3].max(),Ac_ang[4].max(),Ac_ang[5].max(),Ac_ang[6].max()]
    ReportA.index=["left shoulder","Right shoulder","left Elbow","Right Elbow","left wrist","Right wrist"]
    print(ReportA)
    ReportA.to_excel(Racel)
    shutil.move(Racel, Raceleplace)
    archi(Racel)

def vid_obtener_datosxz():

    VAng="angulosmediapipe"
    vdat="datosmediapipe"

    # VIDEO FEED
    cap = cv2.VideoCapture(filename)
    dirc=os.getcwd()
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    doko=dirc+"/"+'Registros'+"/"+'xz'+"/angulosmediapipe/"
    da=dirc+"/"+'Registros'+"/"+'xz'+'/grafica_angulos_tiempo'
    dg=dirc+"/"+'Registros'+"/"+'xz'+'/grafica_aceleracion_tiempo'
    [acel,acelplace]=figname(dg, 'aceleracion.png')
    [angl,anglplace]=figname(da, 'angulos.png')
    [namemediapipe,namemeoriginal,nameangle,namedat]=sailor(doko,0,0)

    pathvA=dirc+"/"+'Registros'+"/"+'xz'+"/"+VAng+"/"+nameangle
    pathvD=dirc+"/"+'Registros'+"/"+'xz'+"/"+vdat+"/"+namedat
    allangle=[]

    ## Setup mediapipe instance
    line1=0
    x_vec=0
    start_time=datetime.now()
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                [allangle,time_dif]=angulosxz(image,mp_pose, landmarks,allangle,start_time)
                
                        
            except:
                pass
            
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            

            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                
                break

        cap.release()
        
        cv2.destroyAllWindows()  
    df2 = pd.DataFrame(allangle)
    df2.to_excel(nameangle)
   
    dfdev = df2.diff()
    acang=pd.DataFrame()
    acang[0]=dfdev[0]
    acang[1]=dfdev[1]/dfdev[0]
    acang[2]=dfdev[2]/dfdev[0]
    acang[3]=dfdev[3]/dfdev[0]
    acang[4]=dfdev[4]/dfdev[0]
    acang[5]=dfdev[5]/dfdev[0]
    acang[6]=dfdev[6]/dfdev[0]
    Ac_ang=pd.DataFrame()
    Ac_ang[0]=df2[0]
    Ac_ang[1]=acang[1].diff()/dfdev[0]
    Ac_ang[2]=acang[2].diff()/dfdev[0]
    Ac_ang[3]=acang[3].diff()/dfdev[0]
    Ac_ang[4]=acang[4].diff()/dfdev[0]
    Ac_ang[5]=acang[5].diff()/dfdev[0]
    Ac_ang[6]=acang[6].diff()/dfdev[0]
    shutil.move(nameangle, pathvA)
    archi(nameangle)
    Ac_ang.to_excel(namedat)
    shutil.move(namedat, pathvD)
    df2.drop(df2.index[0:9], inplace=True)
    grafangle(df2,'Angulos en plano xz',angl)
    Ac_ang.drop(Ac_ang.index[0:9], inplace=True)
    plt.close()
    grafangle(Ac_ang,'Aceleracion en plano xz',acel)
    plt.close()

    global XZ_AC
    XZ_AC=Ac_ang
    global XZ_DEG
    XZ_DEG=df2
    shutil.move(angl, anglplace)
    archi(angl)
    shutil.move(acel, acelplace)
    archi(acel)
    #print(Ac_ang.head)
    Report=pd.DataFrame()
    Report['mean']=[df2[1].mean(),df2[2].mean(),df2[3].mean(),df2[4].mean(),df2[5].mean(),df2[6].mean()]
    Report['std']=[df2[1].std(),df2[2].std(),df2[3].std(),df2[4].std(),df2[5].std(),df2[6].std()]
    Report['min']=[df2[1].min(),df2[2].min(),df2[3].min(),df2[4].min(),df2[5].min(),df2[6].min()]
    Report['25%']=[df2[1].quantile(0.25),df2[2].quantile(0.25),df2[3].quantile(0.25),df2[4].quantile(0.25),df2[5].quantile(0.25),df2[6].quantile(0.25)]
    Report['50%']=[df2[1].quantile(0.50),df2[2].quantile(0.50),df2[3].quantile(0.50),df2[4].quantile(0.50),df2[5].quantile(0.50),df2[6].quantile(0.50)]
    Report['75%']=[df2[1].quantile(0.75),df2[2].quantile(0.75),df2[3].quantile(0.75),df2[4].quantile(0.75),df2[5].quantile(0.75),df2[6].quantile(0.75)]
    Report['max']=[df2[1].max(),df2[2].max(),df2[3].max(),df2[4].max(),df2[5].max(),df2[6].max()]
    Report.index=["left shoulder","Right shoulder","left Elbow","Right Elbow","left wrist","Right wrist"]
    diR=dirc+"/"+'Registros'+"/"+'xz'+'/Report_angle_tiempo'
    diA=dirc+"/"+'Registros'+"/"+'xz'+'/Report_aceleracion_tiempo'
    [Rangle,Rangleplace]=figname(diR, 'report_angles.xlsx')
    [Racel,Raceleplace]=figname(diA, 'report_aceleracion.xlsx')
    print(Report)
    Report.to_excel(Rangle)
    shutil.move(Rangle, Rangleplace)
    archi(Rangle)
    ReportA=pd.DataFrame()
    ReportA['mean']=[Ac_ang[1].mean(),Ac_ang[2].mean(),Ac_ang[3].mean(),Ac_ang[4].mean(),Ac_ang[5].mean(),Ac_ang[6].mean()]
    ReportA['std']=[Ac_ang[1].std(),Ac_ang[2].std(),Ac_ang[3].std(),Ac_ang[4].std(),Ac_ang[5].std(),Ac_ang[6].std()]
    ReportA['min']=[Ac_ang[1].min(),Ac_ang[2].min(),Ac_ang[3].min(),Ac_ang[4].min(),Ac_ang[5].min(),Ac_ang[6].min()]
    ReportA['25%']=[Ac_ang[1].quantile(0.25),Ac_ang[2].quantile(0.25),Ac_ang[3].quantile(0.25),Ac_ang[4].quantile(0.25),Ac_ang[5].quantile(0.25),Ac_ang[6].quantile(0.25)]
    ReportA['50%']=[Ac_ang[1].quantile(0.50),Ac_ang[2].quantile(0.50),Ac_ang[3].quantile(0.50),Ac_ang[4].quantile(0.50),Ac_ang[5].quantile(0.50),Ac_ang[6].quantile(0.50)]
    ReportA['75%']=[Ac_ang[1].quantile(0.75),Ac_ang[2].quantile(0.75),Ac_ang[3].quantile(0.75),Ac_ang[4].quantile(0.75),Ac_ang[5].quantile(0.75),Ac_ang[6].quantile(0.75)]
    ReportA['max']=[Ac_ang[1].max(),Ac_ang[2].max(),Ac_ang[3].max(),Ac_ang[4].max(),Ac_ang[5].max(),Ac_ang[6].max()]
    ReportA.index=["left shoulder","Right shoulder","left Elbow","Right Elbow","left wrist","Right wrist"]
    print('Report xz')
    print(ReportA)
    ReportA.to_excel(Racel)
    shutil.move(Racel, Raceleplace)
    archi(Racel)

def vid_obtener_datoszy():

    VAng="angulosmediapipe"
    vdat="datosmediapipe"

    # VIDEO FEED
    cap = cv2.VideoCapture(filename)
    dirc=os.getcwd()
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    doko=dirc+"/"+'Registros'+"/"+'zy'+"/angulosmediapipe/"
    da=dirc+"/"+'Registros'+"/"+'zy'+'/grafica_angulos_tiempo'
    dg=dirc+"/"+'Registros'+"/"+'zy'+'/grafica_aceleracion_tiempo'
    [acel,acelplace]=figname(dg, 'aceleracion.png')
    [angl,anglplace]=figname(da, 'angulos.png')
    [namemediapipe,namemeoriginal,nameangle,namedat]=sailor(doko,0,0)

    pathvA=dirc+"/"+'Registros'+"/"+'zy'+"/"+VAng+"/"+nameangle
    pathvD=dirc+"/"+'Registros'+"/"+'zy'+"/"+vdat+"/"+namedat
    allangle=[]

    ## Setup mediapipe instance
    line1=0
    x_vec=0
    start_time=datetime.now()
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                [allangle,time_dif]=anguloszy(image,mp_pose, landmarks,allangle,start_time)
                
                        
            except:
                pass
            
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            

            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                
                break

        cap.release()
        
        cv2.destroyAllWindows()  
    df2 = pd.DataFrame(allangle)
    df2.to_excel(nameangle)
    shutil.move(nameangle, pathvA)
    archi(nameangle)
    dfdev = df2.diff()
    acang=pd.DataFrame()
    acang[0]=dfdev[0]
    acang[1]=dfdev[1]/dfdev[0]
    acang[2]=dfdev[2]/dfdev[0]
    acang[3]=dfdev[3]/dfdev[0]
    acang[4]=dfdev[4]/dfdev[0]
    acang[5]=dfdev[5]/dfdev[0]
    acang[6]=dfdev[6]/dfdev[0]
    Ac_ang=pd.DataFrame()
    Ac_ang[0]=df2[0]
    Ac_ang[1]=acang[1].diff()/dfdev[0]
    Ac_ang[2]=acang[2].diff()/dfdev[0]
    Ac_ang[3]=acang[3].diff()/dfdev[0]
    Ac_ang[4]=acang[4].diff()/dfdev[0]
    Ac_ang[5]=acang[5].diff()/dfdev[0]
    Ac_ang[6]=acang[6].diff()/dfdev[0]
    Ac_ang.to_excel(namedat)
    shutil.move(namedat, pathvD)
    archi(namedat)
    df2.drop(df2.index[0:9], inplace=True)
    grafangle(df2,'Angulos en plano zy',angl)
    Ac_ang.drop(Ac_ang.index[0:9], inplace=True)

    grafangle(Ac_ang,'Aceleracion en plano zy',acel)
    global ZY_AC
    ZY_AC=Ac_ang
    global ZY_DEG
    ZY_DEG=df2

    shutil.move(angl, anglplace)
    archi(angl)
    shutil.move(acel, acelplace)
    archi(acel)
    #print(Ac_ang.head)
    Report=pd.DataFrame()
    Report['mean']=[df2[1].mean(),df2[2].mean(),df2[3].mean(),df2[4].mean(),df2[5].mean(),df2[6].mean()]
    Report['std']=[df2[1].std(),df2[2].std(),df2[3].std(),df2[4].std(),df2[5].std(),df2[6].std()]
    Report['min']=[df2[1].min(),df2[2].min(),df2[3].min(),df2[4].min(),df2[5].min(),df2[6].min()]
    Report['25%']=[df2[1].quantile(0.25),df2[2].quantile(0.25),df2[3].quantile(0.25),df2[4].quantile(0.25),df2[5].quantile(0.25),df2[6].quantile(0.25)]
    Report['50%']=[df2[1].quantile(0.50),df2[2].quantile(0.50),df2[3].quantile(0.50),df2[4].quantile(0.50),df2[5].quantile(0.50),df2[6].quantile(0.50)]
    Report['75%']=[df2[1].quantile(0.75),df2[2].quantile(0.75),df2[3].quantile(0.75),df2[4].quantile(0.75),df2[5].quantile(0.75),df2[6].quantile(0.75)]
    Report['max']=[df2[1].max(),df2[2].max(),df2[3].max(),df2[4].max(),df2[5].max(),df2[6].max()]
    Report.index=["left shoulder","Right shoulder","left Elbow","Right Elbow","left wrist","Right wrist"]
    diR=dirc+"/"+'Registros'+"/"+'zy'+'/Report_angle_tiempo'
    diA=dirc+"/"+'Registros'+"/"+'zy'+'/Report_aceleracion_tiempo'
    [Rangle,Rangleplace]=figname(diR, 'report_angles.xlsx')
    [Racel,Raceleplace]=figname(diA, 'report_aceleracion.xlsx')
    print('Report zy')
    print(Report)
    Report.to_excel(Rangle)
    shutil.move(Rangle, Rangleplace)
    archi(Rangle)
    ReportA=pd.DataFrame()
    ReportA['mean']=[Ac_ang[1].mean(),Ac_ang[2].mean(),Ac_ang[3].mean(),Ac_ang[4].mean(),Ac_ang[5].mean(),Ac_ang[6].mean()]
    ReportA['std']=[Ac_ang[1].std(),Ac_ang[2].std(),Ac_ang[3].std(),Ac_ang[4].std(),Ac_ang[5].std(),Ac_ang[6].std()]
    ReportA['min']=[Ac_ang[1].min(),Ac_ang[2].min(),Ac_ang[3].min(),Ac_ang[4].min(),Ac_ang[5].min(),Ac_ang[6].min()]
    ReportA['25%']=[Ac_ang[1].quantile(0.25),Ac_ang[2].quantile(0.25),Ac_ang[3].quantile(0.25),Ac_ang[4].quantile(0.25),Ac_ang[5].quantile(0.25),Ac_ang[6].quantile(0.25)]
    ReportA['50%']=[Ac_ang[1].quantile(0.50),Ac_ang[2].quantile(0.50),Ac_ang[3].quantile(0.50),Ac_ang[4].quantile(0.50),Ac_ang[5].quantile(0.50),Ac_ang[6].quantile(0.50)]
    ReportA['75%']=[Ac_ang[1].quantile(0.75),Ac_ang[2].quantile(0.75),Ac_ang[3].quantile(0.75),Ac_ang[4].quantile(0.75),Ac_ang[5].quantile(0.75),Ac_ang[6].quantile(0.75)]
    ReportA['max']=[Ac_ang[1].max(),Ac_ang[2].max(),Ac_ang[3].max(),Ac_ang[4].max(),Ac_ang[5].max(),Ac_ang[6].max()]
    ReportA.index=["left shoulder","Right shoulder","left Elbow","Right Elbow","left wrist","Right wrist"]
    print(ReportA)
    ReportA.to_excel(Racel)
    shutil.move(Racel, Raceleplace)
    archi(Racel)

def calculoAC():
    dirc=os.getcwd()
    dircreq=dirc+"/"+'Registros'
    di=dirc+"/"+'Registros'+"/"+'report_ac_rms'
    [namfile,place]=figname(dircreq, 'aceleracion_rms.png')
    [namrep,placerep]=figname(di, 'Reporte_est_acerelacion_rms.xlsx')
    fig, ax = plt.subplots(3, 2)
    fig.suptitle('Aceleracion rms')
    plt.subplots_adjust(wspace=0.143, hspace= 0.36,bottom=0.11, left=0.045)
    fig.set_size_inches(18.5, 10.5)
    AB_RMS=pd.DataFrame()
    dirc=os.getcwd()
    Lshouder=pd.DataFrame()
    Lshouder['xy']=XY_AC[1]
    Lshouder['zy']=ZY_AC[1]
    Lshouder['xz']=XZ_AC[1]
    rms1=RMSdtf(Lshouder)
    ax[0, 0].boxplot(rms1,vert=False, patch_artist=True)
    ax[0, 0].set_title("left shoulder")

    Rshouder=pd.DataFrame()
    Rshouder['xy']=XY_AC[2]
    Rshouder['zy']=ZY_AC[2]
    Rshouder['xz']=XZ_AC[2]
    rms2=RMSdtf(Rshouder)
    ax[0, 1].boxplot(rms2,vert=False, patch_artist=True)
    ax[0, 1].set_title("right shoulder")

    Lelbow=pd.DataFrame()
    Lelbow['xy']=XY_AC[3]
    Lelbow['zy']=ZY_AC[3]
    Lelbow['xz']=XZ_AC[3]
    rms3=RMSdtf(Lelbow)
    ax[1, 0].boxplot(rms3,vert=False, patch_artist=True)
    ax[1, 0].set_title("left elbow")

    Relbow=pd.DataFrame()
    Relbow['xy']=XY_AC[4]
    Relbow['zy']=ZY_AC[4]
    Relbow['xz']=XZ_AC[4]
    rms4=RMSdtf(Relbow)
    ax[1, 1].boxplot(rms4,vert=False, patch_artist=True)
    ax[1, 1].set_title("Right elbow")

    Lwrist=pd.DataFrame()
    Lwrist['xy']=XY_AC[5]
    Lwrist['zy']=ZY_AC[5]
    Lwrist['xz']=XZ_AC[5]
    rms5=RMSdtf(Lwrist)
    ax[2, 0].boxplot(rms5,vert=False, patch_artist=True)
    ax[2, 0].set_title("Left wrist")

    Rwrist=pd.DataFrame()
    Rwrist['xy']=XY_AC[6]
    Rwrist['zy']=ZY_AC[6]
    Rwrist['xz']=XZ_AC[6]
    rms6=RMSdtf(Rwrist)
    ax[2, 1].boxplot(rms6,vert=False, patch_artist=True)
    ax[2, 1].set_title("Right wrist")
    
    Report=pd.DataFrame()
    Report['mean']=[rms1.mean(),rms2.mean(),rms3.mean(),rms4.mean(),rms5.mean(),rms6.mean()]
    Report['std']=[rms1.std(),rms2.std(),rms3.std(),rms4.std(),rms5.std(),rms6.std()]
    Report['min']=[rms1.min(),rms2.min(),rms3.min(),rms4.min(),rms5.min(),rms6.min()]
    Report['25%']=[rms1.quantile(0.25),rms2.quantile(0.25),rms3.quantile(0.25),rms4.quantile(0.25),rms5.quantile(0.25),rms6.quantile(0.25)]
    Report['50%']=[rms1.quantile(0.50),rms2.quantile(0.50),rms3.quantile(0.50),rms4.quantile(0.50),rms5.quantile(0.50),rms6.quantile(0.50)]
    Report['75%']=[rms1.quantile(0.75),rms2.quantile(0.75),rms3.quantile(0.75),rms4.quantile(0.75),rms5.quantile(0.75),rms6.quantile(0.75)]
    Report['max']=[rms1.max(),rms2.max(),rms3.max(),rms4.max(),rms5.max(),rms6.max()]
    Report.index=["left shoulder","Right shoulder","left Elbow","Right Elbow","left wrist","Right wrist"]
    print(Report)
    plt.show()
    fig.savefig(namfile, dpi=100)
    shutil.move(namfile, place)
    archi(namfile)
    Report.to_excel(namrep)
    shutil.move(namrep, placerep)
    archi(namrep)

def calculoDEG():
    dirc=os.getcwd()
    dircreq=dirc+"/"+'Registros'
    di=dirc+"/"+'Registros'+"/"+'report_deg_rms'
    [namfile,place]=figname(dircreq, 'angulos_rms.png')
    [namrep,placerep]=figname(di, 'Reporte_est_angulos_rms.xlsx')
    fig, ax = plt.subplots(3, 2)
    fig.suptitle('Angulos rms')
    plt.subplots_adjust(wspace=0.143, hspace= 0.36,bottom=0.11, left=0.045)
    fig.set_size_inches(18.5, 10.5)
    AB_RMS=pd.DataFrame()
    dirc=os.getcwd()
    Lshouder=pd.DataFrame()
    Lshouder['xy']=XY_DEG[1]
    Lshouder['zy']=ZY_DEG[1]
    Lshouder['xz']=XZ_DEG[1]
    rms1=RMSdtf(Lshouder)
    ax[0, 0].boxplot(rms1,vert=False, patch_artist=True)
    ax[0, 0].set_title("left shoulder")

    Rshouder=pd.DataFrame()
    Rshouder['xy']=XY_DEG[2]
    Rshouder['zy']=ZY_DEG[2]
    Rshouder['xz']=XZ_DEG[2]
    rms2=RMSdtf(Rshouder)
    ax[0, 1].boxplot(rms2,vert=False, patch_artist=True)
    ax[0, 1].set_title("right shoulder")

    Lelbow=pd.DataFrame()
    Lelbow['xy']=XY_DEG[3]
    Lelbow['zy']=ZY_DEG[3]
    Lelbow['xz']=XZ_DEG[3]
    rms3=RMSdtf(Lelbow)
    ax[1, 0].boxplot(rms3,vert=False, patch_artist=True)
    ax[1, 0].set_title("left elbow")

    Relbow=pd.DataFrame()
    Relbow['xy']=XY_DEG[4]
    Relbow['zy']=ZY_DEG[4]
    Relbow['xz']=XZ_DEG[4]
    rms4=RMSdtf(Relbow)
    ax[1, 1].boxplot(rms4,vert=False, patch_artist=True)
    ax[1, 1].set_title("Right elbow")

    Lwrist=pd.DataFrame()
    Lwrist['xy']=XY_DEG[5]
    Lwrist['zy']=ZY_DEG[5]
    Lwrist['xz']=XZ_DEG[5]
    rms5=RMSdtf(Lwrist)
    ax[2, 0].boxplot(rms5,vert=False, patch_artist=True)
    ax[2, 0].set_title("Left wrist")

    Rwrist=pd.DataFrame()
    Rwrist['xy']=XY_DEG[6]
    Rwrist['zy']=ZY_DEG[6]
    Rwrist['xz']=XZ_DEG[6]
    rms6=RMSdtf(Rwrist)
    ax[2, 1].boxplot(rms6,vert=False, patch_artist=True)
    ax[2, 1].set_title("Right wrist")
    
    Report=pd.DataFrame()
    Report['mean']=[rms1.mean(),rms2.mean(),rms3.mean(),rms4.mean(),rms5.mean(),rms6.mean()]
    Report['std']=[rms1.std(),rms2.std(),rms3.std(),rms4.std(),rms5.std(),rms6.std()]
    Report['min']=[rms1.min(),rms2.min(),rms3.min(),rms4.min(),rms5.min(),rms6.min()]
    Report['25%']=[rms1.quantile(0.25),rms2.quantile(0.25),rms3.quantile(0.25),rms4.quantile(0.25),rms5.quantile(0.25),rms6.quantile(0.25)]
    Report['50%']=[rms1.quantile(0.50),rms2.quantile(0.50),rms3.quantile(0.50),rms4.quantile(0.50),rms5.quantile(0.50),rms6.quantile(0.50)]
    Report['75%']=[rms1.quantile(0.75),rms2.quantile(0.75),rms3.quantile(0.75),rms4.quantile(0.75),rms5.quantile(0.75),rms6.quantile(0.75)]
    Report['max']=[rms1.max(),rms2.max(),rms3.max(),rms4.max(),rms5.max(),rms6.max()]
    print(Report)
    plt.show()
    fig.savefig(namfile, dpi=100)
    shutil.move(namfile, place)
    archi(namfile)
    Report.to_excel(namrep)
    shutil.move(namrep, placerep)
    archi(namrep)

def figname(direct, name):
    initial_count = 0

    for path in os.listdir(direct):
        if os.path.isfile(os.path.join(direct, path)):
            initial_count += 1

    N=initial_count
    namfile=str(N)+name
    place=direct+"/"+namfile
    return [namfile,place]

def grafsens(tl,tr,left, right, name_fig, nameim):
    
    fig, ax = plt.subplots(2, 2)
    fig.suptitle(name_fig)
    fig.set_size_inches(18.5, 10.5)
    plt.subplots_adjust(wspace=0.143, hspace= 0.36,bottom=0.11, left=0.045)
    ax[0, 0].plot(tl, left[0],'g')
    ax[0, 0].set_title("left shoulder")
    ax[0, 1].plot(tr, right[0],'r')
    ax[0, 1].set_title("Right shoulder")
    ax[1, 0].plot(tl, left[1],'g')
    ax[1, 0].set_title("left Elbow")
    ax[1,1].plot(tr, right[1], 'r')
    ax[1,1].set_title("Right Elbow")
    ax[2,0].plot(tl, left[2], 'g')
    ax[2,0].set_title("left wrist")
    ax[2,1].plot(tr, right[2], 'r')
    ax[2,1].set_title("Right wrist")
    plt.show()
    fig.savefig(nameim, dpi=100)

    print('figura'+nameim+'ha sido guardada')

def get_sensor_var():
    filenameleft = filedialog.askopenfilename()
    df0 = pd.read_csv(filenameleft)
    filenameright = filedialog.askopenfilename()
    df1 = pd.read_csv(filenameleft)
    aceL=pd.DataFrame()
    aceL[0]=df0['gx_deg/s']
    aceL[1]=df0['gy_deg/s']
    aceL[2]=df0['gz_deg/s']
    rms_aceL=RMSdtf(aceL)
    degL=pd.DataFrame()
    degL[0]=df0['x_deg']
    degL[1]=df0['y_deg']
    degL[2]=df0['z_deg']
    rms_degL=RMSdtf(degL)
    df1 = pd.read_csv(filenameright)
    aceR=pd.DataFrame()
    aceR[0]=df1['gx_deg/s']
    aceR[1]=df1['gy_deg/s']
    aceR[2]=df1['gz_deg/s']
    rms_aceR=RMSdtf(aceR)
    degR=pd.DataFrame()
    degR[0]=df1['x_deg']
    degR[1]=df1['y_deg']
    degR[2]=df1['z_deg']
    rms_degR=RMSdtf(degR)
    dirc=os.getcwd()
    wo=dirc1=dirc+"/"+'Registros'+'/sensores'
    [Gdeg,degplace]=figname(wo, 'sensores_grados_vs_tiempo.png')
    [Gacel,acelplace]=figname(wo, 'sensores_aceleracion_vs_tiempo.png')
    #grafsens(df0['time_s'],df1['time_s'],degL, degR, 'Sensores acelerometros: grafica grados VS tiempo', Gdeg)
    #grafsens(df0['time_s'],df1['time_s'],aceL, aceR, 'Sensores acelerometros: grafica aceleracion VS tiempo', Gacel)

    Report_deg=pd.DataFrame()
    Report_deg['mean']=[degL[0].mean(),degL[1].mean(),degL[2].mean(),degR[0].mean(),degR[1].mean(),degR[2].mean()]
    Report_deg['std']=[degL[0].std(),degL[1].std(),degL[2].std(),degR[0].std(),degR[1].std(),degR[2].std()]
    Report_deg['min']=[degL[0].min(),degL[1].min(),degL[2].min(),degR[0].min(),degR[1].min(),degR[2].min()]
    Report_deg['25%']=[degL[0].quantile(0.25),degL[1].quantile(0.25),degL[2].quantile(0.25),degR[0].quantile(0.25),degR[1].quantile(0.25),degR[2].quantile(0.25)]
    Report_deg['50%']=[degL[0].quantile(0.50),degL[1].quantile(0.50),degL[2].quantile(0.50),degR[0].quantile(0.50),degR[1].quantile(0.50),degR[2].quantile(0.50)]
    Report_deg['75%']=[degL[0].quantile(0.75),degL[1].quantile(0.75),degL[2].quantile(0.75),degR[0].quantile(0.75),degR[1].quantile(0.75),degR[2].quantile(0.75)]
    Report_deg['max']=[degL[0].max(),degL[1].max(),degL[2].max(), degR[0].max(),degR[1].max(),degR[2].max()]
    Report_deg.index=['Left_x_deg','Left_y_deg','Left_z_deg', 'Right_x_deg','Right_y_deg','Right_z_deg']

    Report_ace=pd.DataFrame()
    Report_ace['mean']=[aceL[0].mean(),aceL[1].mean(),aceL[2].mean(),aceR[0].mean(),aceR[1].mean(),aceR[2].mean()]
    Report_ace['std']=[aceL[0].std(),aceL[1].std(),aceL[2].std(),aceR[0].std(),aceR[1].std(),aceR[2].std()]
    Report_ace['min']=[aceL[0].min(),aceL[1].min(),aceL[2].min(),aceR[0].min(),aceR[1].min(),aceR[2].min()]
    Report_ace['25%']=[aceL[0].quantile(0.25),aceL[1].quantile(0.25),aceL[2].quantile(0.25),aceR[0].quantile(0.25),aceR[1].quantile(0.25),aceR[2].quantile(0.25)]
    Report_ace['50%']=[aceL[0].quantile(0.50),aceL[1].quantile(0.50),aceL[2].quantile(0.50),aceR[0].quantile(0.50),aceR[1].quantile(0.50),aceR[2].quantile(0.50)]
    Report_ace['75%']=[aceL[0].quantile(0.75),aceL[1].quantile(0.75),aceL[2].quantile(0.75),aceR[0].quantile(0.75),aceR[1].quantile(0.75),aceR[2].quantile(0.75)]
    Report_ace['max']=[aceL[0].max(),aceL[1].max(),aceL[2].max(), aceR[0].max(),aceR[1].max(),aceR[2].max()]
    Report_ace.index=['Left_x_ace','Left_y_ace','Left_z_ace', 'Right_x_ace','Right_y_ace','Right_z_ace']
    
    Report_rms_angle=pd.DataFrame()
    Report_rms_angle['mean']=[rms_degL.mean(),rms_degR.mean()]
    Report_rms_angle['std']=[rms_degL.std(),rms_degR.std()]
    Report_rms_angle['min']=[rms_degL.min(),rms_degR.min()]
    Report_rms_angle['25%']=[rms_degL.quantile(0.25),rms_degR.quantile(0.25)]
    Report_rms_angle['50%']=[rms_degL.quantile(0.50),rms_degR.quantile(0.50)]
    Report_rms_angle['75%']=[rms_degL.quantile(0.75),rms_degR.quantile(0.75)]
    Report_rms_angle['max']=[rms_degL.max(),rms_degR.max()]
    Report_rms_angle.index=['left angle RMS','Right angle RMS']
    
    Report_rms_acel=pd.DataFrame()
    Report_rms_acel['mean']=[rms_aceL.mean(),rms_aceR.mean()]
    Report_rms_acel['std']=[rms_aceL.std(),rms_aceR.std()]
    Report_rms_acel['min']=[rms_aceL.min(),rms_aceR.min()]
    Report_rms_acel['25%']=[rms_aceL.quantile(0.25),rms_aceR.quantile(0.25)]
    Report_rms_acel['50%']=[rms_aceL.quantile(0.50),rms_aceR.quantile(0.50)]
    Report_rms_acel['75%']=[rms_aceL.quantile(0.75),rms_aceR.quantile(0.75)]
    Report_rms_acel['max']=[rms_aceL.max(),rms_aceR.max()]
    Report_rms_acel.index=['left acel RMS','Right acel RMS']
    print(Report_deg)
    [Gdeg,degplace]=figname(wo, 'sensores_grados_vs_tiempo.png')
    [Gacel,acelplace]=figname(wo, 'sensores_aceleracion_vs_tiempo.png')

    print(Report_ace)
    print(Report_rms_angle)
    print(Report_rms_acel)
    [Report_Angles,Report_Anglesplace]=figname(wo, 'Report_Angles.xlsx')
    [Report_Aceleracion,Report_Aceleraciongplace]=figname(wo, 'Report_Aceleracion.xlsx')
    [Report_RMS_Aceleracion,Report_RMS_Aceleraciongplace]=figname(wo, 'Report_RMS_Aceleracion.xlsx')
    [Report_RMS_Angles,Report_RMS_Anglesplace]=figname(wo, 'Report_RMS_Angles.xlsx')
    Report_deg.to_excel(Report_Angles)
    shutil.move(Report_Angles, Report_Anglesplace)
    archi(Report_Angles)
    
    Report_ace.to_excel(Report_Aceleracion)
    shutil.move(Report_Aceleracion,Report_Aceleraciongplace)
    archi(Report_Aceleracion)

    Report_rms_angle.to_excel(Report_RMS_Angles)
    shutil.move(Report_RMS_Angles,Report_RMS_Anglesplace)
    archi(Report_RMS_Angles)
    
    Report_rms_acel.to_excel(Report_RMS_Aceleracion)
    shutil.move(Report_RMS_Aceleracion,Report_RMS_Aceleraciongplace)
    archi(Report_RMS_Aceleracion)
    
def cargar_video():
    #global filename
    #filename = filedialog.askopenfilename()
    vid_obtener_datosxy()
    vid_obtener_datoszy()
    vid_obtener_datosxz()
    calculoAC()
    calculoDEG()

def video_lento():
    #global filename
    #arc = filedialog.askopenfilename()
    global filename
    video = VideoFileClip(filename).fx(vfx.speedx, 0.5)
    video.write_videofile("lento.mp4")
    filename="lento.mp4"
    vid_obtener_datosxy()
    vid_obtener_datoszy()
    vid_obtener_datosxz()
    calculoAC()
    calculoDEG()

def Multiple_vid_normal():
    global filename
    filez = filedialog.askopenfilenames(multiple=True,title='Choose a file')
    lst = list(filez)
    print(lst)
    archivo = open("archivo.txt","w")
    archivo.write(str((lst)))
    archivo.close()
    for filename in lst:
        print('archivo: '+filename)
        cargar_video()

    shutil('archivo.txt','/Registros/archivo.txt')


def Multiple_vid_lento():
    global filename
    filez = filedialog.askopenfilenames(multiple=True,title='Choose a file')
    lst = list(filez)
    print(lst)
    archivo = open("archivo.txt","w")
    archivo.write(str((lst)))
    archivo.close()

    for filename in lst:
        print('archivo: '+filename)
        video_lento()
    
    
    shutil('archivo.txt','/Registros/archivo.txt')

def create_report_pdf():
    images=[]

def RMSdtf(A_art):
    A_art.fillna(0, inplace=True)
    powtwo= A_art.pow(2)
    powtwo.fillna(0, inplace=True)
    s_pow=A_art.sum(axis=1)
    rms=s_pow.pow(1./2)
    rms=rms.dropna()
    return rms

def iniciar():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    visualizar()

def visualizar():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
        else:
            lblVideo.image = ""
            cap.release()

def finalizar():
    global cap
    stop=ord('q')
    cap.release()
    cv2.destroyAllWindows()

#def newregxyz():
   # dirc=os.getcwd()
    #dircreq=dirc+"/"+'Registros'+"/"+'xyz'
    #initial_count = 0

  #  for path in os.listdir(dircreq):
   #     if os.path.isfile(os.path.join(dircreq, path)):
 #           initial_count += 1

#    Nvideo=initial_count-1

    #neededfiles(dircxyz,[str(Nvideo)])
    #dreg=dircreq+"/"+str(Nvideo)
    #neededfiles(dircxyz,['xy','zy','xz'])
    #dxy=dreg+"/"+'xy'
    #dxz=dreg+"/"+'xz'
    #dzy=dreg+"/"+'zy'
    #return[dxy,dxz,dzy]

def mover_carpt():
    carp = filedialog.askdirectory()
    print(carp)
    carpeta=carp+'/Registros'
    shutil.move('Registros', carpeta)
    #archi('Registros')
    create_files()

def create_files():
    dirc=os.getcwd()
    neededfiles(dirc,['Registros'])
    dirc1=dirc+"/"+'Registros'
    neededfiles(dirc1,["xy",'xz',"zy",'xyz','sensores','report_ac_rms','report_deg_rms'])
    dircxy=dirc1+"/"+'xy'
    dircxz=dirc1+"/"+'xz'
    dirczy=dirc1+"/"+'zy'
    dircxyz=dirc1+"/"+'xyz'
    dircxyz_xy=dircxyz+"/"+'xy'
    dircxyz_zy=dircxyz+"/"+'zy'
    dircxyz_xz=dircxyz+"/"+'xz'
    neededfiles(dircxy,["datosmediapipe",'video',"videoOriginal",'angulosmediapipe','grafica_angulos_tiempo','grafica_aceleracion_tiempo','Report_angle_tiempo','Report_aceleracion_tiempo'])
    neededfiles(dircxz,["datosmediapipe",'video',"videoOriginal",'angulosmediapipe','grafica_angulos_tiempo','grafica_aceleracion_tiempo','Report_angle_tiempo','Report_aceleracion_tiempo'])
    neededfiles(dirczy,["datosmediapipe",'video',"videoOriginal",'angulosmediapipe','grafica_angulos_tiempo','grafica_aceleracion_tiempo','Report_angle_tiempo','Report_aceleracion_tiempo'])
    neededfiles(dircxyz,["xy",'xz',"zy"])

def eliminar_carpeta():
    remove('/Registros')
    create_files()

create_files()

cap = None
root = Tk()
tx = Label(root,text="Ubicar camara",bg='lightblue')
tx.grid(column=0, row=0, columnspan=2)

barra_menu=Menu(root)
bar=Menu(barra_menu, tearoff=0)
bar.add_command(label='Mover carpeta',command=mover_carpt)
bar.add_command(label='eliminar datos',command=eliminar_carpeta)
barra_menu.add_cascade(label='Menú', menu=bar)
root.config(menu=barra_menu)

btnIniciar = Button(root, text="Iniciar", width=45, command=iniciar)
btnIniciar.grid(column=0, row=1, padx=5, pady=5)
btnFinalizar = Button(root, text="Finalizar", width=45, command=finalizar,relief="groove")
btnFinalizar.grid(column=1, row=1, padx=5, pady=5)

tx0 = Label(root,text="Tomar registro de grados hombro, codo y muñeca en plano seleccionado",bg='lightblue')
tx0.grid(column=0, row=2, columnspan=2)

btnGrabarxy = Button(root, text="Registro xy", width=45, command=obtener_datosxy,relief="groove")
btnGrabarxy.grid(column=0, row=3, padx=5, pady=5)

btnGrabarzy = Button(root, text="Registro zy", width=45, command=obtener_datoszy,relief="groove")
btnGrabarzy.grid(column=1, row=3, padx=5, pady=5)

btnGrabarxz = Button(root, text="Registro xz", width=45, command=obtener_datosxz,relief="groove")
btnGrabarxz.grid(column=0, row=4, padx=5, pady=5)

btnGrabarxyz = Button(root, text="Registro xyz", width=45, command=obtener_datosxz,relief="groove")
btnGrabarxyz.grid(column=1, row=4, padx=5, pady=5)
tx3 = Label(root,text="presione tecla (q) para detener la toma de datos",bg='lightblue')
tx3.grid(column=0, row=5, columnspan=2)

tx1 = Label(root,text="Tomar registro de video en plano seleccionado",bg='lightblue')
tx1.grid(column=0, row=6, columnspan=2)

btnregxy = Button(root, text="Registro xy", width=45, command=vid_obtener_datosxy,relief="groove")
btnregxy.grid(column=0, row=7, padx=5, pady=5)

btnregxyz = Button(root, text="Registro xz", width=45, command=vid_obtener_datosxz,relief="groove")
btnregxyz.grid(column=1, row=7, padx=5, pady=5)

btnregxyz = Button(root, text="Registro zy", width=45, command=vid_obtener_datoszy,relief="groove")
btnregxyz.grid(column=0, row=8, padx=5, pady=5)

loadvid = Button(root, text="Cargar video", width=45, command=Multiple_vid_normal,relief="groove")
loadvid.grid(column=0, row=9, padx=5, pady=5)

loalenvid = Button(root, text="Cargar video lento", width=45, command=Multiple_vid_lento,relief="groove")
loalenvid.grid(column=1, row=9, padx=5, pady=5)

tx1 = Label(root,text="Calcular RMS, Boxplot y otros en 3 ejes",bg='lightblue')
tx1.grid(column=0, row=10, columnspan=2)

btnregxyz = Button(root, text="calculo RMS Ac", width=45, command=calculoAC,relief="groove")
btnregxyz.grid(column=0, row=11, padx=5, pady=5)

btnregxyz = Button(root, text="calculo RMS Deg", width=45, command=calculoDEG,relief="groove")
btnregxyz.grid(column=1, row=11, padx=5, pady=5)

btnregxyz = Button(root, text="Datos sensor inercial", width=45, command=get_sensor_var,relief="groove")
btnregxyz.grid(column=0, row=12, padx=5, pady=5)

btnregxyz = Button(root, text="Reporte resultados movimiento PDF", width=45, command=create_report_pdf,relief="groove")
btnregxyz.grid(column=1, row=12, padx=5, pady=5)

lblVideo = Label(root)
lblVideo.grid(column=3, row=0, columnspan=2,rowspan=16)

root.config(bg='lightblue')
root.title('Tesis maestria: obtención de datos')
root.resizable(0,0)
root.mainloop()