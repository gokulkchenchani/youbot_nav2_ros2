import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription

from launch_ros.actions import Node


def generate_launch_description():
  pkg_yb_nav = get_package_share_directory('youbot_navigation')
  pkg_tb3_autonomy = get_package_share_directory('tb3_autonomy')

  autonomy_node_cmd = Node(
      package="behavior_tree",
      executable="multi_goal_nav",
      name="multi_goal_nav",
      parameters=[{
          "location_file": os.path.join(pkg_yb_nav, "maps", "navigation_goals_sim.yaml")
      }]
  )

  ld = LaunchDescription()

  # Add the commands to the launch description
  ld.add_action(autonomy_node_cmd)

  return ld
