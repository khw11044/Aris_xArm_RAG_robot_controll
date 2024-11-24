import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import stream, chatbot, audio, notification
# from app.routers.notification import router as notification_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Static files 설정
app.mount("/static", StaticFiles(directory=os.path.join(os.getcwd(), "static")), name="static")

# 라우터 등록
app.include_router(audio.router)
app.include_router(stream.router)  # 스트림 라우터 추가
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(notification.router)

# index.html 서빙
@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open(os.path.join(os.getcwd(), "static", "index.html")) as f:
        return HTMLResponse(content=f.read(), status_code=200)
