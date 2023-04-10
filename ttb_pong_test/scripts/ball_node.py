#!/usr/bin/env python3

import rospy, time, math
from turtlesim.msg import Pose
from turtlesim.srv import TeleportRelative, TeleportRelativeRequest
from turtlesim.srv import TeleportAbsolute, TeleportAbsoluteRequest
from geometry_msgs.msg import Twist

from random import uniform

ball_x = 0.0
ball_y = 0.0
ball_theta = 0.0

right_x = 0.0
right_y = 0.0
right_theta = 0.0

left_x = 0.0
left_y = 0.0
left_theta = 0.0

right_turtle_score = 0
left_turtle_score = -1

def reset_and_print_scores():
    global right_turtle_score, left_turtle_score
    print("Ball out of bound! Reset!")
    print("Current Score")
    print("Right:", right_turtle_score, " Left:", left_turtle_score)

def increment_right_score():
    global right_turtle_score
    right_turtle_score = right_turtle_score + 1

def increment_left_score():
    global left_turtle_score
    left_turtle_score = left_turtle_score + 1

def Teleport_Turtle_Absolute(x, y, theta):
    teleport_turtle = rospy.ServiceProxy('/Ball/teleport_absolute', TeleportAbsolute)
    teleport_turtle_request = TeleportAbsoluteRequest()

    teleport_turtle_request.x = x
    teleport_turtle_request.y = y
    teleport_turtle_request.theta = theta

    teleport_turtle(teleport_turtle_request)

def Teleport_Turtle_Relative(linear_translate, angular_translate):
    teleport_turtle = rospy.ServiceProxy('/Ball/teleport_relative', TeleportRelative)
    teleport_turtle_request = TeleportRelativeRequest()

    teleport_turtle_request.linear = linear_translate
    teleport_turtle_request.angular = angular_translate

    teleport_turtle(teleport_turtle_request)

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
    rospy.wait_for_service('/Ball/teleport_relative')

    pub = rospy.Publisher('/Ball/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/Ball/pose', Pose, callback)
    sub2 = rospy.Subscriber('/Right/pose', Pose, callback2)
    sub3 = rospy.Subscriber('/Left/pose', Pose, callback3)
    ball_vel = Twist()

    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        if (ball_x >= 10.5 and ball_theta == 0.0):
            # ball_vel.linear.x = 1.0
            # ball_vel.angular.z = ball_theta + math.radians(100)
            # pub.publish(ball_vel)
            # time.sleep(1)
            # print("1st condn")            
            Teleport_Turtle_Relative(1.0, math.radians(150))
            increment_right_score()
            reset_and_print_scores()

        if (ball_x >= 10.5 and ball_theta > 0.0):
            # ball_vel.linear.x = 0.5
            # ball_vel.angular.z = ball_theta + math.radians(160)
            # pub.publish(ball_vel)
            # rate.sleep()
            # print("1st condn 1 sec")
            Teleport_Turtle_Relative(1.0, (2*math.pi/3))
            increment_right_score()
            reset_and_print_scores()


        if (ball_x >= 10.5 and ball_theta < 0.0):
            # ball_vel.linear.x = 0.5
            # ball_vel.angular.z = ball_theta - math.radians(160)
            # pub.publish(ball_vel)
            # rate.sleep()
            # print("1st condn 2 sec")
            Teleport_Turtle_Relative(1.0, (-2*math.pi/3))
            increment_right_score()
            reset_and_print_scores()

        if (ball_x <= 0.5 and ball_theta == 0.0):
            # ball_vel.linear.x = 1.0
            # ball_vel.angular.z = ball_theta + math.radians(100)
            # pub.publish(ball_vel)
            # time.sleep(1)
            # print("2nd condn")
            Teleport_Turtle_Relative(1.0, math.radians(150))
            increment_left_score()
            reset_and_print_scores()

        if (ball_x <= 0.5 and ball_theta < 0.0):
            # ball_vel.linear.x = 1.0
            # ball_vel.angular.z = ball_theta + math.radians(230)
            # pub.publish(ball_vel)
            # rate.sleep()
            # print("2nd condn 2 sec")
            Teleport_Turtle_Relative(1.0, (2*math.pi/3))
            increment_left_score()
            reset_and_print_scores()

        if (ball_x <= 0.5 and ball_theta > 0.0):
            # ball_vel.linear.x = 1.0
            # ball_vel.angular.z = ball_theta - math.radians(230)
            # pub.publish(ball_vel)
            # rate.sleep()
            # print("2nd condn 1 sec")
            Teleport_Turtle_Relative(1.0, (-2*math.pi/3))
            increment_left_score()
            reset_and_print_scores()

        if (ball_y <= 0.5 and ball_theta > -1.57):
            # ball_vel.linear.x = 0.5
            # ball_vel.angular.z = ball_theta + math.radians(160)
            # pub.publish(ball_vel)
            # rate.sleep()
            # print("3rd condn ")
            Teleport_Turtle_Relative(0.5, (math.pi/3))

        if (ball_y <= 0.5 and ball_theta < -1.57):
            # ball_vel.linear.x = 0.5
            # ball_vel.angular.z = ball_theta - math.radians(160)
            # pub.publish(ball_vel)
            # rate.sleep()
            # print("3rd condn 2 sec")
            Teleport_Turtle_Relative(0.5, (-math.pi/3))

        if (ball_y >= 10.5 and ball_theta < 1.57):
            # ball_vel.linear.x = 0.5
            # ball_vel.angular.z = ball_theta - math.radians(160)
            # pub.publish(ball_vel)
            # rate.sleep()
            # print("4th condn ")
            Teleport_Turtle_Relative(0.5, (-math.pi/3))

        if (ball_y >= 10.5 and ball_theta > 1.57):
            # ball_vel.linear.x = 0.5
            # ball_vel.angular.z = ball_theta + math.radians(160)
            # pub.publish(ball_vel)
            # rate.sleep()
            # print("4th condn 2 sec ")
            Teleport_Turtle_Relative(0.5, (math.pi/3))

        if ((abs(ball_x-right_x)) < 0.5 and (abs(ball_y-right_y))< 0.5):
            # print("Right Collision")
            # ball_vel.linear.x = 0.6
            # ball_vel.angular.z = -ball_theta
            # pub.publish(ball_vel)
            # rate.sleep()
            # Teleport_Turtle_Relative(0.6, (math.pi/3))
            frand = uniform(-1, 1)
            Teleport_Turtle_Absolute(ball_x, ball_y, frand)

        if ((abs(ball_x-left_x)) < 0.5 and (abs(ball_y-left_y)) < 0.5):
            # print("Left Collision")
            # ball_vel.linear.x = 0.5
            # ball_vel.angular.z = -ball_theta
            # pub.publish(ball_vel)
            # rate.sleep()
            # Teleport_Turtle_Relative(0.6, (math.pi/3))
            frand = uniform(1.6, 3.7)
            Teleport_Turtle_Absolute(ball_x, ball_y, frand)

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