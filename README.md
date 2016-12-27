# ros-robot-inference
Robot behavior inference system based on ROS.

## instruction

### install ROS
1. install ROS following instrucitons in http://wiki.ros.org/ROS/Installation
2. create a catkin workspace `catkin_ws` following instrucitons in http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment#Create_a_ROS_Workspace

### build the package
1. put `robot_inference` under `catkin_ws/src` directory
2. `cd` to `catkin_ws`
3. `source devel/setup.bash`
4. `catkin_make`
5. `cd src/robot_inference/scripts`
6. `chmod +x *.py`

### run the robot inference system

#### run from rosrun
1. in a new terminal or screen run `roscore`
2. in a new terminal or screen run `rosrun robot_inference robot_inference_server.py`
3. in a new terminal or screen run `rosrun robot_inference robot_inference_client.py [observation file]` e.g. under robot_inference directory `rosrun robot_inference robot_inference_client.py scripts/test.txt`

#### run from roslaunch
1. `roslaunch robot_inference robot_inference.launch a:="[observation file]"` e.g. under robot_inference directory `roslaunch robot_inference robot_inference.launch a:="scripts/test.txt"`
2. open the log file (printed with roslaunch) and see the result

## file system

### robot_inference
ROS package

### robot_inference/srv
Service

### robot_inference/scripts/robot_inference_server.py
robot inference server

### robot_inference/scripts/robot_inference_client.py
robot inference client

### robot_inference/scripts/test.txt
test obervations. each line is a pair of coordinates of observed position
