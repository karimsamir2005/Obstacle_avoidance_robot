import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class AvoidanceLogicNode(Node):
    def __init__(self):
        super().__init__('avoidance_logic_node')

        #Subscribe to the LIDAR ros topic coming from the Gazebo lidar plugin
        self.lidar_data = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10
        )

        #Publishing velocity commands to the differential plugin
        self.send_vel_command = self.create_publisher(Twist, '/cmd_vel', 10)

        #Declaring the Parameters of the script
        self.safe_distance = self.declare_parameter("safe_distance" , 0.5).value
        self.forward_speed = self.declare_parameter("forward_speed" , 0.2).value
        self.turn_speed = self.declare_parameter("turn_speed" , 0.2).value

    def filter_ranges(self, scan_slice, r_min, r_max):
        valid = [r for r in scan_slice if r_min < r < r_max]
        return min(valid) if len(valid) > 0 else float('inf')

    def lidar_callback(self, msg: LaserScan):

        right_dist = self.filter_ranges(msg.ranges[90:150], msg.range_min, msg.range_max)
        front_dist = self.filter_ranges(msg.ranges[150:210], msg.range_min, msg.range_max)
        left_dist  = self.filter_ranges(msg.ranges[210:270], msg.range_min, msg.range_max)

        cmd = Twist()

        if front_dist > self.safe_distance:
            # Front is clear -> Move forward
            cmd.linear.x = self.forward_speed
            cmd.angular.z = 0.0
        else:
            cmd.linear.x = 0.0
            if left_dist > right_dist:
                cmd.angular.z = self.turn_speed   # Turn left
            else:
                cmd.angular.z = -self.turn_speed  # Turn right

        self.send_vel_command.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = AvoidanceLogicNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        stop_cmd = Twist()
        node.send_vel_command.publish(stop_cmd)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()