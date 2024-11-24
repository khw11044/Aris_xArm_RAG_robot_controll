# from xArm_Python_SDK.xarm.wrapper import XArmAPI
# import time  

# # 로봇 초기화 함수
# def initialize_arm(ip_address='192.168.1.162'):
#     arm = XArmAPI(ip_address)
#     arm.connect('connect!')
#     arm.motion_enable(True)
#     arm.set_mode(0)
#     arm.set_state(0)
#     return arm

# # 초기 위치 설정
# def set_initial_position(arm, angle_speed=5, angle_acc=50):
#     print("Moving to initial position...")
    
#     pos = arm.get_position()[1]
#     print(pos)
#     # arm.set_servo_angle(angle=[pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], 0.0], speed=angle_speed, mvacc=angle_acc, wait=False, radius=0.0)

    
# def stop_topping_motor(arm):
#     arm.set_cgpio_digital(0,0, delay_sec=0) #토핑닫기
#     time.sleep(1)

#     arm.set_cgpio_digital(1,0, delay_sec=0) #토핑닫기
#     time.sleep(1)

#     arm.set_cgpio_digital(2,0, delay_sec=0) #토핑닫기
#     time.sleep(1)


# arm = initialize_arm(ip_address='192.168.1.162')


# set_initial_position(arm)
# stop_topping_motor(arm)

from utils.motion_Aris import ArisController
controller = ArisController('192.168.1.167',angle_speed=5)


controller.move_to_initial_position()

# from xArm_Python_SDK.xarm.wrapper import XArmAPI

# arm = XArmAPI('192.168.1.167')
# arm.connect('connect!')

# tcp_speed = 100
# tcp_acc = 2000
# angle_speed = 65
# angle_acc = 500

# p0 = arm.get_servo_angle()
# print(p0)