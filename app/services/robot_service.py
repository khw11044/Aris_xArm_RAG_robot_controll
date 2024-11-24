from utils.motion_Aris import ArisController
import asyncio
from utils.CupPosition import get_cup_position
from utils.CupPosition import set_cup_position
from app.routers.notification import send_notification
from utils.ActionGlobal import set_action_state, get_action_state

# ArisController 초기화
controller = ArisController('192.168.1.167')

# 주문 응답을 처리하고 로봇 동작을 수행하는 비동기 함수
async def process_order_response_async(response_text):
    # 주문 응답을 라인별로 분리
    lines = response_text.strip().split("\n")
    last_line = lines[-1].strip()
    

    # 주문 완료 여부 확인
    if "주문되었습니다." in last_line:
        set_action_state(True)

        choice = None  # 선택된 토핑 초기화
        for line in lines[:-1]:
            line = line.strip()
            print(f"Processed line: {line}")

            # 토핑 종류 분석
            if "코코볼" in line or "코코" in line or "코코별" in line:
                choice = "코코볼"
                print("인식된 토핑: 코코볼")
                break
            elif "아몬드" in line:
                choice = "아몬드"
                print("인식된 토핑: 해바라기씨")
                break
            elif "시리얼" in line or "씨리얼" in line:
                choice = "씨리얼"
                print("인식된 토핑: 조리퐁")
                break
            else:
                print("Invalid topping. Skipping.")

        if choice is None:
            print("Error: No valid topping selected.")
            return  # 토핑이 없으면 종료
        
        #    position = get_cup_position()
        position = get_cup_position()
        if position is None:
            print("Error: Could not detect cup position.")
            return  # 위치가 없으면 종료
        
        # 로봇 동작 수행
        print("Starting robot actions...")
        # await asyncio.to_thread(controller.move_to_initial_position())
        await asyncio.to_thread(controller.IceCreamPosition, position)
        await asyncio.to_thread(controller.deliverIceCream)
        await asyncio.to_thread(controller.ToppingChoice, choice)
        await asyncio.to_thread(controller.IceCreamPutback, position)
        # await send_notification("아이스크림 제조가 완료되었습니다.") # WebSocket 알림 전송
        print("아이스크림이 완료되었습니다. 맛있게 드세요.")
        await asyncio.to_thread(controller.pressEnd)
        await send_notification("아이스크림 제조가 완료되었습니다. 감사합니다. 또 오세요!")
        print("감사합니다.")
        set_cup_position(None)  # 컵위치 None으로 
        set_action_state(False)
        

    else:
        print("Error: Order not completed.")
