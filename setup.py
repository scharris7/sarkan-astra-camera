from setuptools import setup

package_name = 'astra_custom_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='scharris',
    maintainer_email='scharris2007@gmail.com',
    description='Astra custom bridge for ROS 2',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'astra_bridge_node = astra_custom_bridge.camera_node:main', 'image_viewer = astra_custom_bridge.image_viewer:main'
        ],
    },
)
