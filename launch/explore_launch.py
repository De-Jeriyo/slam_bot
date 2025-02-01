import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Declare "use_sim_time" launch argument with default false
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time if true'
    )
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Get package share directories
    slam_bot_share = get_package_share_directory('slam_bot')
    explore_lite_share = get_package_share_directory('explore_lite')

    # Define file paths for the various launch/config files
    online_async_launch_file = os.path.join(slam_bot_share, 'launch', 'online_async_launch.py')
    navigation_launch_file = os.path.join(slam_bot_share, 'launch', 'navigation_launch.py')
    explore_launch_file = os.path.join(explore_lite_share, 'launch', 'explore.launch.py')

    mapper_params_file = os.path.join(slam_bot_share, 'config', 'mapper_params_online_async.yaml')
    nav2_params_file = os.path.join(slam_bot_share, 'config', 'nav2_params.yaml')
    explore_params_file = os.path.join(slam_bot_share, 'config', 'explore.yaml')
    rviz_config_file = os.path.join(slam_bot_share, 'rviz', 'nav2_default_view.rviz')

    # Launch RViz immediately
    rviz_launch = ExecuteProcess(
        cmd=['rviz2', '-d', rviz_config_file],
        output='screen'
    )

    # Launch slam_toolbox (online_async_launch) after a short delay
    slam_launch = TimerAction(
        period=5.0,  # delay in seconds (adjust as needed)
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(online_async_launch_file),
                launch_arguments={
                    'slam_params_file': mapper_params_file,
                    'use_sim_time': use_sim_time
                }.items()
            )
        ]
    )

    # Launch nav2 (navigation_launch) after an additional delay
    nav2_launch = TimerAction(
        period=10.0,  # delay from start (adjust as needed)
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(navigation_launch_file),
                launch_arguments={
                    'params_file': nav2_params_file,
                    'use_sim_time': use_sim_time
                }.items()
            )
        ]
    )

    # Launch explore_lite after another delay
    explore_launch = TimerAction(
        period=15.0,  # delay from start (adjust as needed)
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(explore_launch_file),
                launch_arguments={
                    'params_file': explore_params_file,
                    'use_sim_time': use_sim_time
                }.items()
            )
        ]
    )

    return LaunchDescription([
        use_sim_time_arg,
        rviz_launch,
        slam_launch,
        nav2_launch,
        explore_launch
    ])
