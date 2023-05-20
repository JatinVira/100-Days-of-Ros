#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "geometry_msgs/Point.h"
#include "sensor_msgs/LaserScan.h"
#include "visualization_msgs/Marker.h" 
using std::cout;
using std::cin;
using std::endl;

class action{
   public:
      ros::NodeHandle nh;
      ros::Publisher velocity_pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel",100);
      ros::Publisher marker_pub = nh.advertise<visualization_msgs::Marker>("/Rviz_marker",100);
      visualization_msgs::Marker markers_;
      geometry_msgs::Point point_;
      geometry_msgs::Twist velocity_messsage;
      void forward(){
        velocity_messsage.linear.x = 0.5;
        velocity_pub.publish(velocity_messsage);
      }
      void left_(){
        velocity_messsage.angular.z = -0.5;
        velocity_pub.publish(velocity_messsage);  
      }
      void right(){
        velocity_messsage.angular.z = 0.5;
        velocity_pub.publish(velocity_messsage);
      }

      //Publish the Visual marker method
      void read_marker(){
        markers_.header.frame_id = "lidar_1"; //start transition from the laser_frame
        markers_.ns = "robot_namespace";
        markers_.id = 0;
        markers_.type = markers_.ARROW; //specify the shape of the marker
        markers_.action = markers_.ADD;
        point_.z = 0.0;
        markers_.pose.position = point_;

        markers_.pose.position.x = 0.0;
        markers_.pose.position.y = 0.0;
        markers_.pose.position.z = 0.0;
        //size of marker
        markers_.scale.x = 0.1; 
        markers_.scale.y = 0.1;
        markers_.scale.z = 0.1;

        //r,g,b color for the marker
        markers_.color.r = 0.0;
        markers_.color.g = 1.0;
        markers_.color.b = 0.0;

        //set to 1(True) so arrow becomes visible
        markers_.color.a = 1.0;
        while (ros::ok() || velocity_messsage.linear.x == 0.5){
          marker_pub.publish(markers_);
          cout << "The position of markers(x,y,z):" <<  markers_.pose.position.x << " " <<   markers_.pose.position.y  << " "<<   markers_.pose.position.z << endl;
          ROS_INFO("The Marker node has started.....");
        }
      }
};//main class action

void laser_callback(const sensor_msgs::LaserScanConstPtr& msg){
    //action store(p);//copy constructor
    float angle_min = msg->angle_min;
    float angle_max = msg->angle_max;
    float angle_increment = msg->angle_increment; 
    float range_min = msg->range_min;
    float range_max = msg->range_max;
    std::vector<float> ranges = msg->ranges;

    ROS_INFO("Received LaserScan message");
    ROS_INFO("Angle Min: %f", angle_min);
    ROS_INFO("Angle Max: %f", angle_max);
    ROS_INFO("Angle Increment: %f", angle_increment);
    ROS_INFO("Range Min: %f", range_min);
    ROS_INFO("Range Max: %f", range_max);
    for (size_t i = 0; i < ranges.size(); ++i)
    {
        ROS_INFO("Range at index %zu: %f", i, ranges[i]);
    }
    if (msg->range_min < 1){
        action p;
        p.left_();
    }
    else if (msg->range_min > 1){
        action p;
        p.forward();
    }
    else{
        action p;
        p.forward();
    }

}

int main(int argc,char**argv){
    ros::init(argc,argv,"Visual_marker_node");
    ros::NodeHandle nh;
    ros::Subscriber laser_scan = nh.subscribe("/scan",1,laser_callback);
    action p;
    p.read_marker();
    p.forward();//robot moves forward
    ros::spin();
    return 0;
}