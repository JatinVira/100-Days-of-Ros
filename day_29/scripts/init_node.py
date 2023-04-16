#!/usr/bin/env python3

import rospy
from turtlesim.srv import Kill, KillRequest
from turtlesim.srv import Spawn, SpawnRequest
from turtlesim.srv import SetPen, SetPenRequest

def turnOffPen(name):
    call_name = name + "/set_pen"
    rospy.wait_for_service(call_name)

    pen = rospy.ServiceProxy(call_name, SetPen)
    pen_request = SetPenRequest()

    pen_request.off = 1
    pen(pen_request)

def init():

    rospy.init_node('init_node', anonymous=True)
    rospy.wait_for_service('/kill')
    rospy.wait_for_service('/spawn')

    killer = rospy.ServiceProxy('/kill', Kill)
    killer_request = KillRequest()

    spawn_turtle = rospy.ServiceProxy('/spawn', Spawn)
    spawn_turtle_request = SpawnRequest()
    
    killer_request.name = "turtle1"
    killer(killer_request)
    print("Called Kill Request!")

    spawn_turtle_request.x = 1.0
    spawn_turtle_request.y = 1.0
    spawn_turtle_request.theta = 1.5702
    spawn_turtle_request.name = "Right"
    spawn_turtle(spawn_turtle_request)
    print("Called Spawn Request Right!")
    turnOffPen("Right")

    spawn_turtle_request.x = 10.0
    spawn_turtle_request.y = 1.0
    spawn_turtle_request.theta = 1.5702
    spawn_turtle_request.name = "Left"
    spawn_turtle(spawn_turtle_request)
    print("Called Spawn Request Left!")
    turnOffPen("Left")

    spawn_turtle_request.x = 5.0
    spawn_turtle_request.y = 1.0
    spawn_turtle_request.theta = 0
    spawn_turtle_request.name = "Ball"
    spawn_turtle(spawn_turtle_request)
    print("Called Spawn Request Ball!")
    turnOffPen("Ball")

if __name__ == '__main__':
    try:
        init()
    except rospy.ROSInterruptException:
        pass