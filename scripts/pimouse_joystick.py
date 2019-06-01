#!/usr/bin/env python
#encoding: utf8

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse


# ジョイスティックの移動キーに基づきRaspimouseを動作させる
class Joystick():
    def __init__(self):
        # ジョイスティックのキーが押されたら、モータ速度に変換して送信する
        rospy.Subscriber('/joy', Joy, self.joystick_callback)
        self.motor = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.wait_for_service('/motor_on')
        rospy.wait_for_service('/motor_off')
        rospy.on_shutdown(rospy.ServiceProxy('/motor_off', Trigger).call)
        rospy.ServiceProxy('/motor_on', Trigger).call()


    # ジョイスティックが押されたら呼ばれる関数
    def joystick_callback(self, message):
        # 左右の移動速度をleft, rightとする
        # K: 最高移動速度[m/s]
        K = 0.1
        left, right = K * message.axes[1], K * message.axes[4]
        vel = Twist()
        vel.linear.x  = (left + right) / 2.0    # 直進速度[m/s]
        vel.angular.z = (right - left) / 2.0    # 回転速度[m/s]
        vel.angular.z *= 2.0*1000.0/90.0        # 回転速度[rad/s]
        print "linear.x = %5.2f  angular = %5.2f" % (vel.linear.x, vel.angular.z)
        self.motor.publish(vel)


if __name__ == '__main__':
    rospy.init_node('joystick_action')
    joystick = Joystick()
    rospy.spin()
