#!/usr/bin/env python3

import rospy, time, math
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

ball_x = 0.0
ball_y = 0.0
ball_theta = 0.0

right_x = 0.0
right_y = 0.0
right_theta = 0.0

left_x = 0.0
left_y = 0.0
left_theta = 0.0

def callback(data):
    global ball_x, ball_y, ball_theta
    ball_x = data.x
    ball_y = data.y
    ball_theta = data.theta
    # print(ball_x, ball_y, ball_theta)

def callback2(data):
    global right_x, right_y, right_theta
    right_x = data.x
    right_y = data.y
    right_theta = data.theta
    # print(right_x, right_y, right_theta)

def callback3(data):
    global left_x, left_y, left_theta
    left_x = data.x
    left_y = data.y
    left_theta = data.theta
    # print(ball_x, ball_y, ball_theta)

def init():
    global ball_x, ball_y, ball_theta
    global right_x, right_y, right_theta
    global left_x, left_y, left_theta

    rospy.init_node('ball_node', anonymous=True)
    pub = rospy.Publisher('/Ball/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/Ball/pose', Pose, callback)
    sub2 = rospy.Subscriber('/Right/pose', Pose, callback2)
    sub3 = rospy.Subscriber('/Left/pose', Pose, callback3)
    ball_vel = Twist()

    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        if (ball_x >= 10.5 and ball_theta == 0.0):
            ball_vel.linear.x = 1.0
            ball_vel.angular.z = ball_theta + math.radians(100)
            pub.publish(ball_vel)
            time.sleep(1)
            print("1st condn")

        if (ball_x >= 10.5 and ball_theta > 0.0):
            ball_vel.linear.x = 0.5
            ball_vel.angular.z = ball_theta + math.radians(160)
            pub.publish(ball_vel)
            rate.sleep()
            print("1st condn 1 sec")

        if (ball_x >= 10.5 and ball_theta < 0.0):
            ball_vel.linear.x = 0.5
            ball_vel.angular.z = ball_theta - math.radians(160)
            pub.publish(ball_vel)
            rate.sleep()
            print("1st condn 2 sec")

        if (ball_x <= 0.5 and ball_theta == 0.0):
            ball_vel.linear.x = 1.0
            ball_vel.angular.z = ball_theta + math.radians(100)
            pub.publish(ball_vel)
            time.sleep(1)
            print("2nd condn")

        if (ball_x <= 0.5 and ball_theta < 0.0):
            ball_vel.linear.x = 1.0
            ball_vel.angular.z = ball_theta + math.radians(230)
            pub.publish(ball_vel)
            rate.sleep()
            print("2nd condn 2 sec")

        if (ball_x <= 0.5 and ball_theta > 0.0):
            ball_vel.linear.x = 1.0
            ball_vel.angular.z = ball_theta - math.radians(230)
            pub.publish(ball_vel)
            rate.sleep()
            print("2nd condn 1 sec")

        if (ball_y <= 0.5 and ball_theta > -1.57):
            ball_vel.linear.x = 0.5
            ball_vel.angular.z = ball_theta + math.radians(160)
            pub.publish(ball_vel)
            rate.sleep()
            print("3rd condn ")

        if (ball_y <= 0.5 and ball_theta < -1.57):
            ball_vel.linear.x = 0.5
            ball_vel.angular.z = ball_theta - math.radians(160)
            pub.publish(ball_vel)
            rate.sleep()
            print("3rd condn 2 sec")

        if (ball_y >= 10.5 and ball_theta < 1.57):
            ball_vel.linear.x = 0.5
            ball_vel.angular.z = ball_theta - math.radians(160)
            pub.publish(ball_vel)
            rate.sleep()
            print("4th condn ")

        if (ball_y >= 10.5 and ball_theta > 1.57):
            ball_vel.linear.x = 0.5
            ball_vel.angular.z = ball_theta + math.radians(160)
            pub.publish(ball_vel)
            rate.sleep()
            print("4th condn 2 sec ")

        if ((abs(ball_x-right_x)) < 0.5 and (abs(ball_y-right_y))< 0.5):
            print("Right Collision")
            ball_vel.linear.x = 0.5
            ball_vel.angular.z = -ball_theta
            pub.publish(ball_vel)
            rate.sleep()

        if ((abs(ball_x-left_x)) < 0.5 and (abs(ball_y-left_y)) < 0.5):
            print("Left Collision")
            ball_vel.linear.x = 0.5
            ball_vel.angular.z = -ball_theta
            pub.publish(ball_vel)
            rate.sleep()

        ball_vel.linear.x = 1.5
        ball_vel.angular.z = 0.0
        pub.publish(ball_vel)
        rate.sleep()

    # rospy.spin()

if __name__ == '__main__':
    try:
        init()
    except rospy.ROSInterruptException:
        pass