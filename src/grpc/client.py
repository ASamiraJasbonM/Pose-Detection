# src/grpc/client.py (importaciones corregidas)
import grpc
import cv2
import threading
import queue
import time
from datetime import datetime
from typing import Optional, Generator, List, Dict, Any


import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))

import pose_analysis_pb2 as pb
import pose_analysis_pb2_grpc as pb_grpc

print("Import exitosa")

class PoseAnalysisClient:
    """Cliente gRPC para el servicio de análisis de poses"""
    
    def __init__(self, server_address: str = 'localhost:50051'):
        """
        Inicializa el cliente gRPC.
        
        Args:
            server_address: Dirección del servidor (ej: 'localhost:50051')
        """
        self.server_address = server_address
        self.channel = None
        self.stub = None
        self.video_stream = None
        self.sensor_stream = None
        self.video_results_queue = queue.Queue()
        self.sensor_results_queue = queue.Queue()
        self.is_video_streaming = False
        self.is_sensor_streaming = False
        
        self._connect()
    
    def _connect(self):
        """Establece conexión con el servidor"""
        try:
            print(f"🔗 Conectando a servidor gRPC en {self.server_address}...")
            self.channel = grpc.insecure_channel(self.server_address)
            self.stub = pb_grpc.PoseAnalysisServiceStub(self.channel)
            
            # Test de conexión
            grpc.channel_ready_future(self.channel).result(timeout=5)
            print("✅ Conexión establecida exitosamente")
            
        except grpc.FutureTimeoutError:
            print(f"❌ No se pudo conectar al servidor en {self.server_address}")
            print("   Asegúrate de que el servidor esté corriendo")
            raise
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            raise
    
    def start_video_stream(self, camera_index: int = 0, fps: int = 30):
        """
        Inicia streaming de video desde una cámara.
        
        Args:
            camera_index: Índice de la cámara (0 para cámara por defecto)
            fps: Frames por segundo para captura
        """
        if self.is_video_streaming:
            print("⚠️ El streaming de video ya está activo")
            return
        
        print(f"🎬 Iniciando streaming desde cámara {camera_index}...")
        
        # Crear generador de frames
        def frame_generator(cam_index: int, target_fps: int) -> Generator[pb.VideoFrame, None, None]:
            """Genera frames de video para enviar al servidor"""
            cap = cv2.VideoCapture(cam_index)
            if not cap.isOpened():
                print(f"❌ No se pudo abrir cámara {cam_index}")
                return
            
            cap.set(cv2.CAP_PROP_FPS, target_fps)
            frame_count = 0
            last_time = time.time()
            
            try:
                while self.is_video_streaming:
                    ret, frame = cap.read()
                    if not ret:
                        print("⚠️ No se pudo leer frame de la cámara")
                        break
                    
                    # Codificar frame como JPEG (85% calidad para balance)
                    encode_params = [cv2.IMWRITE_JPEG_QUALITY, 85]
                    success, encoded_frame = cv2.imencode('.jpg', frame, encode_params)
                    
                    if not success:
                        print("⚠️ No se pudo codificar frame")
                        continue
                    
                    # Crear mensaje gRPC
                    video_frame = pb.VideoFrame(
                        frame_data=encoded_frame.tobytes(),
                        timestamp=int(time.time() * 1000),
                        frame_number=frame_count
                    )
                    
                    yield video_frame
                    frame_count += 1
                    
                    # Control de FPS
                    elapsed = time.time() - last_time
                    sleep_time = max(0, (1.0 / target_fps) - elapsed)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                    last_time = time.time()
                    
            finally:
                cap.release()
                print("📷 Cámara liberada")
        
        # Iniciar streaming bidireccional
        self.is_video_streaming = True
        self.video_stream = self.stub.ProcessVideoStream(
            frame_generator(camera_index, fps)
        )
        
        # Hilo para recibir resultados
        self.video_receiver_thread = threading.Thread(
            target=self._receive_video_results,
            daemon=True
        )
        self.video_receiver_thread.start()
        
        print("✅ Streaming de video iniciado")
    
    def _receive_video_results(self):
        """Recibe resultados del streaming de video"""
        try:
            for result in self.video_stream:
                # Poner resultado en la cola para procesamiento
                self.video_results_queue.put(result)
                
                # Opcional: procesar inmediatamente
                self._process_video_result(result)
                
        except grpc.RpcError as e:
            print(f"❌ Error en streaming de video: {e.code()}: {e.details()}")
            self.is_video_streaming = False
        except Exception as e:
            print(f"❌ Error recibiendo resultados: {e}")
            self.is_video_streaming = False
    
    def _process_video_result(self, result: pb.ProcessedResult):
        """Procesa un resultado de video recibido"""
        # Puedes personalizar este método según tus necesidades
        if result.angles:
            angles_str = ", ".join([
                f"{angle.joint_name}: {angle.angle_xy:.1f}°"
                for angle in result.angles[:2]  # Mostrar solo los primeros 2
            ])
            print(f"📐 Ángulos: {angles_str}")
    
    def stop_video_stream(self):
        """Detiene el streaming de video"""
        if self.is_video_streaming:
            print("🛑 Deteniendo streaming de video...")
            self.is_video_streaming = False
            
            # Cerrar el stream
            if hasattr(self, 'video_stream') and self.video_stream:
                self.video_stream.cancel()
            
            print("✅ Streaming de video detenido")
    
    def process_video_file(self, file_path: str, planes: List[str] = None) -> Optional[pb.VideoAnalysisResult]:
        """
        Procesa un archivo de video completo.
        
        Args:
            file_path: Ruta al archivo de video
            planes: Lista de planos a procesar (ej: ['xy', 'xz'])
        
        Returns:
            Resultado del análisis o None si hay error
        """
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            return None
        
        print(f"🎞️ Enviando archivo para procesamiento: {file_path}")
        
        request = pb.VideoFileRequest(
            file_path=file_path,
            processing_mode="normal",
            planes=planes or ["xy", "xz", "zy"]
        )
        
        try:
            # Llamada unaria (request-response)
            start_time = time.time()
            response = self.stub.ProcessVideoFile(request)
            processing_time = time.time() - start_time
            
            if response.success:
                print(f"✅ Video procesado en {processing_time:.2f}s")
                print(f"   • Frames: {response.total_frames}")
                print(f"   • Ángulo medio: {response.statistics.mean_angle_xy:.1f}°")
                print(f"   • Máx aceleración: {response.statistics.max_acceleration:.2f}")
            else:
                print(f"❌ Error procesando video: {response.error_message}")
            
            return response
            
        except grpc.RpcError as e:
            print(f"❌ Error gRPC: {e.code()}: {e.details()}")
            return None
        except Exception as e:
            print(f"❌ Error procesando video: {e}")
            return None
    
    def start_sensor_stream(self, sensor_id: str = "default_sensor"):
        """
        Inicia streaming de datos de sensores.
        
        Args:
            sensor_id: Identificador del sensor
        """
        if self.is_sensor_streaming:
            print("⚠️ El streaming de sensores ya está activo")
            return
        
        print(f"📡 Iniciando streaming de sensores ({sensor_id})...")
        
        # Crear stream bidireccional
        self.sensor_stream = self.stub.ProcessSensorData()
        self.is_sensor_streaming = True
        
        # Hilo para recibir análisis
        self.sensor_receiver_thread = threading.Thread(
            target=self._receive_sensor_results,
            daemon=True
        )
        self.sensor_receiver_thread.start()
        
        print("✅ Streaming de sensores iniciado")
    
    def send_sensor_data(self, accelerometer: List[float], gyroscope: List[float], 
                        sensor_id: str = "default_sensor"):
        """
        Envía datos de sensores al servidor.
        
        Args:
            accelerometer: Datos del acelerómetro [x, y, z]
            gyroscope: Datos del giroscopio [x, y, z]
            sensor_id: Identificador del sensor
        """
        if not self.is_sensor_streaming:
            print("⚠️ El streaming de sensores no está activo")
            return
        
        sensor_data = pb.SensorData(
            accelerometer=accelerometer,
            gyroscope=gyroscope,
            timestamp=int(time.time() * 1000),
            sensor_id=sensor_id
        )
        
        try:
            self.sensor_stream.send(sensor_data)
        except Exception as e:
            print(f"❌ Error enviando datos de sensores: {e}")
            # Intentar reconectar
            self.stop_sensor_stream()
            self.start_sensor_stream(sensor_id)
    
    def _receive_sensor_results(self):
        """Recibe resultados del análisis de sensores"""
        try:
            for analysis in self.sensor_stream:
                # Poner resultado en la cola
                self.sensor_results_queue.put(analysis)
                
                # Procesar inmediatamente
                self._process_sensor_result(analysis)
                
        except grpc.RpcError as e:
            print(f"❌ Error en streaming de sensores: {e.code()}: {e.details()}")
            self.is_sensor_streaming = False
        except Exception as e:
            print(f"❌ Error recibiendo análisis de sensores: {e}")
            self.is_sensor_streaming = False
    
    def _process_sensor_result(self, analysis: pb.SensorAnalysis):
        """Procesa un resultado de análisis de sensores"""
        print(f"📊 Sensor {analysis.sensor_id}: "
              f"RMS={analysis.rms_value:.3f}, "
              f"Calidad={analysis.quality_score:.2f}")
    
    def stop_sensor_stream(self):
        """Detiene el streaming de sensores"""
        if self.is_sensor_streaming:
            print("🛑 Deteniendo streaming de sensores...")
            self.is_sensor_streaming = False
            
            if hasattr(self, 'sensor_stream') and self.sensor_stream:
                self.sensor_stream.close()
            
            print("✅ Streaming de sensores detenido")
    
    def calculate_angles(self, landmarks: Dict[str, Dict[str, float]], 
                        plane: str = "xy") -> Optional[pb.AngleResults]:
        """
        Calcula ángulos a partir de landmarks.
        
        Args:
            landmarks: Diccionario con landmarks {nombre: {x, y, z}}
            plane: Plano para cálculo ('xy', 'xz', 'zy')
        
        Returns:
            Resultados del cálculo o None si hay error
        """
        print(f"📐 Calculando ángulos para {len(landmarks)} landmarks...")
        
        # Crear request
        request = pb.AngleCalculationRequest(plane=plane)
        
        for name, coords in landmarks.items():
            landmark = request.landmarks.add()
            landmark.name = name
            landmark.x = coords.get('x', 0.0)
            landmark.y = coords.get('y', 0.0)
            landmark.z = coords.get('z', 0.0)
            landmark.visibility = coords.get('visibility', 1.0)
        
        try:
            response = self.stub.CalculateAngles(request)
            
            print(f"✅ {response.total_joints_calculated} ángulos calculados "
                  f"en {response.processing_time_ms:.1f}ms")
            
            for angle in response.angles:
                print(f"   • {angle.joint_name}: "
                      f"XY={angle.angle_xy:.1f}°, "
                      f"XZ={angle.angle_xz:.1f}°, "
                      f"ZY={angle.angle_zy:.1f}° "
                      f"(conf: {angle.confidence:.2f})")
            
            return response
            
        except grpc.RpcError as e:
            print(f"❌ Error calculando ángulos: {e.code()}: {e.details()}")
            return None
    
    def close(self):
        """Cierra todas las conexiones y streams"""
        print("🔒 Cerrando conexiones...")
        
        self.stop_video_stream()
        self.stop_sensor_stream()
        
        if self.channel:
            self.channel.close()
        
        print("✅ Cliente cerrado")

# Función de conveniencia para crear cliente
def create_client(server_address: str = 'localhost:50051') -> PoseAnalysisClient:
    """Crea y retorna un cliente gRPC"""
    return PoseAnalysisClient(server_address)

# Ejemplo de uso
if __name__ == "__main__":
    # Prueba básica del cliente
    client = None
    
    try:
        client = create_client()
        
        # Probar cálculo de ángulos
        landmarks = {
            "left_shoulder": {"x": 0.5, "y": 0.3, "z": 0.1},
            "left_elbow": {"x": 0.6, "y": 0.4, "z": 0.2},
            "left_wrist": {"x": 0.7, "y": 0.5, "z": 0.3},
            "right_shoulder": {"x": 0.4, "y": 0.3, "z": 0.1},
            "right_elbow": {"x": 0.3, "y": 0.4, "z": 0.2},
            "right_wrist": {"x": 0.2, "y": 0.5, "z": 0.3},
        }
        
        client.calculate_angles(landmarks)
        
        print("\n✅ Prueba completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
    finally:
        if client:
            client.close()