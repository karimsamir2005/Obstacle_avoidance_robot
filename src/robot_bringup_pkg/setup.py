import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'robot_bringup_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
        # Install all launch files:
        (os.path.join('share', package_name, 'launch'), glob('launch/*launch.[pxy][yma]*')),
        
        # Install bridge and yaml configs:
        (os.path.join('share', package_name, 'config'), glob('config/*')),
        
        # Install rviz configs:
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kareem',
    maintainer_email='kareem@todo.todo',
    description='Bringup package for obstacle robot simulation',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)