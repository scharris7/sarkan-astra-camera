#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class DirectImageViewer(Node):
    def __init__(self):
        super().__init__('direct_image_viewer')
        self.bridge = CvBridge()
        
        self.subscription = self.create_subscription(
            Image,
            '/camera/color/image_raw',
            self.listener_callback,
            10
        )
        self.get_logger().info("Visor directo activo. Presiona 'q' en la ventana para cerrar.")

    def listener_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        cv2.imshow("Orbbec Astra+ Fluid View", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    viewer = DirectImageViewer()
    try:
        rclpy.spin(viewer)
    except KeyboardInterrupt:
        pass
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
