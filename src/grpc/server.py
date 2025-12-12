# src/grpc/server.py (importaciones corregidas)
import grpc
from concurrent import futures
import logging
import time
from datetime import datetime
import cv2
import numpy as np
import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))

import pose_analysis_pb2 as pb
import pose_analysis_pb2_grpc as pb_grpc
# Importar TU lógica existente desde src (nuevo path)
try:
    # Importar desde el mismo nivel (src/)
    from .. import video as video_module
    from .. import angles as angles_module
    from .. import sensors as sensors_module
    from .. import io_module as io_module
    
    # Acceder a funciones específicas
    if hasattr(video_module, 'procesar_video_plano'):
        procesar_video_plano = video_module.procesar_video_plano
    else:
        # Si no existe, crear función simulada
        def procesar_video_plano(plano, video_path):
            print(f"[SERVER] Procesando video {video_path} en plano {plano}")
            # DataFrame simulado
            df = pd.DataFrame({
                0: [0.0, 0.1, 0.2],
                1: [85.0, 86.0, 87.0],
                2: [75.0, 76.0, 77.0],
            })
            return df, df
    
    if hasattr(angles_module, 'calculate_angle'):
        calculate_angle = angles_module.calculate_angle
    
    if hasattr(angles_module, 'angulosxy'):
        angulosxy = angles_module.angulosxy
    
    print("✅ Módulos del proyecto importados correctamente desde src/")
    
except ImportError as e:
    print(f"⚠️ Advertencia: Error importando módulos: {e}")
    print("Usando funciones simuladas...")
    
    # Funciones simuladas
    def procesar_video_plano(plano, video_path):
        print(f"[SIMULADO] Procesando video {video_path} en plano {plano}")
        df = pd.DataFrame({
            0: [0.0, 0.1, 0.2],
            1: [85.0, 86.0, 87.0],
            2: [75.0, 76.0, 77.0],
        })
        return df, df
    
    def calculate_angle(a, b, c):
        return 90.0  # Valor simulado


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PoseAnalysisServicer(pb_grpc.PoseAnalysisServiceServicer):
    """Implementación del servicio de análisis de poses"""
    
    def ProcessVideoStream(self, request_iterator, context):
        """Procesa un stream de video en tiempo real (bidireccional)"""
        logger.info("Nueva conexión de streaming de video")
        
        try:
            for frame_idx, video_frame in enumerate(request_iterator):
                # Decodificar el frame
                nparr = np.frombuffer(video_frame.frame_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if img is None:
                    logger.warning(f"Frame {frame_idx}: No se pudo decodificar")
                    continue
                
                # Procesar el frame (aquí integrarías MediaPipe)
                # Por ahora, creamos datos simulados
                
                # Crear respuesta con landmarks simulados
                result = pb.ProcessedResult()
                result.processing_time_ms = 15  # Tiempo simulado
                
                # Landmarks simulados para hombro izquierdo
                landmark = result.landmarks.add()
                landmark.name = "left_shoulder"
                landmark.x = 0.5
                landmark.y = 0.3 + (frame_idx * 0.01)  # Pequeño movimiento
                landmark.z = 0.1
                landmark.visibility = 0.9
                
                # Landmarks simulados para codo izquierdo
                landmark = result.landmarks.add()
                landmark.name = "left_elbow"
                landmark.x = 0.6
                landmark.y = 0.4 + (frame_idx * 0.01)
                landmark.z = 0.2
                landmark.visibility = 0.8
                
                # Ángulos simulados
                angle = result.angles.add()
                angle.joint_name = "left_elbow"
                angle.angle_xy = 120.5 + frame_idx
                angle.angle_xz = 85.2
                angle.angle_zy = 45.7
                angle.confidence = 0.95
                
                angle = result.angles.add()
                angle.joint_name = "left_shoulder"
                angle.angle_xy = 85.0 + frame_idx * 0.5
                angle.angle_xz = 60.0
                angle.angle_zy = 30.0
                angle.confidence = 0.92
                
                # Enviar resultado al cliente
                yield result
                
                # Log cada 30 frames
                if frame_idx % 30 == 0:
                    logger.info(f"Procesado frame {frame_idx}")
                    
        except Exception as e:
            logger.error(f"Error en streaming: {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
    
    def ProcessVideoFile(self, request, context):
        """Procesa un archivo de video completo"""
        logger.info(f"Procesando archivo: {request.file_path}")
        
        try:
            # Verificar que el archivo existe
            if not os.path.exists(request.file_path):
                error_msg = f"Archivo no encontrado: {request.file_path}"
                logger.error(error_msg)
                return pb.VideoAnalysisResult(
                    file_path=request.file_path,
                    success=False,
                    error_message=error_msg
                )
            
            # Procesar el video usando tu lógica existente
            # Usar el primer plano solicitado, o 'xy' por defecto
            plane = request.planes[0] if request.planes else 'xy'
            
            # Llamar a tu función de procesamiento
            df_angles, df_acceleration = procesar_video_plano(plane, request.file_path)
            
            # Calcular estadísticas
            stats = pb.VideoStatistics(
                mean_angle_xy=float(df_angles[1].mean()) if len(df_angles.columns) > 1 else 0.0,
                max_acceleration=float(df_acceleration.max().max()) if not df_acceleration.empty else 0.0,
                processing_time_seconds=0.0  # Podrías medir el tiempo real
            )
            
            # Crear respuesta
            result = pb.VideoAnalysisResult(
                file_path=request.file_path,
                total_frames=len(df_angles),
                success=True,
                statistics=stats
            )
            
            logger.info(f"Video procesado: {len(df_angles)} frames")
            return result
            
        except Exception as e:
            error_msg = f"Error procesando video: {str(e)}"
            logger.error(error_msg)
            return pb.VideoAnalysisResult(
                file_path=request.file_path,
                success=False,
                error_message=error_msg
            )
    
    def ProcessSensorData(self, request_iterator, context):
        """Procesa stream de datos de sensores IMU"""
        logger.info("Conexión de streaming de sensores IMU")
        
        sensor_buffer = []
        sample_count = 0
        
        try:
            for sensor_data in request_iterator:
                sensor_buffer.append({
                    'accel': sensor_data.accelerometer,
                    'gyro': sensor_data.gyroscope,
                    'timestamp': sensor_data.timestamp,
                    'sensor_id': sensor_data.sensor_id
                })
                
                # Procesar cada 10 muestras
                if len(sensor_buffer) >= 10:
                    # Calcular métricas (simulado por ahora)
                    accel_data = np.array([s['accel'] for s in sensor_buffer])
                    rms_values = np.sqrt(np.mean(accel_data**2, axis=0))
                    
                    # Crear respuesta
                    analysis = pb.SensorAnalysis(
                        timestamp=int(time.time() * 1000),
                        sensor_id=sensor_buffer[0]['sensor_id'],
                        rms_value=float(np.mean(rms_values)),
                        quality_score=0.9,
                        calculated_angles=[float(rms_values[0]), float(rms_values[1]), float(rms_values[2])]
                    )
                    
                    yield analysis
                    
                    sample_count += len(sensor_buffer)
                    sensor_buffer = []
                    
                    if sample_count % 100 == 0:
                        logger.info(f"Procesadas {sample_count} muestras de sensores")
                        
        except Exception as e:
            logger.error(f"Error en streaming de sensores: {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
    
    def CalculateAngles(self, request, context):
        """Calcula ángulos a partir de landmarks"""
        logger.info(f"Cálculo de ángulos para {len(request.landmarks)} landmarks")
        
        try:
            angles = []
            
            # Convertir landmarks a un formato usable
            landmarks_dict = {}
            for landmark in request.landmarks:
                landmarks_dict[landmark.name] = {
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z
                }
            
            # Calcular ángulos (ejemplo simplificado)
            # Aquí integrarías tu lógica real de cálculo de ángulos
            
            start_time = time.time()
            
            # Ángulo simulado para hombro-codo-muñeca izquierdos
            if all(k in landmarks_dict for k in ['left_shoulder', 'left_elbow', 'left_wrist']):
                angle = pb.Angle(
                    joint_name="left_elbow",
                    angle_xy=120.5,
                    angle_xz=85.2,
                    angle_zy=45.7,
                    confidence=0.95
                )
                angles.append(angle)
            
            if all(k in landmarks_dict for k in ['right_shoulder', 'right_elbow', 'right_wrist']):
                angle = pb.Angle(
                    joint_name="right_elbow",
                    angle_xy=110.3,
                    angle_xz=75.1,
                    angle_zy=40.2,
                    confidence=0.93
                )
                angles.append(angle)
            
            processing_time = (time.time() - start_time) * 1000  # ms
            
            return pb.AngleResults(
                angles=angles,
                processing_time_ms=processing_time,
                total_joints_calculated=len(angles)
            )
            
        except Exception as e:
            logger.error(f"Error calculando ángulos: {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return pb.AngleResults()

def serve(port=50051, max_workers=10):
    print("Inicia el servidor gRPC")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    pb_grpc.add_PoseAnalysisServiceServicer_to_server(
        PoseAnalysisServicer(), server
    )
    
    # Escuchar en el puerto especificado
    server_address = f'[::]:{port}'
    server.add_insecure_port(server_address)
    
    logger.info(f"🚀 Iniciando servidor gRPC en {server_address}")
    logger.info(f"📡 Servicios disponibles:")
    logger.info(f"   • ProcessVideoStream (streaming bidireccional)")
    logger.info(f"   • ProcessVideoFile (unario)")
    logger.info(f"   • ProcessSensorData (streaming bidireccional)")
    logger.info(f"   • CalculateAngles (unario)")
    
    server.start()
    
    try:
        # Mantener el servidor corriendo
        while True:
            time.sleep(86400)  # 24 horas
    except KeyboardInterrupt:
        logger.info("👋 Apagando servidor...")
        server.stop(0)
        logger.info("Servidor detenido")

if __name__ == '__main__':
    serve()