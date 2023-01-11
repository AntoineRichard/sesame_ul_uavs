cmake_minimum_required(VERSION 3.0.2)
project(sesame_ul_uavs)

find_package(catkin REQUIRED COMPONENTS
  gazebo_ros
  gazebo_dev
  roscpp
  rospy
  tf
  tf2_ros
  nav_msgs
  std_msgs
)

find_package(Boost REQUIRED COMPONENTS thread)

include_directories(include
  ${Boost_INCLUDE_DIRS}
  ${catkin_INCLUDE_DIRS}
)

link_directories(
  ${catkin_LIBRARY_DIRS}
)

if (NOT GAZEBO_VERSION VERSION_LESS 6.0)
  catkin_package(  INCLUDE_DIRS include LIBRARIES gazebo_ros_elevator)
endif()

if (NOT GAZEBO_VERSION VERSION_LESS 7.3)
  catkin_package(INCLUDE_DIRS include LIBRARIES gazebo_ros_harness)
endif()

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES
  gazebo_ros_p3d_v2

  CATKIN_DEPENDS
  gazebo_msgs
  roscpp
  rospy
  geometry_msgs
  nav_msgs
  tf
  tf2_ros
  std_msgs
)

add_library(gazebo_ros_p3d_v2 src/gazebo_ros_p3d_v2.cpp)
target_link_libraries(gazebo_ros_p3d_v2 ${catkin_LIBRARIES} ${Boost_LIBRARIES})

install(TARGETS
	gazebo_ros_p3d_v2)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY models/spacer5g
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY worlds
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
