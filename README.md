# Sesame UL UAVs
![OS](https://img.shields.io/badge/OS-Ubuntu_20.04-orange.svg) ![ROS_Noetic](https://img.shields.io/badge/ROS-Noetic-brightgreen.svg) ![Gazebo](https://img.shields.io/badge/Gazebo-11-lightgrey.svg)

This package provides simulation environments, pre-equipped UAVs, and basic scenarios to run.

## Installation and pre-requisites

To run this code you will need ROS Noetic and Gazebo 11.
ROS Melodic might work but hasn't been tested.

To use this package you need to install the following package:
 - GRVC-UAL : Please use our modified version available here: https://github.com/AntoineRichard/grvc-ual-3.1-noetic

Once both packages (GRVC-UAL and the present package) are in your source folder, the simulation should be ready to go.
Please note that yo install GRVC-UAL you will also need to install PX4. 
Follow to installation instructions available in the GRVC-UAL package.

## How to launch?

To launch a simulation with two of the drones used for Sesame inside the Univeristy of Luxemburg's Aerolab envrionment use the following command:
```
roslaunch sesame_ul_uavs aerolab_two_drones.launch
```
A single drone can also be simulated using this command:
```
roslaunch sesame_ul_uavs aerolab_one_drone.launch
```
To spawn a drone one can use the following launch file:
```
roslaunch sesame_ul_uavs spawn_drone.launch id:=1 robot_model:=spacer5g description_package:=sesame_ul_uavs
```

To start a world one can use the following launch file:
```
roslaunch sesame_ul_uavs start_grvc_world.launch description_package:=A_CATKIN_PACKAGE world:=A_WORLD
roslaunch sesame_ul_uavs start_grvc_world.launch description_package:=sesame_ul_uavs world:=aerolab.world
roslaunch sesame_ul_uavs start_grvc_world.launch description_package:=vineyard world:=vineyard.world
```

Beware, the simulation may take some time to start, up to one or two minutes.
This is normal behavior and is due to the number of cameras being simulated as well as the use 
of Software in the Loop (SIL) elements such as PX4.

## Following waypoints
To follow waypoints we provide a simple script that can be started from a launch file.

### Following a set of waypoints
To follow waypoints, one can use a launch file like so:
```
roslaunch sesame_ul_uavs simple_mission.launch uav_namespace:=uav_1 flight_plan_path:=$(rospack find sesame_ul_uavs)/cfg/grid_pattern_aerolab.yaml
```
This has the drone with `id 1` follow a grid like pattern.
```
roslaunch sesame_ul_uavs simple_mission.launch uav_namespace:=uav_2 flight_plan_path:=$(rospack find sesame_ul_uavs)/cfg/observer_position.yaml
```
This has the drone with `id 2` stay at a fixed position.
```
roslaunch sesame_ul_uavs simple_mission.launch uav_namespace:=uav_2 flight_plan_path:=$(rospack find sesame_ul_uavs)/cfg/rectangle_pattern_y_z.yaml
```
This last command has a drone with `id 2` repeat an infinite loop.

### Generating a new set of waypoints

```
---
frame_id: 'map' # The frame in which the points should be followed
take_off_altitude: 1.5 # The altitude the drone should reach when taking off
landing_position: [2.25, 1.75, 1.0, 0.0, 0.0, 0.0, 1.0] # The desired landing position
loop_waypoints: True # If true, the drone will repeat the waypoint sequence till the script is interrupted.
waypoints: # The list of waypoints. Having a single waypoint and loop_waypoints: = True will result in the drone hovering in position.
    - [2.25,  1.75, 1.5, 0.0, 0.0, 1.0, 0]
    - [2.25, -1.75, 1.5, 0.0, 0.0, 1.0, 0]
    - [2.25, -1.75, 2.5, 0.0, 0.0, 1.0, 0]
    - [2.25,  1.75, 2.5, 0.0, 0.0, 1.0, 0]
```


## World and robot settings

### World definition
Worlds must contain the following physics settings:
```
    <physics type='ode'>
      <!-- Values shoud be step_size = 0.001*F and time_up= 1000/F-->
      <!-- 
              F   step_size   real_time   real_time_factor
              1   0.001       1000        0.4 (controler works)
              2   0.002        500        0.6 (controler works)
              3   0.003        333        0.8-0.9 (controler works)
              4   0.004        250        (controler does not work)
              5   0.005        200        (controler does not work)
              6   0.006        166
              7   0.007        142
              8   0.008        125
              9   0.009        111
              10  0.01         100
      -->
      <max_step_size>0.004</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>250</real_time_update_rate>
    </physics>
```


### Robot settings
TODO
