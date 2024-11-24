from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.audio_service import start_audio_stream, start_speech_recognition
import asyncio
from starlette.websockets import WebSocketState
from utils.ActionGlobal import get_action_state


router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cur_act = get_action_state()
    if not cur_act:
        try:
            # asyncio.gather로 두 비동기 작업 병렬 실행
            await asyncio.gather(
                start_audio_stream(websocket),
                start_speech_recognition(websocket)
            )
        except WebSocketDisconnect:
            print("WebSocket disconnected by client.")
        except asyncio.CancelledError:
            print("Async task was cancelled.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            # WebSocket 상태 확인 후 안전하게 닫기
            if websocket.application_state == WebSocketState.CONNECTED:
                try:
                    await websocket.close()
                except RuntimeError as e:
                    print(f"Error during WebSocket close: {e}")
            print("WebSocket closed cleanly.")
