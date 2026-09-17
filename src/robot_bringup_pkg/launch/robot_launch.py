#Those are the needed import in the launch file
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    #The files Paths to be passsed to the launch file

    robot_urdf_file = PathJoinSubstitution([
        FindPackageShare('robot_description_pkg'),
        'urdf',
        'obstacle.urdf.xacro' #the assembler xacro file that has all descriptions
    ])

    #rviz configuration file to not start from scratch everytime rviz opens
    rviz_config_file = PathJoinSubstitution([
        FindPackageShare('robot_description_pkg'),
        'rviz',
        'obstacle_config.rviz'
    ])

    #gazebo/ros bridge
    bridge_config_file = PathJoinSubstitution([
        FindPackageShare('robot_bringup_pkg'),
        'config',
        'gazebo_bridge.yaml'
    ])

    #this will take the xacro file and transform it to urdf format
    robot_description = ParameterValue (
        Command(['xacro ' , robot_urdf_file]),
        value_type = str
    )

    #launching gazbeo harmonic
    start_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ]),
        launch_arguments={
            'gz_args': 'empty.sdf -r'
        }.items()
    )


    start_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }],
        output='screen'
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', '/robot_description',
            '-name', 'edges_robot',
            '-x', '0',
            '-y', '0',
            '-z', '0.1' #slightly above the ground to ensur clean start
        ],
        output='screen'
    )

    
    start_gazebo_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': bridge_config_file
        }],
        output='screen'
    )

    start_rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{
            'use_sim_time': True
        }],
        output='screen'
    )

    #the teleop keyboard to test the simulation topics and nodes
    start_teleop = Node(
    package='teleop_twist_keyboard',
    executable='teleop_twist_keyboard',
    prefix='gnome-terminal --',
    output='screen'
    )

    return LaunchDescription([
        start_gazebo,
        start_robot_state_publisher,
        spawn_robot,
        start_gazebo_bridge,
        start_rviz,
        start_teleop
    ])