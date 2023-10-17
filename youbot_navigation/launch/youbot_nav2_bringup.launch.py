import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import (DeclareLaunchArgument, GroupAction,
                            IncludeLaunchDescription, SetEnvironmentVariable)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import PushRosNamespace
from nav2_common.launch import RewrittenYaml

def generate_launch_description():
    
    yb_nav_dir = get_package_share_directory('youbot_navigation')
    map_file = os.path.join(yb_nav_dir, 'maps', 'my_map.yaml')
    use_sim_time = True
    
    

    map_server = Node(
                    package='nav2_map_server',
                    executable='map_server',
                    name='map_server',
                    output='screen',
                    parameters=[{'use_sim_time': use_sim_time}, 
                                {'yaml_filename':map_file},
                                {"topic_name": "map"},
                                {"frame_id": "map"}]
                    )
    
    lifecycle_manager = Node(
                    package='nav2_lifecycle_manager',
                    executable='lifecycle_manager',
                    name='lifecycle_manager_mapper',
                    output='screen',
                    parameters=[{'use_sim_time': use_sim_time},
                                {'autostart': True},
                                {'node_names': ['map_server']}]
                    )
    
    localization_node = Node(
                    package='youbot_navigation',
                    executable='localization_launch.py',
                    name='localization_launch',
                    output='screen'
                    )
    
    tf2_ros = Node(
                    package='tf2_ros',
                    executable='static_transform_publisher',
                    name='static_transform_publisher',
                    arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']
                    )
    
    navigation_node = Node(
                    package='youbot_navigation',
                    executable='navigation_launch.py',
                    name='localization_launch',
                    output='screen'
                    )
    
    rviz_launch_cmd = Node(
                    package="rviz2",
                    executable="rviz2",
                    name="rviz2",
                    arguments=['-d' + os.path.join(get_package_share_directory('youbot_description'), 'rviz', 'navigation.rviz')],
                    )
    
    return LaunchDescription([
        rviz_launch_cmd,
        map_server,
        lifecycle_manager,
        tf2_ros, 
        # localization_node,
        # navigation_node,          
        ])