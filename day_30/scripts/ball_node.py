#!/usr/bin/env python3

# Importing Math package for Pi, radians funnctions
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
    print("Ball out of bound! Printing the score's !")
    print("Current Score")
    print("Right:", right_turtle_score_, " Left:", left_turtle_score_)


def increment_right_score():
    """
    Increment Right Player Score
    """
    global right_turtle_score_
    right_turtle_score_ = right_turtle_score_ + 1


def increment_left_score():
    """
    Increment Left Player Score
    """
    global left_turtle_score_
    left_turtle_score_ = left_turtle_score_ + 1


def Teleport_Turtle_Absolute(x, y, theta):
    """
    Teleport's the Turtle to an Absolute Location (x,y,theta)
    """

    # Setup a Service Proxy
    teleport_turtle = rospy.ServiceProxy("/Ball/teleport_absolute", TeleportAbsolute)
    teleport_turtle_request = TeleportAbsoluteRequest()

    # Fill the data packet
    teleport_turtle_request.x = x
    teleport_turtle_request.y = y
    teleport_turtle_request.theta = theta

    # Call the service
    teleport_turtle(teleport_turtle_request)


def Teleport_Turtle_Relative(linear_translate, angular_translate):
    """
    Teleport's the Turtle to a Relative Location (x_translation,y_translation)
    """

    # Setup a Service Proxy
    teleport_turtle = rospy.ServiceProxy("/Ball/teleport_relative", TeleportRelative)
    teleport_turtle_request = TeleportRelativeRequest()

    # Fill the data packets
    teleport_turtle_request.linear = linear_translate
    teleport_turtle_request.angular = angular_translate

    # Call the service
    teleport_turtle(teleport_turtle_request)


def ball_pose_callback(data):
    """
    Updates the ball pose in x, y, theta continuosly
    """
    global ball_x_, ball_y_, ball_theta_
    ball_x_ = data.x
    ball_y_ = data.y
    ball_theta_ = data.theta


def right_pose_callback(data):
    """
    Updates the right_turtle's pose in x, y, theta continuosly
    """
    global right_turtle_x_, right_turtle_y_, right_turtle_theta_
    right_turtle_x_ = data.x
    right_turtle_y_ = data.y
    right_turtle_theta_ = data.theta


def left_pose_callback(data):
    """
    Updates the left_turtle's pose in x, y, theta continuosly
    """
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

    # Setup a publisher object to publish to /Ball/cmd_vel topic
    pub = rospy.Publisher("/Ball/cmd_vel", Twist, queue_size=10)

    # Setup a subscriber object to sub to /Ball/Pose for Ball Location feedback
    ball_pose_subscriber = rospy.Subscriber("/Ball/pose", Pose, ball_pose_callback)

    # Setup a subscriber object to sub to /Right/Pose for Right_tutles Location feedback
    right_pose_subscriber = rospy.Subscriber("/Right/pose", Pose, right_pose_callback)

    # Setup a subscriber object to sub to /Left/Pose for Left_tutles Location feedback
    left_pose_subscriber = rospy.Subscriber("/Left/pose", Pose, left_pose_callback)

    # Create a variable to move ball later
    ball_vel = Twist()

    # Setting the Publisher rate to 10Hz
    rate = rospy.Rate(10)

    # Start an Infinite loop until ROS is active
    while not rospy.is_shutdown():
        # Ball out of Positive X bound (>10.5)
        if ball_x_ >= 10.5 and ball_theta_ == 0.0:
            Teleport_Turtle_Relative(1.0, math.radians(150))
            increment_right_score()
            print_player_scores()

        # Ball out of Positive X bound (>10.5)
        # and Angled upwards (Towards Top of screen)
        if ball_x_ >= 10.5 and ball_theta_ > 0.0:
            Teleport_Turtle_Relative(1.0, (2 * math.pi / 3))
            increment_right_score()
            print_player_scores()

        # Ball out of Positive X bound (>10.5)
        # and Angled downwards (Towards Bottom of screen)
        if ball_x_ >= 10.5 and ball_theta_ < 0.0:
            Teleport_Turtle_Relative(1.0, (-2 * math.pi / 3))
            increment_right_score()
            print_player_scores()

        # Ball out of Negative X bound (<0.5)
        if ball_x_ <= 0.5 and ball_theta_ == 0.0:
            Teleport_Turtle_Relative(1.0, math.radians(150))
            increment_left_score()
            print_player_scores()

        # Ball out of Negative X bound (<0.5)
        # and Angled downwards (Towards Bottom of screen)
        if ball_x_ <= 0.5 and ball_theta_ < 0.0:
            Teleport_Turtle_Relative(1.0, (2 * math.pi / 3))
            increment_left_score()
            print_player_scores()

        # Ball out of Negative X bound (<0.5)
        # and Angled upwards (Towards Top of screen)
        if ball_x_ <= 0.5 and ball_theta_ > 0.0:
            Teleport_Turtle_Relative(1.0, (-2 * math.pi / 3))
            increment_left_score()
            print_player_scores()

        # Ball out of Negative Y bound (<0.5)
        # and Angled towrads Right Turtle
        if ball_y_ <= 0.5 and ball_theta_ > -1.57:
            Teleport_Turtle_Relative(0.5, (math.pi / 3))

        # Ball out of Negative Y bound (<0.5)
        # and Angled towrads Left Turtle
        if ball_y_ <= 0.5 and ball_theta_ < -1.57:
            Teleport_Turtle_Relative(0.5, (-math.pi / 3))

        # Ball out of Positive Y bound (>10.5)
        # and Angled towrads Right Turtle
        if ball_y_ >= 10.5 and ball_theta_ < 1.57:
            Teleport_Turtle_Relative(0.5, (-math.pi / 3))

        # Ball out of Positive Y bound (>10.5)
        # and Angled towrads Left Turtle
        if ball_y_ >= 10.5 and ball_theta_ > 1.57:
            Teleport_Turtle_Relative(0.5, (math.pi / 3))

        # Collision of Ball with Right Turtle
        if (abs(ball_x_ - right_turtle_x_)) < 0.5 and (
            abs(ball_y_ - right_turtle_y_)
        ) < 0.5:
            frand = uniform(-1, 1)
            # Keeping the same (x,y) chnage the theta
            Teleport_Turtle_Absolute(ball_x_, ball_y_, frand)

        # Collision of Ball with Left Turtle
        if (abs(ball_x_ - left_turtle_x_)) < 0.5 and (
            abs(ball_y_ - left_turtle_y_)
        ) < 0.5:
            frand = uniform(1.6, 3.7)
            # Keeping the same (x,y) chnage the theta
            Teleport_Turtle_Absolute(ball_x_, ball_y_, frand)

        # Logic to keep Ball moving
        ball_vel.linear.x = 2.0
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
