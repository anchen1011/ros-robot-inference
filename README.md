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
7. `roscd robot_inference`

### run the robot inference system

#### run from rosrun
1. in a new terminal or screen run `roscore`
2. in a new terminal or screen **(build the package first)**, run `rosrun robot_inference robot_inference_server.py`
3. **[c++ client]** in a new terminal or screen **(build the package first)**, `roscd robot_inference/src`, run `rosrun robot_inference robot_inference_client [observation file]` e.g. under robot_inference/src directory `rosrun robot_inference robot_inference_client test.txt`
3. **[python client]** in a new terminal or screen **(build the package first)**, `roscd robot_inference`, run `rosrun robot_inference robot_inference_client.py [observation file]` e.g. under robot_inference directory `rosrun robot_inference robot_inference_client.py sample/test.txt`

#### run from roslaunch (using python client)
1. **build the package**, `roscd robot_inference`
2. ``ROS_HOME=`pwd` roslaunch robot_inference robot_inference.launch a:="[observation file]"`` e.g. under robot_inference directory ``ROS_HOME=`pwd` roslaunch robot_inference robot_inference.launch a:="sample/test.txt"``. Information received by client is displayed on screen.

## file system

### robot_inference
ROS package

### robot_inference/CMakeLists.txt
build information

### robot_inference/package.xml
package information

### robot_inference/package.xml
package information

### robot_inference/launch/robot_inference.launch
launch file

### robot_inference/srv/Inference.srv
service

### robot_inference/scripts/robot_inference_server.py
robot inference server

### robot_inference/scripts/robot_inference_client.py
robot inference client (python)

### robot_inference/src/robot_inference_client.cpp
robot inference client (c++)

### robot_inference/scripts/test.txt
test obervations. each line is a pair of coordinates of observed position
