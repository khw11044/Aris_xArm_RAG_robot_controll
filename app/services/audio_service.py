import sounddevice as sd
import numpy as np
import asyncio
import speech_recognition as sr
from concurrent.futures import ThreadPoolExecutor
from fastapi import WebSocket
from starlette.websockets import WebSocketState
from queue import Queue
from collections import deque

executor = ThreadPoolExecutor(max_workers=2)  # 음성 인식과 기타 작업을 병렬 실행
# volume_queue = Queue()  # SoundDevice 콜백과 asyncio 간 데이터 전달용 큐
volume_queue = deque(maxlen=5) 
# 볼륨 데이터를 WebSocket으로 전송
async def start_audio_stream(websocket: WebSocket):
    """
    마이크 입력 볼륨을 실시간으로 계산하여 WebSocket으로 전송.
    """
    def audio_callback(indata, frames, time, status):
        """
        SoundDevice 콜백에서 볼륨 계산 후 큐에 추가.
        """
        volume_norm = np.linalg.norm(indata)**3 # 볼륨 크기 계산
        volume_percentage = min(volume_norm, 100)  # 0~100 사이로 정규화
        # volume_queue.put(volume_percentage)  # 큐에 볼륨 데이터 추가
        if volume_percentage > 2: 
            volume_queue.extend([volume_percentage]*5)
        else:
            volume_queue.append(volume_percentage)

    try:
        with sd.InputStream(callback=audio_callback):
            while websocket.application_state == WebSocketState.CONNECTED:
                # 큐에서 볼륨 데이터 가져오기
                # 최근 볼륨 데이터의 평균값 계산
                if len(volume_queue) > 0:
                    avg_volume = sum(volume_queue) / len(volume_queue)
                else:
                    avg_volume = 0
                
                # print('Average volume:', avg_volume)  # 디버깅 출력
                if websocket.application_state == WebSocketState.CONNECTED:
                    await websocket.send_text(f"volume:{int(avg_volume)}")  # 평균값 전송
                
                await asyncio.sleep(0.1)  # 스트림 유지
    except Exception as e:
        print(f"Audio stream error: {e}")


# 음성 인식을 수행하고 텍스트 결과를 WebSocket으로 전송
async def start_speech_recognition(websocket: WebSocket):
    """
    Google Speech-to-Text를 사용하여 음성을 텍스트로 변환 후 WebSocket으로 전송.
    """
    recognizer = sr.Recognizer()

    def recognize_speech_from_microphone():
        """
        Google Speech-to-Text를 사용하여 음성을 텍스트로 변환.
        """
        with sr.Microphone(sample_rate=16000) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("음성 인식 대기 중...")
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                return recognizer.recognize_google(audio, language="ko-KR")
            except sr.UnknownValueError:
                return "음성을 이해하지 못했습니다."
            except sr.RequestError as e:
                return f"STT 서비스 오류: {e}"

    while websocket.application_state == WebSocketState.CONNECTED:
        try:
            # 음성 인식을 별도 스레드에서 실행
            text = await asyncio.get_event_loop().run_in_executor(executor, recognize_speech_from_microphone)
            if websocket.application_state == WebSocketState.CONNECTED and text:
                await websocket.send_text(f"text:{text}")
        except Exception as e:
            print(f"Speech recognition error: {e}")
            if websocket.application_state == WebSocketState.CONNECTED:
                await websocket.send_text(f"error:{str(e)}")
        await asyncio.sleep(0.1)
