cmake_minimum_required(VERSION 3.0.2)
project(cr_cw2_gaze_based_prediction)

find_package(catkin REQUIRED COMPONENTS
  #bayesian_belief_network
  rospy
  std_msgs
  message_generation
)

catkin_python_setup()

################################################
## Declare ROS messages, services and actions ##
################################################
# Generate messages in the 'msg' folder
add_message_files(
	FILES
	human_info.msg
	prediction_results.msg
)

# Generate services in the 'srv' folder
add_service_files(
	FILES
	prediction.srv
)

# Generate added messages and services with any dependencies listed here
generate_messages(
	DEPENDENCIES
	std_msgs
)

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES cr_cw2_gaze_based_prediction
	CATKIN_DEPENDS rospy std_msgs #bayesian_belief_network
#  DEPENDS system_lib
)

###########
## Build ##
###########
## Specify additional locations of header files

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

#############
## Install ##
#############
# Mark executable scripts (Python etc.) for installation
catkin_install_python(PROGRAMS
	scripts/update_human.py
	scripts/controller.py
	scripts/target_prediction.py
	scripts/data_logger.py
	DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
