#!/usr/bin/env python3
import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
import tf_transformations
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
    # node = Node('single_pose_goal_node')
    # rclpy.spin(node)
    nav = BasicNavigator()

    # --- Set initial pose
    # initial_pose = create_pose_stamped(nav, 0.0, 0.0, 0.0)
    # nav.setInitialPose(initial_pose)

    # --- Wait for Nav2
    nav.waitUntilNav2Active()

    # --- Send Nav2 goal
    waypoints = []
    waypoints.append(create_pose_stamped(nav, 2.636, 3.277, -0.696))

    # --- Follow waypoints
    nav.goToPose(create_pose_stamped(nav, 2.636, 3.277, -0.696))
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