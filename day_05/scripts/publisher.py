#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def Publisher():
    pub = rospy.Publisher("chatter", String, queue_size=10)
    rospy.init_node('Talker',anonymous=False)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        hello_str = "hello world in ros!"
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()    

if __name__ == "__main__":
    try :
        Publisher()
    except rospy.ROSInterruptException:
        pass