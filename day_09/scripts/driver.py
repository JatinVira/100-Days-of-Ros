#! /usr/bin/env python3

# Importing the essential packages
import rospy
import time
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen, SetPenRequest
from turtlesim.srv import TeleportRelative, TeleportRelativeRequest

def teleport_turtle(ser,spr,tser,tspr):
    '''
    Function to teleport thr Robot 
    at the start of screen
    '''

    spr.width = 10
    spr.r = spr.g = spr.b = 255
    spr.off = 1
    ser(spr)

    tspr.linear = -3
    tspr.angular = 0
    tser(tspr)

    spr.width = 10
    spr.r = spr.g = spr.b = 255
    spr.off = 0
    ser(spr)

def draw_R(vel,pub,ser,spr):
    '''
    Function to draw R and goto next point
    '''

    # Take 90 degree turn
    vel.linear.x = 0
    vel.angular.z = 3.1415
    pub.publish(vel)
    time.sleep(0.5)

    # Move Straight
    vel.linear.x = 4
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(0.5)

    # Take -90 degree turn
    vel.linear.x = 0
    vel.angular.z = -3.1415
    pub.publish(vel)
    time.sleep(0.5)

    # SemiCircle
    vel.linear.x = 1.5708
    vel.angular.z = -3.1415
    pub.publish(vel)
    time.sleep(1)

    # Take 135 degree turn
    vel.linear.x = 0
    vel.angular.z = 2.35619
    pub.publish(vel)
    time.sleep(1)

    # Move Straight
    vel.linear.x = 2.8284
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(0.5)

    # Orient for next Point
    vel.linear.x = 0
    vel.angular.z = 0.785398
    pub.publish(vel)
    time.sleep(1)

    # Stop Robot
    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(0.5)

    # Service object modify and call to turn pen off
    spr.off = 1
    (ser(spr))

    # Move to next point
    vel.linear.x = 3
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(0.5)

    # Stop Robot
    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(0.5)

    # Service object modify and call to turn pen on
    spr.width = 10
    spr.r = spr.g = spr.b = 255
    spr.off = 0
    (ser(spr))

def draw_O(vel,pub,ser,spr):
    '''
    Function to draw O and goto next point
    '''

    # O is symmetrical, thus for loop to reduce code
    for i in range(2):

        # Move Straight
        vel.linear.x = 0.5
        vel.angular.z = 0
        pub.publish(vel)
        time.sleep(0.5)

        # Take 90 degree turn
        vel.linear.x = 1.5
        vel.angular.z = 3.1415
        pub.publish(vel)
        time.sleep(0.5)

        # Move Straight
        vel.linear.x = 2.2
        vel.angular.z = 0
        pub.publish(vel)
        time.sleep(0.5)

        # Take 90 degree turn
        vel.linear.x = 1.5
        vel.angular.z = 3.1415
        pub.publish(vel)
        time.sleep(0.5)

        # Move Straight
        vel.linear.x = 0.5
        vel.angular.z = 0
        pub.publish(vel)
        time.sleep(0.5)

    # Stop Robot
    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(0.5)

    # Service call
    spr.off = 1
    (ser(spr))

    # Move to next point
    vel.linear.x = 4
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(0.5)

    # Stop Robot
    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(0.5)

    # Service call
    spr.r = spr.g = spr.b = 255
    spr.off = 0
    (ser(spr))

def draw_S(vel,pub,ser,spr):
    '''
    Function to draw S
    '''

    # Move Straight
    vel.linear.x = 2
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(0.5)

    # Take 180 degree turn
    vel.linear.x = 3
    vel.angular.z = 6.282
    pub.publish(vel)
    time.sleep(0.5)

    # Move Straight
    vel.linear.x = 1.5
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(0.5)

    # Take -180 degree turn
    vel.linear.x = 3
    vel.angular.z = -6.282
    pub.publish(vel)
    time.sleep(0.5)

    # Move Straight
    vel.linear.x = 2
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(0.5)

    # Stop Robot
    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(0.5)

    # Service call
    spr.off = 1
    (ser(spr))

def init_driver():
    '''
    Function to initialize everything
    and also draw basic shapes
    '''

    # Initializing our Node 
    rospy.init_node('Controller', anonymous = True)
    rospy.wait_for_service('/turtle1/set_pen')
    rospy.wait_for_service('/turtle1/teleport_relative')

    # Publishing to topic to move the robot
    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)

    # Setting up service proxy to call service
    ser = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
    tser = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
    spr = SetPenRequest()
    tspr = TeleportRelativeRequest()

    # Create a handshake between Pub and Sub
    vel = Twist()
    vel.linear.x = 0
    vel.angular.z = 0
    pub.publish(vel)
    time.sleep(1)

    # Calling specific functions one after the other
    teleport_turtle(ser,spr,tser,tspr)
    draw_R(vel,pub,ser,spr)
    draw_O(vel,pub,ser,spr)
    draw_S(vel,pub,ser,spr) 

# Main loop starts here
if __name__ == '__main__':
    try:
        init_driver()
    except rospy.ROSInterruptException:
        pass