# aris-repo-2


얼굴인식 + 고객등록 + 음성인식 + 채팅 + 객체탐지 + 로봇제어

## 현재 최종 

xArm-Python-SDK를 다운받고 venv로 가상환경 만들어주세요.

```
python3 -m venv xarm

source xarm/bin/activate 

git clone https://github.com/xArm-Developer/xArm-Python-SDK.git

mv xArm-Python-SDK xArm_Python_SDK

cd xArm_Python_SDK

python setup.py install

cd .. 
```

아나콘다 가상환경은 안되더라구요

그리고 아래 pip를 수행해주세요

pip install 전에 portaudio 설치를 위해 아래 명령어를 수행해야함

sudo apt update

sudo apt install portaudio19-dev

### torch install 먼저 하기 

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121


> pip install -r requirements.txt


### uvicorn 실행

> uvicorn app.main:app --reload


![스크린샷 2024-11-20 17-06-36](https://github.com/user-attachments/assets/9195ad5a-59ef-479d-9f6d-cf79d7b8783e)



