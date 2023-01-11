# Sesame UL UAVs

This package provides simulation environments, pre-equipped UAVs, and basic scenarios to run.

## Installation and pre-requisites

To run this code you will need ROS Noetic and Gazebo 11.
ROS Melodic might work but hasn't been tested.

To use this package you need to install the following package:
 - GRVC-UAL : Please use our modified version available here: 

Once both packages (GRVC-UAL and the present package) are in your source folder, the simulation should be ready to go.
Please note that yo install GRVC-UAL you will also need to install PX4. 
Follow to installation instructions available in the GRVC-UAL package.

## How to launch?

To launch a simulation with two of the drones used for Sesame inside the Univeristy of Luxemburg's Aerolab envrionment use the following command:
 - 
A single drone can also be simulated using this command:

To spawn a drone one can use the following launch file:

To start a world one can use the following launch file:

Beware, the simulation may take some time to start, up to one or two minutes.
This is normal behavior and is due to the number of cameras being simulated as well as the use 
of Software in the Loop (SIL) elements such as PX4.

## World and robot settings

### World definition


### Robot settings
