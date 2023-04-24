# 100-Days-of-Ros: Day 30   
![Short Game Play](https://github.com/JatinVira/100-Days-of-Ros/blob/main/image/turtlesim_pong.gif)   

-----------------------  
## Package Description:      
This repository contains code for Day 30 of the [100 Days of ROS challenge](https://github.com/JatinVira/100-Days-of-Ros), which implements the Pong arcade video game for the Robot Operating System (ROS 1 Noetic) using `turtlesim`.    
The intention of developing this package was to take something as simple as turtlesim, use reference from other projects, and develop a cool game out of it using ROS. Also explaining the process of breaking down problem into smaller modules and solving each module appropriately.
The inspiration for this project was drawn from [ros-turtle-pong](https://fjp.at/ros/turtle-pong/)   

-------------------------  

## Requirements

To run this project, you will need the following:
- ROS Noetic installed on your system
- Turtlesim package   

------------------------
## Usage   

To run the project, first clone the repository:
```console
git clone https://github.com/JatinVira/100-Days-of-Ros.git
```
Next, build the project
```console
cd catkin_ws/
catkin build
source ~/.bashrc
```
Then, navigate to the `day_30` directory:
```console
cd catkin_ws/src/100-Days-of-Ros/day_30/
```
Launch the project using the following launch file:
```console
roslaunch day_30 turtlesim_pong.launch
```

--------------------------