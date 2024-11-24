import sounddevice as sd
import numpy as np
import asyncio
import speech_recognition as sr
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from concurrent.futures import ThreadPoolExecutor
from fastapi import WebSocket
from queue import Queue
import torch
from starlette.websockets import WebSocketState
import re

current_volume = {"value": 0}

# Hugging Face Whisper 모델 초기화
model_name = "steja/whisper-small-korean"  # 사용할 Whisper 모델
device = "cuda" if torch.cuda.is_available() else "cpu"

processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name).to(device)

# 볼륨 데이터를 WebSocket으로 전송
async def start_audio_stream(websocket: WebSocket):
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=1)

    def audio_callback(indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 20  # 볼륨 크기 계산
        volume_percentage = min(volume_norm, 100)  # 0~100 사이로 정규화

        current_volume["value"] = volume_percentage

        # WebSocket 상태 확인 후 비동기 전송
        loop.run_in_executor(executor, send_volume, websocket, volume_percentage)

    def send_volume(websocket: WebSocket, volume_percentage: float):
        if websocket.application_state == WebSocketState.CONNECTED:
            loop.create_task(websocket.send_text(f"volume:{int(volume_percentage)}"))
        else:
            print("WebSocket disconnected, cannot send volume data.")

    try:
        with sd.InputStream(callback=audio_callback):
            while websocket.application_state == WebSocketState.CONNECTED:
                await asyncio.sleep(0.1)  # 스트림 유지 및 전송 주기
    except Exception as e:
        print(f"Audio stream error: {e}")


# 음성 인식을 수행하고 텍스트 결과를 WebSocket으로 전송
async def start_speech_recognition(websocket: WebSocket):
    loop = asyncio.get_event_loop()
    data_queue = Queue()
    recorder = sr.Recognizer()
    source = sr.Microphone(sample_rate=16000)

    # 주변 소음에 따라 에너지 임계값을 자동으로 조정
    recorder.energy_threshold = 100
    recorder.dynamic_energy_threshold = True
    recorder.dynamic_energy_adjustment_damping = 0.5  # 보정 속도 조정 (낮을수록 빠름)
    
    # 초기 소음 보정
    with source:
        recorder.adjust_for_ambient_noise(source, duration=1)

    def record_callback(_, audio: sr.AudioData):
        data = audio.get_raw_data()
        data_queue.put(data)

    recorder.listen_in_background(source, record_callback, phrase_time_limit=3)

    try:
        while websocket.application_state == WebSocketState.CONNECTED:
            print("current_volume", current_volume["value"])
            if current_volume["value"] >= 20 and not data_queue.empty():
                audio_data = b''.join(data_queue.queue)
                data_queue.queue.clear()

                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                audio_np = audio_np / np.max(np.abs(audio_np))  # 볼륨 정규화

                # Hugging Face Whisper 모델로 음성 텍스트 변환
                input_features = processor.feature_extractor(audio_np, sampling_rate=16000, return_tensors="pt").input_features.to(device)
                predicted_ids = model.generate(input_features)
                text = processor.tokenizer.batch_decode(predicted_ids, skip_special_tokens=True)[0]

                # 한국어 텍스트만 필터링
                # text = re.sub(r"조립폼|조립퐁|조립폭|조립봉|조립공|조리폭", "조리퐁", text)
                # text = re.sub(r"코코 보여주세요", "코코볼 주세요", text)
                # text = re.sub(r"코코벌 주세요", "코코볼 주세요", text)
                # text = re.sub(r"코코별 주세요", "코코볼 주세요", text)
                # text = re.sub(r"해발하기 쉬 주세요", "해바라기씨 주세요", text)
                # text = re.sub(r"해발하기 쉬주세요", "해바라기씨 주세요", text)
                # text = re.sub(r"해발하기 시작", "해바라기씨 주세요", text)
                # text = re.sub(r"해발하기 쉬해주세요", "해바라기씨 주세요", text)
                # text = re.sub(r"해바라기실 주세요", "해바라기씨 주세요", text)
                # text = re.sub(r"회원가이 팔레요|해엉가이 발래요|회원가에 팔레요|해언가에 발래요|회형가에 발래요", "회원가입 할래요.", text)
                # text = re.sub(r"회원다이 발래요|해왕 가이 팔레요|태영가의 발레요|하얀가에 밸래요|배영가이 팔레요", "회원가입 할래요.", text)
                # text = re.sub(r"해발하기 씻으세요|해발하기 시 주세요|회원가에 발래요|회원가에 펄래요|회형가에 팔래요|해완 나이 팔래요|회원가에 팔래요", "회원가입 할래요.", text)
                
                # text = re.sub(r"[^\uac00-\ud7a3\u3131-\u318e]", " ", text)
                print("text: ", text)

                if websocket.application_state == WebSocketState.CONNECTED:
                    await websocket.send_text(f"text:{text}")
            await asyncio.sleep(0.1)
    except Exception as e:
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.send_text(f"error:{str(e)}")
        print(f"Speech recognition error: {e}")
