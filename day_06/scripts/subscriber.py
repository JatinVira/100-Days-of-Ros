#!/usr/bin/env python3

from py_compile import main
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo("I heard " + data.data)

def Subscriber():
    rospy.init_node('listner', anonymous=False)
    rospy.Subscriber('chatter', String, callback)
    rospy.spin()

if __name__ == '__main__':
    Subscriber()