#!/usr/bin/env python3
import yaml
import rospy
import os
from uav_abstraction_layer.srv import TakeOff, GoToWaypoint, Land
from geometry_msgs.msg import PoseStamped


class WayPointTracker:
    def __init__(self):
        self.uav_namespace = rospy.get_param("~uav_namespace", "")
        self.file_path = rospy.get_param("~flight_plan_path", "")
	# Create the servies
        self.take_off_service_name = os.path.join("/", self.uav_namespace, "ual/take_off")
        self.go_to_service_name = os.path.join("/", self.uav_namespace, "ual/go_to_waypoint")
        self.land_service_name = os.path.join("/", self.uav_namespace, "ual/land")
        self.take_off_service = self.registerService(self.take_off_service_name, TakeOff)
        self.go_to_service = self.registerService(self.go_to_service_name, GoToWaypoint)
        self.land_service = self.registerService(self.land_service_name, Land)
        # Load flight plan    
        self.raw_flight_plan = None
        self.flight_plan = None
        self.loop_waypoints = None
        self.loadFlightPlan()
        self.parseFlightPlan()
        # Exectute flight plan
        self.takeOff(self.take_off_service, self.flight_plan['TakeOff'])
        self.followPoints(self.go_to_service, self.flight_plan['Waypoints'])
        self.goToWaypoint(self.go_to_service, self.flight_plan['LandingPosition'])
        self.land(self.land_service)

    def loadFlightPlan(self):
        # Check file exists
        if not os.path.exists(self.file_path):
            raise ValueError("The file does not exist, please check the provided path.")

        with open(self.file_path, 'r') as wp_file:
            self.raw_flight_plan = yaml.safe_load(wp_file)

    def makeStampedPose(self, data, frame):
        waypoint = PoseStamped()
        waypoint.header.frame_id = frame 
        waypoint.pose.position.x =    data[0]
        waypoint.pose.position.y =    data[1]
        waypoint.pose.position.z =    data[2]
        waypoint.pose.orientation.x = data[3]
        waypoint.pose.orientation.y = data[4]
        waypoint.pose.orientation.z = data[5]
        waypoint.pose.orientation.w = data[6]
        return waypoint

    def parseFlightPlan(self):
        self.loop_waypoints = self.raw_flight_plan['loop_waypoints']
        self.flight_plan = {}
        self.flight_plan['TakeOff'] = self.raw_flight_plan['take_off_altitude']
        self.flight_plan['LandingPosition'] = self.makeStampedPose(self.raw_flight_plan['landing_position'],
                                                              self.raw_flight_plan['frame_id'])
        self.flight_plan['Waypoints'] = []
        for i in self.raw_flight_plan['waypoints']:
            waypoint = self.makeStampedPose(i, self.raw_flight_plan['frame_id'])
            self.flight_plan['Waypoints'].append(waypoint)

    def followPoints(self, go_to_service, waypoints):
        if self.loop_waypoints:
            while (not rospy.is_shutdown()):
                for waypoint in waypoints:
                    self.goToWaypoint(go_to_service, waypoint)
        else:
            for waypoint in waypoints:
                self.goToWaypoint(go_to_service, waypoint)

    def registerService(self, service_path, service_type):
        rospy.wait_for_service(service_path)
        try:
            service = rospy.ServiceProxy(service_path, service_type)
        except rospy.ServiceException as e:
            print("Service registration failed: %s", e)
        return service

    def goToWaypoint(self, go_to_service, waypoint):
        try:
            go_to_service(waypoint, True)
        except rospy.ServiceException as e:
            print("Service call failed: %s", e)

    def takeOff(self, take_off_service, height):
        try:
            take_off_service(height, True)
        except rospy.ServiceException as e:
            print("Service call failed: %s", e)

    def land(self, land_service):
        try:
            land_service(True)
        except rospy.ServiceException as e:
            print("Service call failed: %s", e)

if __name__ == "__main__":
    rospy.init_node('waypoint_tracker')
    WPT = WayPointTracker()
