import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
import launch
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    ld = LaunchDescription()

    can_channel = LaunchConfiguration("can_channel")

    declare_can_channel_cmd = DeclareLaunchArgument(
        "can_channel",
        default_value="can0",
        description="CAN Channel",
    )
    
    ld.add_action(declare_can_channel_cmd)

    master_bin_path = os.path.join(
        get_package_share_directory("can_transceiver"),
        "config",
        "17w_config",
        "master.bin",
    )

    if not os.path.exists(master_bin_path):
        master_bin_path = ""

    device_container = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("canopen_core"), "launch"),
                "/canopen.launch.py",
            ]
        ),
        launch_arguments={
            "master_config": os.path.join(
                get_package_share_directory("can_transceiver"),
                "config",
                "17w_config",
                "master.dcf",
            ),
            "master_bin": master_bin_path,
            "bus_config": os.path.join(
                get_package_share_directory("can_transceiver"),
                "config",
                "17w_config",
                "bus.yml",
            ),
            "can_interface_name": can_channel,
        }.items(),
    )

    ld.add_action(device_container)
    
    return ld