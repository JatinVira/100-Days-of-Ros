#!/usr/bin/env python3

import rospy
from day_06.srv import AddTwoInts, AddTwoIntsResponse

def handler(req):
    print("Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b)))
    return AddTwoIntsResponse(req.a + req.b)

def add_two_ints_server():
    rospy.init_node("Server", anonymous= False)
    s = rospy.Service("add_two_ints", AddTwoInts, handler)
    rospy.loginfo("Ready to Serve!")
    rospy.spin()

if __name__ == '__main__':
    add_two_ints_server()