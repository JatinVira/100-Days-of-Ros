#!/usr/bin/env python3

# Importing essential ROS packages
import rospy
from turtlesim.msg import Pose
from turtlesim.srv import TeleportRelative, TeleportRelativeRequest
from turtlesim.srv import TeleportAbsolute, TeleportAbsoluteRequest
from geometry_msgs.msg import Twist

# Importing Math package for Pi
import math

# Using Random package to generate new angle in range
from random import uniform

# Variables to store ball's location (x,y,theta)
ball_x = 0.0
ball_y = 0.0
ball_theta = 0.0

# Variables to store right_turtle's location (x,y,theta)
right_x = 0.0
right_y = 0.0
right_theta = 0.0

# Variables to store left_turtle's location (x,y,theta)
left_x = 0.0
left_y = 0.0
left_theta = 0.0

# Variables to store Right and Left player score's
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
    teleport_turtle = rospy.ServiceProxy("/Ball/teleport_absolute", TeleportAbsolute)
    teleport_turtle_request = TeleportAbsoluteRequest()

    teleport_turtle_request.x = x
    teleport_turtle_request.y = y
    teleport_turtle_request.theta = theta

    teleport_turtle(teleport_turtle_request)


def Teleport_Turtle_Relative(linear_translate, angular_translate):
    teleport_turtle = rospy.ServiceProxy("/Ball/teleport_relative", TeleportRelative)
    teleport_turtle_request = TeleportRelativeRequest()

    teleport_turtle_request.linear = linear_translate
    teleport_turtle_request.angular = angular_translate

    teleport_turtle(teleport_turtle_request)


def callback(data):
    global ball_x, ball_y, ball_theta
    ball_x = data.x
    ball_y = data.y
    ball_theta = data.theta


def callback2(data):
    global right_x, right_y, right_theta
    right_x = data.x
    right_y = data.y
    right_theta = data.theta


def callback3(data):
    global left_x, left_y, left_theta
    left_x = data.x
    left_y = data.y
    left_theta = data.theta


def init():
    """
    Function to initialize everything
    """

    # Accessing global variables
    global ball_x, ball_y, ball_theta
    global right_x, right_y, right_theta
    global left_x, left_y, left_theta

    # Create a ROS node called as 'ball_node'
    rospy.init_node("ball_node", anonymous=True)

    # Wait for services to start before proceeding further
    rospy.wait_for_service("/Ball/teleport_relative")

    pub = rospy.Publisher("/Ball/cmd_vel", Twist, queue_size=10)
    sub = rospy.Subscriber("/Ball/pose", Pose, callback)
    sub2 = rospy.Subscriber("/Right/pose", Pose, callback2)
    sub3 = rospy.Subscriber("/Left/pose", Pose, callback3)
    ball_vel = Twist()

    rate = rospy.Rate(10)  # 10hz

    while not rospy.is_shutdown():
        if ball_x >= 10.5 and ball_theta == 0.0:
            Teleport_Turtle_Relative(1.0, math.radians(150))
            increment_right_score()
            reset_and_print_scores()

        if ball_x >= 10.5 and ball_theta > 0.0:
            Teleport_Turtle_Relative(1.0, (2 * math.pi / 3))
            increment_right_score()
            reset_and_print_scores()

        if ball_x >= 10.5 and ball_theta < 0.0:
            Teleport_Turtle_Relative(1.0, (-2 * math.pi / 3))
            increment_right_score()
            reset_and_print_scores()

        if ball_x <= 0.5 and ball_theta == 0.0:
            Teleport_Turtle_Relative(1.0, math.radians(150))
            increment_left_score()
            reset_and_print_scores()

        if ball_x <= 0.5 and ball_theta < 0.0:
            Teleport_Turtle_Relative(1.0, (2 * math.pi / 3))
            increment_left_score()
            reset_and_print_scores()

        if ball_x <= 0.5 and ball_theta > 0.0:
            Teleport_Turtle_Relative(1.0, (-2 * math.pi / 3))
            increment_left_score()
            reset_and_print_scores()

        if ball_y <= 0.5 and ball_theta > -1.57:
            Teleport_Turtle_Relative(0.5, (math.pi / 3))

        if ball_y <= 0.5 and ball_theta < -1.57:
            Teleport_Turtle_Relative(0.5, (-math.pi / 3))

        if ball_y >= 10.5 and ball_theta < 1.57:
            Teleport_Turtle_Relative(0.5, (-math.pi / 3))

        if ball_y >= 10.5 and ball_theta > 1.57:
            Teleport_Turtle_Relative(0.5, (math.pi / 3))

        if (abs(ball_x - right_x)) < 0.5 and (abs(ball_y - right_y)) < 0.5:
            frand = uniform(-1, 1)
            Teleport_Turtle_Absolute(ball_x, ball_y, frand)

        if (abs(ball_x - left_x)) < 0.5 and (abs(ball_y - left_y)) < 0.5:
            frand = uniform(1.6, 3.7)
            Teleport_Turtle_Absolute(ball_x, ball_y, frand)

        ball_vel.linear.x = 1.5
        ball_vel.angular.z = 0.0
        pub.publish(ball_vel)
        rate.sleep()


if __name__ == "__main__":
    """
    Main Function
    """
    try:
        init()
    except rospy.ROSInterruptException:
        pass
