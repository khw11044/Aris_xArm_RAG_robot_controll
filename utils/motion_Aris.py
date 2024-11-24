from xArm_Python_SDK.xarm.wrapper import XArmAPI
import time
from ultralytics import YOLO

class ArisController:
    def __init__(self, ip_address, angle_speed=65):
        self.ip_address = ip_address
        self.arm = XArmAPI(ip_address)
        self.arm.connect()
        self.tcp_speed = 100
        self.tcp_acc = 2000
        self.angle_speed = angle_speed
        self.angle_acc = 500
        self.init_position = [180.0, 0.0, 6.0, 180.0, 90.0, 180.0, 0.0]
        print("Connected to XArm.")
        
    def move_to_initial_position(self):
        self.arm.set_servo_angle(angle=self.init_position, speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        time.sleep(1)
    
    def Pickup_Ice1(self):
        print("아이스크림을 집는중입니다")
        c_init = self.arm.set_servo_angle(angle = [180.0, 0.0, 6.0, 180.0, 90.0, 180.0, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #1번 위치 아이스크림 잡는 모션(플래닝)
        #오픈
        open_gripper = self.arm.open_lite6_gripper()
        c1 = self.arm.set_servo_angle(angle = [180.271831, 0.120436, 10.520193, 136.153565, 75.540188, 183.65847, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        c2 = self.arm.set_servo_angle(angle = [179.092627, 14.560175, 23.930843, 117.158181, 84.544392, 186.075435, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        c3 = self.arm.set_servo_angle(angle = [197.067802, 37.8846, 49.818279, 126.990939, 78.945907, 190.502909, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        time.sleep(3)
        close_gripper = self.arm.close_lite6_gripper()
        time.sleep(1)
        #올리기
        c4 = self.arm.set_servo_angle(angle = [197.075079, 25.797024, 46.448084, 125.156271, 73.342895, 194.98533, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #초기위치
        c_init = self.arm.set_servo_angle(angle = [180.0, 0.0, 6.0, 180.0, 90.0, 180.0, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
    
    def Pickup_Ice2(self):
        c_init = self.arm.set_servo_angle(angle = [180.0, 0.0, 6.0, 180.0, 90.0, 180.0, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #2번 위치 아이스크림 잡는 모션(플래닝)
        #오픈
        open_gripper = self.arm.open_lite6_gripper()
        #아이스크림 2번위치의 준비자세 
        c34 = self.arm.set_servo_angle(angle = [174.526497, 14.781795, 18.643932, 85.946018, 86.206084, 181.801743, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #아이스크림 2번 잡기 위치
        c35 = self.arm.set_servo_angle(angle = [204.199064, 14.780363, 18.706327, 121.563711, 78.387445, 183.032227, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #클로즈
        time.sleep(3)
        close_gripper = self.arm.close_lite6_gripper()
        time.sleep(1)
        #아이스크림 2번 들어올리기
        c36 = self.arm.set_servo_angle(angle = [204.168411, 10.847925, 20.646076, 118.608394, 82.461576, 190.964369, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #초기위치
        c_init = self.arm.set_servo_angle(angle = [180.0, 0.0, 6.0, 180.0, 90.0, 180.0, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)

    def Pickup_Ice3(self):
        #초기위치
        c_init = self.arm.set_servo_angle(angle = [180.0, 0.0, 6.0, 180.0, 90.0, 180.0, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #3번 위치 아이스크림 잡는 모션(플래닝)
        #오픈
        open_gripper = self.arm.open_lite6_gripper()
        #아이스크림 3번위치의 준비자세 
        c37 = self.arm.set_servo_angle(angle = [195.696485, 0.385314, 12.896764, 71.872571, 82.328821, 192.502475, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #아이스크림 3번 잡기 위치
        c38 = self.arm.set_servo_angle(angle = [219.974712, 11.897068, 13.939891, 99.711902, 80.154446, 180.175803, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #클로즈
        time.sleep(3)
        close_gripper = self.arm.close_lite6_gripper()
        time.sleep(1)
        #아이스크림 3번 들어올리기
        c39 = self.arm.set_servo_angle(angle = [219.969556, 2.967635, 13.98229, 98.2068, 84.187324, 190.733639, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #초기위치
        c_init = self.arm.set_servo_angle(angle = [180.0, 0.0, 6.0, 180.0, 90.0, 180.0, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)

    def deliverIceCream(self):
        ###아이스크림 프레스기로 이동, 컵 잡아서 토핑 이니셜 위치###
        #---------------------------------------------------------------------------------------------
        #초기위치
        c_init = self.arm.set_servo_angle(angle = [180.0, 0.0, 6.0, 180.0, 90.0, 180.0, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #올려서 이동(high 위치)
        c5 = self.arm.set_servo_angle(angle = [179.995264, -4.367084, 162.402882, 183.570578, -68.243399, 168.255646, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #뒤로 빼기
        c6 = self.arm.set_servo_angle(angle = [115.220781, -19.187612, 162.725858, 196.567381, -81.111171, 170.310043, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)

        #프레스기 앞
        c7 = self.arm.set_servo_angle(angle = [156.064307, -1.859535, 241.676004, 102.843002, -104.360939, 118.58645, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #프레스기 넣기
        c8 = self.arm.set_servo_angle(angle = [196.122995, -1.854378, 243.947095, 84.781482, -74.180617, 118.048099, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #프레스기 빼고난 후 컵 잡기 전
        time.sleep(3)
        open_gripper = self.arm.open_lite6_gripper()
        time.sleep(3)
        #프레스기에서 빼면서 살짝 아래로 내림
        c8_1 = self.arm.set_servo_angle(angle = [187.510121, 2.060815, 247.396931, 87.319341, -80.552652, 112.752708, 0.0], speed=self.angle_speed, mvacc=-self.angle_acc, wait=False, radius=0.0)
        #프레스기 앞
        c7 = self.arm.set_servo_angle(angle = [156.064307, -1.859535, 241.676004, 102.843002, -104.360939, 118.58645, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        # 프레스기 빼고난 후 컵 잡기 전
        c9 = self.arm.set_servo_angle(angle = [170.265467, -6.548621, 289.561697, 271.702889, -75.12359, 303.12378, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        # #컵잡기직전 중간위치
        c9_1 = self.arm.set_servo_angle(angle = [186.519936, -24.964344, 290.365671, 282.875967, -86.242696, 316.911608, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #컵 잡기 위치
        c10 = self.arm.set_servo_angle(angle = [169.70901, -44.394432, 283.368252, 262.243642, -84.603865, 327.15088, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #그리퍼 잡기
        time.sleep(8)
        close_gripper = self.arm.close_lite6_gripper()
        time.sleep(7)
        #프레스기 빼고난 후 컵 잡기 전
        c9 = self.arm.set_servo_angle(angle = [169.78613, -20.864888, 282.953947, 272.966318, -85.423252, 302.750211, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #중간위치
        c11 = self.arm.set_servo_angle(angle = [159.937845, -6.545126, 282.027302, 167.222889, -99.078383, 267.703873, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #토핑 이니셜 포지션 (토핑 받기위한 wayPoi6nt)
        # c12 = self.arm.set_servo_angle(angle = [164.703937, -6.539282, 281.734578, 97.45972, -99.09666, 256.992198, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        # c13 = self.arm.set_servo_angle(angle = [196.380482, -3.136142, 268.77645, 91.010736, -68.788167, 269.296867, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)

    def IceCreamPress(self):
        
        c13_center = self.arm.set_servo_angle(angle = [196.057162, -6.976792, 261.88646, 92.163699, -73.370454, 269.588388, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        press = self.arm.set_cgpio_digital(3,5, delay_sec=0)   #0은 up, 5는 down
        time.sleep(7)
        c13_down = self.arm.set_servo_angle(angle = [196.057162, -16.219748, 268.626507, 96.764837, -74.623628, 253.007391, 0.0], speed=self.angle_speed, mvacc=-self.angle_acc, wait=False, radius=0.0)
        c13_center = self.arm.set_servo_angle(angle = [196.057162, -6.976792, 261.88646, 92.163699, -73.370454, 269.588388, 0.0], speed=15, mvacc=self.angle_acc, wait=False, radius=0.0)
        c13_middle = self.arm.set_servo_angle(angle = [196.057162, -8.158862, 263.374145, 92.957418, -73.489801, 266.805761, 0.0], speed=15, mvacc=self.angle_acc, wait=False, radius=0.0)
        press = self.arm.set_cgpio_digital(3,0, delay_sec=0)   #0은 up, 5는 down
        #         # 오른쪽
        # c13_1 = [196.414745, -10.337247, 268.037048, 95.013305, -73.609836, 259.663499, 0.0]

        # # 앞(사용자랑 가까운쪽)
        # c13_2 = [197.414671, -12.143096, 265.806981, 95.053297, -72.586591, 260.014378, 0.0]

        # # 왼쪽
        # c13_3 = [195.772287, -12.803831, 265.065058, 94.761604, -74.200441, 260.24402, 0.0]

        # # 뒤쪽 (기계랑 가까운쪽)
        # c13_4 = [194.278701, -11.16053, 267.138707, 94.634293, -75.709497, 259.925283, 0.0]

        # # 동작 수행 함수
        # def move_to_position(angle):
        #     self.arm.set_servo_angle(angle=angle, speed=7, mvacc=self.angle_acc, wait=False, radius=0.0)
        #     # time.sleep(1)  # 동작 간격

        # # 순차적으로 동작 수행
        # print("아이스크림을 받고 있는중입니다")
        # c13_center = self.arm.set_servo_angle(angle = [196.057162, -11.689714, 266.419301, 94.876253, -73.939516, 259.970547, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)

        # press = self.arm.set_cgpio_digital(3,5, delay_sec=0)   #0은 up, 5는 down

        # time.sleep(11)

        # for i in range(5):
        #     move_to_position(c13_1)
        #     move_to_position(c13_2)
        #     move_to_position(c13_3)
        #     move_to_position(c13_4)

        # press = self.arm.set_cgpio_digital(3,0, delay_sec=0)   #0은 up, 5는 down
    
    
    def topping1(self):
        ###3시나리오. (토핑받기) 컵 토핑 이니셜 위치이동 후 토핑3을 받고 다시 토핑 이니셜로 돌아온다 ###
        #---------------------------------------------------------------------------------------------
        #토핑 이니셜 포지션 (토핑 받기위한 wayPoint)
        c12 = self.arm.set_servo_angle(angle = [164.703937, -6.539282, 281.734578, 97.45972, -99.09666, 256.992198, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #아이스크림 받는 위치
        c13 = self.arm.set_servo_angle(angle = [196.380482, -3.136142, 268.77645, 91.010736, -68.788167, 269.296867, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #토핑3 배출 위치(wayPoint)
        c14_topping_3 = self.arm.set_servo_angle(angle = [216.398482, 6.109162, 279.785547, 89.055174, -99.984745, 272.922372, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #토핑2 배출 위치(wayPoint)
        c15_topping_2 = self.arm.set_servo_angle(angle = [257.590079, 7.545969, 279.679607, 93.098136, -86.114525, 269.143085, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #토핑1 배출 위치
        c16_topping_1 = self.arm.set_servo_angle(angle = [298.158069, 3.990536, 275.73783, 94.284674, -46.105971, 266.912847, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        time.sleep(2)
        t6 = self.arm.set_cgpio_digital(0,5, delay_sec=0)   #토핑나옴
        print("시리얼을 받고 있는중입니다")
        time.sleep(6)
        t5 = self.arm.set_cgpio_digital(0,0, delay_sec=0)   #토핑닫기
        time.sleep(1)
        #토핑2 배출 위치(wayPoint)
        c15_topping_2 = self.arm.set_servo_angle(angle = [257.590079, 7.545969, 279.679607, 93.098136, -86.114525, 269.143085, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #토핑3 배출 위치(wayPoint)
        c14_topping_3 = self.arm.set_servo_angle(angle = [216.398482, 6.109162, 279.785547, 89.055174, -99.984745, 272.922372, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        
        controller.IceCreamPress()
        #아이스크림 받는 위치
        # c13 = self.arm.set_servo_angle(angle = [196.380482, -3.136142, 268.77645, 91.010736, -68.788167, 269.296867, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        # print("아이스크림을 받고 있는중입니다")
        # press = self.arm.set_cgpio_digital(3,5, delay_sec=0)   #0은 up, 5는 down
        # time.sleep(18)
        # press = self.arm.set_cgpio_digital(3,0, delay_sec=0)   #0은 up, 5는 down
        # c12 = self.arm.set_servo_angle(angle = [164.703937, -6.539282, 281.734578, 97.45972, -99.09666, 256.992198, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        
    def topping2(self):
        ###3시나리오. (토핑받기) 컵 토핑 이니셜 위치이동 후 토핑3을 받고 다시 토핑 이니셜로 돌아온다 ###
        #---------------------------------------------------------------------------------------------
        #토핑 이니셜 포지션 (토핑 받기위한 wayPoint)
        c12 = self.arm.set_servo_angle(angle = [164.703937, -6.539282, 281.734578, 97.45972, -99.09666, 256.992198, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #아이스크림 받는 위치
        c13 = self.arm.set_servo_angle(angle = [196.380482, -3.136142, 268.77645, 91.010736, -68.788167, 269.296867, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #토핑3 배출 위치(wayPoint)
        c14_topping_3 = self.arm.set_servo_angle(angle = [216.398482, 6.109162, 279.785547, 89.055174, -99.984745, 272.922372, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #토핑2 배출 위치
        c15_topping_2 = self.arm.set_servo_angle(angle = [257.590079, 7.545969, 279.679607, 93.098136, -86.114525, 269.143085, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        
        time.sleep(2)
        t6 = self.arm.set_cgpio_digital(1,5, delay_sec=0)   #토핑나옴
        time.sleep(5)
        print("코코볼을 받고 있는중입니다")
        t5 = self.arm.set_cgpio_digital(1,0, delay_sec=0)   #토핑닫기
        time.sleep(1)
        # 토핑3 배출 위치(wayPoint)
        c14_topping_3 = self.arm.set_servo_angle(angle = [216.398482, 6.109162, 279.785547, 89.055174, -99.984745, 272.922372, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        
        controller.IceCreamPress()
        
        # #아이스크림 받는 위치
        # c13 = self.arm.set_servo_angle(angle = [196.380482, -3.136142, 268.77645, 91.010736, -68.788167, 269.296867, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        # print("아이스크림을 받고 있는중입니다")
        # press = self.arm.set_cgpio_digital(3,5, delay_sec=0)   #0은 up, 5는 down
        # time.sleep(18)
        # press = self.arm.set_cgpio_digital(3,0, delay_sec=0)   #0은 up, 5는 down
        # c12 = self.arm.set_servo_angle(angle = [164.703937, -6.539282, 281.734578, 97.45972, -99.09666, 256.992198, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)

    def topping3(self):
        ###3시나리오. (토핑받기) 컵 토핑 이니셜 위치이동 후 토핑3을 받고 다시 토핑 이니셜로 돌아온다 ###
        #---------------------------------------------------------------------------------------------
        #토핑 이니셜 포지션 (토핑 받기위한 wayPoint)
        c12 = self.arm.set_servo_angle(angle = [164.703937, -6.539282, 281.734578, 97.45972, -99.09666, 256.992198, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #아이스크림 받는 위치
        c13 = self.arm.set_servo_angle(angle = [196.380482, -3.136142, 268.77645, 91.010736, -68.788167, 269.296867, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #토핑3 배출 위치
        c14_topping_3 = self.arm.set_servo_angle(angle = [216.398482, 6.109162, 279.785547, 89.055174, -99.984745, 272.922372, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        
        time.sleep(2)
        t6 = self.arm.set_cgpio_digital(2,5, delay_sec=0)   #토핑나옴
        print("코코볼을 받고 있는중입니다")
        time.sleep(6)
        t5 = self.arm.set_cgpio_digital(2,0, delay_sec=0)   #토핑닫기
        time.sleep(1)
        #아이스크림 받는 위치
        c13 = self.arm.set_servo_angle(angle = [196.380482, -3.136142, 268.77645, 91.010736, -68.788167, 269.296867, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        
        controller.IceCreamPress()
        # #아이스크림 받는 위치
        # print("아이스크림을 받고 있는중입니다")
        # press = self.arm.set_cgpio_digital(3,5, delay_sec=0)   #0은 up, 5는 down
        # time.sleep(18)
        # press = self.arm.set_cgpio_digital(3,0, delay_sec=0)   #0은 up, 5는 down
        # #중간위치
        # c12 = self.arm.set_servo_angle(angle = [164.703937, -6.539282, 281.734578, 97.45972, -99.09666, 256.992198, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
    
    def ice1_Putback(self):
        #원점복귀 포인트1(20
        c17 = self.arm.set_servo_angle(angle = [61.054898, 4.08771, 281.742084, 80.639627, -98.295608, 256.33301, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #원점복귀 포인트2
        c18 = self.arm.set_servo_angle(angle = [12.513971, -41.749601, 248.260894, 90.96679, -81.459014, 248.170195, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #아이스크림 완전 놓기
        c19 = self.arm.set_servo_angle(angle = [11.14718, -48.580748, 244.928399, 92.373058, -85.496533, 244.32496, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        time.sleep(2)
        open_gripper = self.arm.open_lite6_gripper()
        open_gripper
        print("\n아이스크림이 완성 되었습니다 맛있게 드세요!")
        time.sleep(4)
        c20 = self.arm.set_servo_angle(angle = [9.914634, -47.534641, 245.223186, 83.595001, -84.796149, 244.995092, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #뒤로 빼기
        c21 = self.arm.set_servo_angle(angle = [-2.072675, -47.534126, 246.107375, 81.969004, -92.720041, 245.104985, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)

    def ice2_Putback(self):
        #원점복귀 포인트1(20
        c17 = self.arm.set_servo_angle(angle = [61.054898, 4.08771, 281.742084, 80.639627, -98.295608, 256.33301, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #원점복귀 포인트2
        c_2putdown_1 = self.arm.set_servo_angle(angle = [17.597768, -34.224832, 281.746495, 93.416758, -86.938496, 225.681143, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #아이스크림 완전 놓기
        open_gripper = self.arm.open_lite6_gripper()
        open_gripper
        print("\n아이스크림이 완성 되었습니다 맛있게 드세요!")
        time.sleep(6)
        c_2putdown_2 = self.arm.set_servo_angle(angle = [-2.279856, -34.223743, 281.837195, 77.816148, -100.932302, 221.737073, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)        
        time.sleep(1)
        
    def ice3_Putback(self):
        #원점복귀 포인트1(20
        c17 = self.arm.set_servo_angle(angle = [61.054898, 4.08771, 281.742084, 80.639627, -98.295608, 256.33301, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #원점복귀 포인트2
        c_3putdown_1 = self.arm.set_servo_angle(angle = [42.68421, -21.987255, 284.121921, 74.487321, -93.905663, 232.844261, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #아이스크림 완전 놓기
        open_gripper = self.arm.open_lite6_gripper()
        open_gripper
        print("\n아이스크림이 완성 되었습니다 맛있게 드세요!")
        time.sleep(4)
        c_3putdown_2 = self.arm.set_servo_angle(angle = [21.518347, -21.986625, 279.282204, 64.061265, -102.580244, 227.395031, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)  
        time.sleep(1)
    
    
    def pressEnd(self):
        ###4시나리오.아이스크림 받고, 서빙하고, 쓰레기 치우기###
        #---------------------------------------------------------------------------------------------
        c22 = self.arm.set_servo_angle(angle = [-4.243669, 9.390263, 183.614524, 90.73606, -1.226817, 277.00928, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #회전1
        #아이스크림 치우러 가기
        c24 = self.arm.set_servo_angle(angle = [-1.095782, 10.921951, 102.279555, 100.118416, -89.79492, 348.112827, 0.0]
        , speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #회전2
        c25 = self.arm.set_servo_angle(angle = [-7.312488, 10.922696, 85.395864, 25.949717, 6.079082, 356.517316, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #아이스크림 쓰레기 잡는 위치 앞
        c26 = self.arm.set_servo_angle(angle = [-24.553361, 10.899548, 77.012403, 78.717067, 114.637739, 242.45729, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #아이스크림 쓰레기 집는 직전위치
        c27 = self.arm.set_servo_angle(angle = [3.354324, -3.667044, 69.282114, 96.108399, 81.221007, 246.741925, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #아이스크림 집는 위치
        c28 = self.arm.set_servo_angle(angle = [15.348451, -3.664466, 68.615248, 100.052468, 70.555112, 246.302524, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        time.sleep(5)
        close_gripper = self.arm.close_lite6_gripper()
        close_gripper
        time.sleep(5)

        #안에서 살짝 들어올림
        c29 = self.arm.set_servo_angle(angle = [15.217816, -3.66968, 73.088616, 100.382091, 70.600891, 249.532459, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #밖으로 완전 쓰레기 빼기
        c30 = self.arm.set_servo_angle(angle = [-21.875529, -3.665497, 72.155325, 85.462671, 108.059668, 252.081319, 0.0]
        , speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)

        #아이스크림 쓰레기 잡는 위치 앞
        c26 = self.arm.set_servo_angle(angle = [-24.553361, 10.899548, 77.012403, 78.717067, 114.637739, 242.45729, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)

        #아이스크림 버리는 직전 위치
        c31 = self.arm.set_servo_angle(angle = [15.720816, 11.34783, 46.803203, 83.613679, 67.871091, 215.661199, 0.0]
        , speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)

        #아이스크림 회전시켜 버리기
        c32 = self.arm.set_servo_angle(angle = [16.149675, 10.658734, 45.975566, 85.953868, 70.395772, 41.909055, 0.0]
        , speed=self.angle_speed + 30, mvacc=self.angle_acc + 20, wait=False, radius=0.0)

        open_gripper = self.arm.open_lite6_gripper()
        open_gripper

        #원위치로 돌아오기
        #아이스크림 쓰레기 잡는 위치 앞
        c26 = self.arm.set_servo_angle(angle = [-24.553361, 10.899548, 77.012403, 78.717067, 114.637739, 242.45729, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #쓰레기 집으러 가기
        c22 = self.arm.set_servo_angle(angle = [-4.243669, 9.390263, 183.614524, 90.73606, -1.226817, 277.00928, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #회전
        c33 = self.arm.set_servo_angle(angle = [161.348811, 4.602914, 182.115838, -76.79445, -1.304625, 282.854023, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #원점
        c_init = self.arm.set_servo_angle(angle = [180.0, 0.0, 6.0, 180.0, 90.0, 180.0, 0.0], speed=self.angle_speed, mvacc=self.angle_acc, wait=False, radius=0.0)
        #그리퍼 전원off
        stop_gripper = self.arm.stop_lite6_gripper()
        
        #컵빼기
        cup1 = self.arm.set_cgpio_analog(0,5)
        cup1
        time.sleep(15)
        cup2 = self.arm.set_cgpio_analog(1,5)
        cup2
        time.sleep(15)
        cup3 = self.arm.set_cgpio_analog(0,0)
        cup3
        time.sleep(12)
        cup4 = self.arm.set_cgpio_analog(1,0)
        cup4
    
    def ToppingChoice(self, choice):
        if choice == "코코볼" :
            controller.topping1()
        
        elif choice == "아몬드":
            controller.topping2()
                
        elif choice in ["시리얼", "씨리얼"]:
            controller.topping3()

        else:
            print("1,2,3 중에 선택해주세요.")
    
    def IceCreamPosition(self, position):
        
        if position == 1:
            print("\n1번 위치 아이스크림을 집는중")
            controller.Pickup_Ice1()

        elif position == 2:
            print("\n2번 위치 아이스크림을 집는중")
            controller.Pickup_Ice2()

        elif position == 3:
            print("\n3번 위치 아아스크림을 집는중")
            controller.Pickup_Ice3()
        
        else:
            print("1,2,3 포지션에 아이스크림을 놓아 주세요")

    def IceCreamPutback(self, putback):

        if putback == 1:
            print("\n 1번 아이스크림 위치에 서빙")
            controller.ice1_Putback()
        
        elif putback == 2:
            print("\n 2번 아이스크림 위치에 서빙")
            controller.ice2_Putback()
        
        elif putback == 3:
            print("\n 3번 아이스크림 위치에 서빙")
            controller.ice3_Putback()

        

    def run_all_scenarios(self):
        self.ice1()
        self.deliverIceCream()
        self.topping3()
        self.pressEnd()

controller = ArisController('192.168.1.167')