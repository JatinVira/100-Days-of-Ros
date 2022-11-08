#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen, SetPenRequest, SetPenResponse
import time

def draw_R(vel,pub,ser,spr):
    vel.linear.x = 3
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(1)

    spr.off = 1
    (ser(spr))

    vel.linear.x = 3
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(1)

def init_driver():
    rospy.init_node('Controller', anonymous = True)
    rospy.wait_for_service('/turtle1/set_pen')
    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    ser = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
    spr = SetPenRequest()

    vel = Twist()
    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(1)

    draw_R(vel,pub,ser,spr)
    # draw_O()
    # draw_S()

if __name__ == '__main__':
    init_driver()

'''
rosservice info /turtle1/set_pen 
Node: /turtlesim
URI: rosrpc://Edith:53177
Type: turtlesim/SetPen
Args: r g b width off
'''
