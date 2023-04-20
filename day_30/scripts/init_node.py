#!/usr/bin/env python3

# Importing essential ROS packages
import rospy
from turtlesim.srv import Kill, KillRequest
from turtlesim.srv import Spawn, SpawnRequest
from turtlesim.srv import SetPen, SetPenRequest


# Function to turn off the trace left by turtle (Pen Off)
def turnOffPen(name):
    # Create a variable to use service with turtle name
    call_name = name + "/set_pen"

    # Wait for services to start before proceeding further
    rospy.wait_for_service(call_name)

    # Service setup for Setting Pen status
    pen = rospy.ServiceProxy(call_name, SetPen)
    pen_request = SetPenRequest()

    # Turn off the pen field and call service
    pen_request.off = 1
    pen(pen_request)


# Function to initialize robot poses
def init():
    # Create a ROS Node
    rospy.init_node("init_node", anonymous=True)

    # Wait for services to start before proceeding further
    rospy.wait_for_service("/kill")
    rospy.wait_for_service("/spawn")

    # Service setup for Killing Turtle
    killer = rospy.ServiceProxy("/kill", Kill)
    killer_request = KillRequest()

    # Kill the turtle with name 'turtle1'
    killer_request.name = "turtle1"
    killer(killer_request)
    print("Called Kill Request!")

    # Service setup for Spawning Turtle at Position
    spawn_turtle = rospy.ServiceProxy("/spawn", Spawn)
    spawn_turtle_request = SpawnRequest()

    # Spawn the Right Player turtle at (x,y) = (1,1) and turn off Pen
    spawn_turtle_request.x = 1.0
    spawn_turtle_request.y = 1.0
    spawn_turtle_request.theta = 1.5702
    spawn_turtle_request.name = "Right"
    spawn_turtle(spawn_turtle_request)
    print("Called Spawn Request Right!")
    turnOffPen("Right")

    # Spawn the Right Player turtle at (x,y) = (10,1) and turn off Pen
    spawn_turtle_request.x = 10.0
    spawn_turtle_request.y = 1.0
    spawn_turtle_request.theta = 1.5702
    spawn_turtle_request.name = "Left"
    spawn_turtle(spawn_turtle_request)
    print("Called Spawn Request Left!")
    turnOffPen("Left")

    # Spawn the Ball turtle at (x,y) = (5,1) and turn off Pen
    spawn_turtle_request.x = 5.0
    spawn_turtle_request.y = 1.0
    spawn_turtle_request.theta = 0
    spawn_turtle_request.name = "Ball"
    spawn_turtle(spawn_turtle_request)
    print("Called Spawn Request Ball!")
    turnOffPen("Ball")


# Main
if __name__ == "__main__":
    try:
        init()
    except rospy.ROSInterruptException:
        pass
