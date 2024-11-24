from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from concurrent.futures import ThreadPoolExecutor
from app.services.face_service import FaceService
from app.services.detection_service import CupDetection
import cv2
import asyncio
import base64
import json

executor = ThreadPoolExecutor(max_workers=2)
router = APIRouter()
face_service = FaceService()
cup_detection = CupDetection()  # CupDetection 초기화

@router.websocket("/ws/stream/{camera_id}")
async def camera_stream(websocket: WebSocket, camera_id: int):
    """WebSocket을 통해 특정 카메라 스트림을 제공합니다."""
    await websocket.accept()
    # print(f"Client connected for Camera {camera_id} stream.")

    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        await websocket.send_text(json.dumps({"error": "Failed to open camera"}))
        await websocket.close()
        return

    frame_count = 0
    
    try:
        while True:
            ret, frame = await asyncio.get_event_loop().run_in_executor(executor, cap.read)
            if not ret:
                await websocket.send_text(json.dumps({"error": "Failed to capture frame"}))
                break

            if camera_id == 0:  # 1번 카메라만 얼굴 탐지 및 인식 수행
                processed_frame = face_service.process_frame(frame, frame_count)
                labels = face_service.previous_labels

                if frame_count % 30 == 0:
                    frame_count = 0
                    if "Unknown" in labels:
                        face_service.trigger_recognition()

                _, buffer = cv2.imencode('.jpg', processed_frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')

                response = {
                    "frame": frame_base64,
                    "label": labels[0] if labels else "None"
                }
            elif camera_id == 4:
                position, processed_frame = cup_detection.detect_position(frame)
                if position is not None:
                    await websocket.send_text(f"컵 위치 확인 {position}.")
                
                # print('position:',position)
                _, buffer = cv2.imencode('.jpg', processed_frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                response = {"frame": frame_base64}
                    
            else:
                _, buffer = cv2.imencode('.jpg', frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                response = {"frame": frame_base64}

            await websocket.send_text(json.dumps(response))
            await asyncio.sleep(0.033)

    except WebSocketDisconnect:
        print(f"Client disconnected from Camera {camera_id} stream.")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        cap.release()
        if camera_id == 0:
            face_service.close()
