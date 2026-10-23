#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import threading

class AstraCustomBridge(Node):
    def __init__(self):
        super().__init__('astra_custom_bridge')
        
        self.declare_parameter('color_device', '/dev/video4')
        self.declare_parameter('depth_device', '/dev/video7')
        
        color_dev = self.get_parameter('color_device').value
        depth_dev = self.get_parameter('depth_device').value
        
        self.color_pub = self.create_publisher(Image, '/camera/color/image_raw', 10)
        self.depth_pub = self.create_publisher(Image, '/camera/depth/image_raw', 10)
        
        self.bridge = CvBridge()
        
        # Inicializar capturas por V4L2
        self.cap_color = cv2.VideoCapture(color_dev, cv2.CAP_V4L2)
        self.cap_color.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap_color.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap_color.set(cv2.CAP_PROP_FPS, 30)
        
        self.cap_depth = cv2.VideoCapture(depth_dev, cv2.CAP_V4L2)
        self.cap_depth.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap_depth.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap_depth.set(cv2.CAP_PROP_FPS, 30)
        
        # Variables compartidas y control de hilos para evitar lag
        self.color_frame = None
        self.depth_frame = None
        self.lock = threading.Lock()
        self.is_running = True
        
        # Lanzar hilos independientes de captura en segundo plano
        self.color_thread = threading.Thread(target=self.update_color, daemon=True)
        self.depth_thread = threading.Thread(target=self.update_depth, daemon=True)
        self.color_thread.start()
        self.depth_thread.start()
        
        # Timer de publicación a 30 FPS (~0.033s)
        self.timer = self.create_timer(0.033, self.timer_callback)
        self.get_logger().info("Astra Custom Bridge optimizado con hilos iniciado correctamente.")

    def update_color(self):
        while self.is_running:
            ret, frame = self.cap_color.read()
            if ret:
                with self.lock:
                    self.color_frame = frame

    def update_depth(self):
        while self.is_running:
            ret, frame = self.cap_depth.read()
            if ret:
                if len(frame.shape) == 3:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                with self.lock:
                    self.depth_frame = frame

    def timer_callback(self):
        with self.lock:
            c_frame = self.color_frame.copy() if self.color_frame is not None else None
            d_frame = self.depth_frame.copy() if self.depth_frame is not None else None
            
        if c_frame is not None:
            msg_c = self.bridge.cv2_to_imgmsg(c_frame, encoding='bgr8')
            msg_c.header.stamp = self.get_clock().now().to_msg()
            msg_c.header.frame_id = 'camera_color_frame'
            self.color_pub.publish(msg_c)
            
        if d_frame is not None:
            encoding = 'mono16' if d_frame.dtype.name == 'uint16' else 'mono8'
            msg_d = self.bridge.cv2_to_imgmsg(d_frame, encoding=encoding)
            msg_d.header.stamp = self.get_clock().now().to_msg()
            msg_d.header.frame_id = 'camera_depth_frame'
            self.depth_pub.publish(msg_d)

    def destroy_node(self):
        self.is_running = False
        self.cap_color.release()
        self.cap_depth.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = AstraCustomBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
