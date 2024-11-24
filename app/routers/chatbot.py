# app/routers/chatbot.py
import asyncio 
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
from app.services.rag_service import RagPipeline
from app.services.robot_service import process_order_response_async  # 함수 임포트
from app.services.face_service import get_global_embeddings
from app.services.signin_service import SignInService
from langchain_community.chat_message_histories import SQLChatMessageHistory
from utils.CupPosition import get_cup_position



router = APIRouter()
rag_pipeline = RagPipeline()  # RAG 파이프라인 인스턴스 생성
signin_service = SignInService()

# ThreadPoolExecutor 생성 (최대 2개의 스레드 사용)
executor = ThreadPoolExecutor(max_workers=2)

# 요청 데이터 구조 정의
class ChatRequest(BaseModel):
    question: str
    session_id: str

class SaveMessageRequest(BaseModel):
    session_id: str
    message: str
    
class DeleteSessionRequest(BaseModel):
    session_id: str

# SQLChatMessageHistory 설정
def get_chat_history(session_id: str):
    return SQLChatMessageHistory(
        table_name='chat_history',
        session_id=session_id,
        connection="sqlite:///sqlite.db"
    )

async def async_generate_answer(question: str, session_id: str):
    """RAG 모델 응답을 별도 스레드에서 비동기로 실행"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, rag_pipeline.generate_answer, question, session_id)

# 예외 처리가 추가된 백그라운드 작업 함수
async def run_process_order_response(response_text: str):
    try:
        await process_order_response_async(response_text)
    except Exception as e:
        print(f"Error in background task: {e}")

@router.post("/chat")
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    try:
        print('[사용자]')
        print(request.question)

        answer = await async_generate_answer(request.question, session_id=request.session_id)
        response_text = answer["answer"]
        
        print('[AI]')
        print(response_text)
        
        # "회원가입이 완료되었습니다" 포함 여부 확인
        if "회원가입이 완료되었습니다" in response_text and request.session_id == "Unknown":
            embeddings = get_global_embeddings()  # 전역 상태에서 임베딩 가져오기
            if embeddings is not None:
                print('DB에 넣기 성공')
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(executor, signin_service.handle_signup_with_embedding, embeddings)

        lines = response_text.strip().split("\n")
        last_line = lines[-1].strip()
        if "주문되었습니다." in last_line:
            position = get_cup_position()
            if position == None:
                response_text = "아이스크림이 없어요. 아이스크림을 올려주세요."
            else:
                #비동기로 로봇 제어 함수 실행
                background_tasks.add_task(run_process_order_response, response_text)
                
        return {"answer": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("/save_message")
async def save_message(request: SaveMessageRequest):
    """
    SQL 데이터베이스에 사용자의 메시지를 저장합니다.
    """
    try:
        chat_message_history = get_chat_history(request.session_id)
        chat_message_history.add_ai_message(request.message)
        messages = chat_message_history.messages
        print(messages)
        return {"message": "User message saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save message: {str(e)}")


@router.post("/delete_session")
async def delete_session(request: DeleteSessionRequest):
    """
    특정 세션의 모든 대화 기록을 SQL 데이터베이스에서 삭제합니다.
    """
    try:
        chat_message_history = get_chat_history(request.session_id)
        chat_message_history.clear()  # 해당 세션의 모든 메시지 삭제
        return {"message": f"Session {request.session_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")