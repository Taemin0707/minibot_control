#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import rospy
import numpy as np

import cv2
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError

from darknet_ros_msgs.msg import BoundingBoxes, ObjectCount

class Bridge(object):
    """압축된 이미지를 센서 메세지 형태로 변환한다.."""

    def __init__(self):
        # 글로벌 변수 설정
        self.bridge = CvBridge()
        self.bounding_boxes = BoundingBoxes()
        self.image = None

        # 발행 설정
        self.compressed_detection_image_pub = rospy.Publisher("/detection_image/compressed", CompressedImage, queue_size=1)

        # 구독 설정
        compressed_color_image_sub = rospy.Subscriber("camera/color/image_raw/compressed", CompressedImage, self.bridge_color_image)
        bounding_boxes_sub = rospy.Subscriber('darknet_ros/bounding_boxes', BoundingBoxes, self.update_bounding_boxes)
        
    def bridge_color_image(self, data):
        """
        """

        # 압축 데이터를 CV 배열로 변환
        np_arr = np.fromstring(data.data, np.uint8)
        self.image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # try:
        #     self.color_image_pub.publish(self.bridge.cv2_to_imgmsg(color_image, "bgr8"))

        # except CvBridgeError as e:
        #     print(e)

    def update_bounding_boxes(self, data):
        bounding_boxes = data

        for i in range(len(self.bounding_boxes.bounding_boxes)):
            try:
                if self.bounding_boxes.bounding_boxes[i].Class == 'person':
                    probability = self.bounding_boxes.bounding_boxes[i].probability
                    xmin = self.bounding_boxes.bounding_boxes[i].xmin
                    ymin = self.bounding_boxes.bounding_boxes[i].ymin
                    xmax = self.bounding_boxes.bounding_boxes[i].xmax
                    ymax = self.bounding_boxes.bounding_boxes[i].ymax
                    _id = i + 1
                    _class = self.bounding_boxes.bounding_boxes[i].Class
            except:
                pass

    # def bridge_detection_image(self, data):
    #     """
    #     """
    #     # try:
    #     detection_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    #     # except CvBridgeError as e:
    #     #     print(e)

    #     compressed_detection_image = CompressedImage()
    #     compressed_detection_image.header.stamp = rospy.Time.now()
    #     compressed_detection_image.format = "jpeg"
    #     compressed_detection_image.data = cv2.imencode('.jpg', detection_image)[1].tostring()
  
    #     try:
    #         self.compressed_detection_image_pub.publish(compressed_detection_image)

    #     except CvBridgeError as e:
    #         print(e)

if __name__ == '__main__':
    rospy.init_node('bridge', anonymous=False)
    bridge = Bridge()
    rospy.spin()
