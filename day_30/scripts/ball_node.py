#!/usr/bin/env python3

# Importing Math package for Pi
import math

# Using Random package to generate new angle in range
from random import uniform

# Importing essential ROS packages
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import (
    TeleportAbsolute,
    TeleportAbsoluteRequest,
    TeleportRelative,
    TeleportRelativeRequest,
)

# Variables to store ball's location (x,y,theta)
ball_x_ = 0.0
ball_y_ = 0.0
ball_theta_ = 0.0

# Variables to store right_turtle's location (x,y,theta)
right_turtle_x_ = 0.0
right_turtle_y_ = 0.0
right_turtle_theta_ = 0.0

# Variables to store left_turtle's location (x,y,theta)
left_turtle_x_ = 0.0
left_turtle_y_ = 0.0
left_turtle_theta_ = 0.0

# Variables to store Right and Left player score's
right_turtle_score_ = 0
left_turtle_score_ = -1


def print_player_scores():
    """
    Print the player scores when ball is out of bounds
    """
    global right_turtle_score_, left_turtle_score_
    print("Ball out of bound! Printing the score's!")
    print("Current Score")
    print("Right:", right_turtle_score_, " Left:", left_turtle_score_)


def increment_right_score():
    global right_turtle_score_
    right_turtle_score_ = right_turtle_score_ + 1


def increment_left_score():
    global left_turtle_score_
    left_turtle_score_ = left_turtle_score_ + 1


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
    global ball_x_, ball_y_, ball_theta_
    ball_x_ = data.x
    ball_y_ = data.y
    ball_theta_ = data.theta


def callback2(data):
    global right_turtle_x_, right_turtle_y_, right_turtle_theta_
    right_turtle_x_ = data.x
    right_turtle_y_ = data.y
    right_turtle_theta_ = data.theta


def callback3(data):
    global left_turtle_x_, left_turtle_y_, left_turtle_theta_
    left_turtle_x_ = data.x
    left_turtle_y_ = data.y
    left_turtle_theta_ = data.theta


def init():
    """
    Function to initialize everything
    """

    # Accessing global variables
    global ball_x_, ball_y_, ball_theta_
    global right_turtle_x_, right_turtle_y_, right_turtle_theta_
    global left_turtle_x_, left_turtle_y_, left_turtle_theta_

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
        if ball_x_ >= 10.5 and ball_theta_ == 0.0:
            Teleport_Turtle_Relative(1.0, math.radians(150))
            increment_right_score()
            print_player_scores()

        if ball_x_ >= 10.5 and ball_theta_ > 0.0:
            Teleport_Turtle_Relative(1.0, (2 * math.pi / 3))
            increment_right_score()
            print_player_scores()

        if ball_x_ >= 10.5 and ball_theta_ < 0.0:
            Teleport_Turtle_Relative(1.0, (-2 * math.pi / 3))
            increment_right_score()
            print_player_scores()

        if ball_x_ <= 0.5 and ball_theta_ == 0.0:
            Teleport_Turtle_Relative(1.0, math.radians(150))
            increment_left_score()
            print_player_scores()

        if ball_x_ <= 0.5 and ball_theta_ < 0.0:
            Teleport_Turtle_Relative(1.0, (2 * math.pi / 3))
            increment_left_score()
            print_player_scores()

        if ball_x_ <= 0.5 and ball_theta_ > 0.0:
            Teleport_Turtle_Relative(1.0, (-2 * math.pi / 3))
            increment_left_score()
            print_player_scores()

        if ball_y_ <= 0.5 and ball_theta_ > -1.57:
            Teleport_Turtle_Relative(0.5, (math.pi / 3))

        if ball_y_ <= 0.5 and ball_theta_ < -1.57:
            Teleport_Turtle_Relative(0.5, (-math.pi / 3))

        if ball_y_ >= 10.5 and ball_theta_ < 1.57:
            Teleport_Turtle_Relative(0.5, (-math.pi / 3))

        if ball_y_ >= 10.5 and ball_theta_ > 1.57:
            Teleport_Turtle_Relative(0.5, (math.pi / 3))

        if (abs(ball_x_ - right_turtle_x_)) < 0.5 and (
            abs(ball_y_ - right_turtle_y_)
        ) < 0.5:
            frand = uniform(-1, 1)
            Teleport_Turtle_Absolute(ball_x_, ball_y_, frand)

        if (abs(ball_x_ - left_turtle_x_)) < 0.5 and (
            abs(ball_y_ - left_turtle_y_)
        ) < 0.5:
            frand = uniform(1.6, 3.7)
            Teleport_Turtle_Absolute(ball_x_, ball_y_, frand)

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
