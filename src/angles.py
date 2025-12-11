# src/angles.py
import numpy as np
import pandas as pd
import cv2
from datetime import datetime
from pathlib import Path

def calculate_angle(a, b, c):
    """
    Calcula el ángulo entre los puntos a-b-c en grados.
    """
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def shouldvect(hip, should):
    #x=hip[0]+(should[0]-hip[0])# tonto
    x=should[0]# Se usa coordenada X de hombro paraque esté al msmo nivel
    y=hip[1]
    return (x,y)

# Las funciones angulosxy, angulosxz, anguloszy toman la imagen, mp_pose, landmarks y van construyendo 'allangle'.
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

