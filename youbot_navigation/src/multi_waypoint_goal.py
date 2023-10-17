#!/usr/bin/env python3
import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
import tf_transformations
import yaml
from ament_index_python.packages import get_package_share_directory
import os
from rclpy.node import Node

# --- A function to create a pose message
def create_pose_stamped(navigator: BasicNavigator, position_x, position_y, orientation_z):
    q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, orientation_z)
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = position_x
    pose.pose.position.y = position_y
    pose.pose.position.z = 0.0
    pose.pose.orientation.x = q_x
    pose.pose.orientation.y = q_y
    pose.pose.orientation.z = q_z
    pose.pose.orientation.w = q_w
    return pose

def main(args=None):
    # --- Init
    rclpy.init(args=args)
    # node = Node('multi_waypoint_goal_node')
    # rclpy.spin(node)

    nav = BasicNavigator()
    yb_nav_dir = get_package_share_directory('youbot_navigation')
    goals_yaml = os.path.join(yb_nav_dir, 'maps', 'navigation_goals_sim.yaml')
    # --- Set initial pose
    # initial_pose = create_pose_stamped(nav, -0.266, -0.009, 0.205)
    # nav.setInitialPose(initial_pose)

    # --- Wait for Nav2
    # print("initial pose set")
    nav.waitUntilNav2Active()
    print("nav2 active")

    waypoints = []
    goals=[]
    #simulation goals
    # goals_yaml = "maps/navigation_goals_sim.yaml" 
    #real world goals
    # goals_yaml = "../maps/navigation_goals.yaml"

    with open(goals_yaml, 'r') as yaml_file:
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)

    for goal_name, goal_values in data.items():
        # print(goal_values)
        goals.append(goal_values)

    print("Total number of goals to navigate to: ", len(goals))

    for i in range(len(goals)):
        waypoints.append(create_pose_stamped(nav, goals[i][0], goals[i][1], goals[i][2]))


    # --- Go to one pose
    # nav.goToPose(goal_pose1)
    # while not nav.isTaskComplete():
    #     feedback = nav.getFeedback()
    #     # print(feedback)

    # --- Follow waypoints
    nav.followWaypoints(waypoints)
    while not nav.isTaskComplete():
        feedback = nav.getFeedback()
        # print(feedback)

    result = nav.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Goal succeeded!')
    elif result == TaskResult.CANCELED:
        print('Goal was canceled!')
    elif result == TaskResult.FAILED:
        print('Goal failed!')
    else:
        print('Goal has an invalid return status!')

    # nav.lifecycleShutdown()
    # # --- Shutdown
    # rclpy.shutdown()

if __name__ == '__main__':
    main()