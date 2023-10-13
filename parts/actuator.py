# -*- coding: utf-8 -*-
"""
コントローラ/AI入力値をGPIOピン値に変換するパーツクラス。
"""
from donkeycar.parts.actuator import TwoWheelSteeringThrottle

class CaterpillerMotorDriver(object):
    def __init__(self, left_balance=1.0, right_balance=1.0, debug=False):
        """
        donkeycarパッケージのTwoWheelSteeringThrottleインスタンスを生成する。

        引数：
            left_balance    float       左PWM値に積算される値(0から1.0の範囲内)
            right_balance   float       右PWM値に積算される値(0から1.0の範囲内)
            debug           boolean     デバッグ表示有無（デフォルト:False）
        戻り値：
            なし
        """
        self.twowheel = TwoWheelSteeringThrottle()
        self.set_left_balance(left_balance)
        self.set_right_balance(right_balance)
        self.debug = debug

    def set_left_balance(self, left_balance):
        #if left_balance is None or left_balance < 0 or left_balance > 1:
        #    raise ValueError('[CaterpillerMD] left_balance:{} out of range [0.0, 1.0]'.format(str(left_balance)))
        self.left_balance = self.to_range_value(left_balance)
    
    def set_right_balance(self, right_balance):
        #if right_balance is None or right_balance < 0 or right_balance > 1:
        #    raise ValueError('[CaterpillerMD] right_balance:{} out of range [0.0, 1.0]'.format(str(right_balance)))
        self.right_balance = self.to_range_value(right_balance)

    def run(self, throttle, steering):
        """
        コントローラの入力値(スロットル、ステアリング、リフト：-1.0～1.0)を
        GPIOピン出力値に変換する。

        引数： 
            throttle        float   スロットル値（-1.0～1.0）
            steering        float   ステアリング値（-1.0～1.0）
        戻り値：
            left_verf       float   左モータVref値（0.0～1.0）
            left_in1        int     左モータIN1値（0もしくは1）
            left_in2        int     左モータIN2値（0もしくは1）
            right_verf       float   左モータVref値（0.0～1.0）
            right_in1        int     左モータIN1値（0もしくは1）
            right_in2        int     左モータIN2値（0もしくは1）
        """
        if self.debug:
            print('[CaterpillerMD] orig throttle:{}, steering:{}'.format(str(throttle), str(steering)))
        throttle, steering = self.to_range_value(throttle), self.to_range_value(steering)

        if self.debug:
            print('[CaterpillerMD] conv throttle:{}, steering:{}'.format(str(throttle), str(steering)))

        left_motor_speed, right_motor_speed = self.twowheel.run(throttle, steering)
        left_motor_speed, right_motor_speed = self.to_range_value(left_motor_speed), self.to_range_value(right_motor_speed)

        if self.debug:
            print('[CaterpillerMD] left motor speed:{}, right motor speed:{}'.format(str(left_motor_speed), str(right_motor_speed)))

        left_pwm, left_in1, left_in2 = self.convert_pin_values(left_motor_speed)
        right_pwm, right_in1, right_in2 = self.convert_pin_values(right_motor_speed)

        left_pwm = self.to_range_value(left_pwm * self.left_balance)
        right_pwm = self.to_range_value(right_pwm * self.right_balance)

        if self.debug:
            print('[CaterpillerMD]  left   pwm:{}, in1:{}, in2:{}'.format(str(left_pwm), str(left_in1), str(left_in2)))
            print('[CaterpillerMD]  right  pwm:{}, in1:{}, in2:{}'.format(str(right_pwm), str(right_in1), str(right_in2)))

        return left_pwm, left_in1, left_in2, right_pwm, right_in1, right_in2
    
    def convert_pin_values(self, motor_speed):
        """
        モータ速度(-1.0～1.0)をPWM, IN1, IN2 のピン出力値に変換する。

        引数：
            motor_speed         モータ速度(-1.0～1.0)
        戻り値：
            pwm     float       PWM値(PWM:0.0～1.0)
            in1     int         IN1値(0か1)
            in2     int         IN2値(0か1)
        """
        # 停止
        in1 = 0
        in2 = 0
        pwm = max(min(abs(float(motor_speed)), 1.0), 0.0)
        # 正転
        if motor_speed > 0:
            in1 = 1
        # 逆転
        elif motor_speed < 0:
            in2 = 1
        return pwm, in1, in2

    def to_range_value(self, value):
        if value is None:
            return 0.0
        elif value > 1.0:
            return 1.0
        elif value < -1.0:
            return -1.0
        else:
            return float(value)

    def shutdown(self):
        """
        シャットダウン時にTwoWheelSteeringThrottleのシャットダウン処理を呼び出す。

        引数：
            なし
        戻り値：
            なし
        """
        self.twowheel.shutdown()

