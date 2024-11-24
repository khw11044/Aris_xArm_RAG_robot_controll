from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()
active_connections: List[WebSocket] = []


@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket 연결을 통해 클라이언트와 통신합니다.
    클라이언트가 연결되면 active_connections에 추가됩니다.
    """
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # 클라이언트로부터 데이터를 기다리지만, 여기에선 필요 없음
            await websocket.receive_text()
    except WebSocketDisconnect:
        # 연결이 끊어지면 active_connections에서 제거
        active_connections.remove(websocket)


async def send_notification(message: str):
    """
    활성화된 모든 WebSocket 연결로 알림 메시지를 전송합니다.
    """
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            # 메시지 전송 실패 시 연결 제거
            print(f"Error sending notification: {e}")
            active_connections.remove(connection)
