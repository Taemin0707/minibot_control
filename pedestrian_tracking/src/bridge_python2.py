#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import rospy
import numpy as np

import cv2
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError

class Bridge(object):
    """압축된 이미지를 센서 메세지 형태로 변환한다.."""

    def __init__(self):
        # 글로벌 변수 설정
        self.bridge = CvBridge()

        # 발행 설정
        self.color_image_pub = rospy.Publisher("camera/color/image_raw", Image, queue_size=1)

        # 구독 설정
        self.compressed_color_image_sub = rospy.Subscriber("camera/color/image_raw/compressed", CompressedImage, self.bridge_color_image)
        
    def bridge_color_image(self, data):
        """
        """

        # 압축 데이터를 CV 배열로 변환
        np_arr = np.fromstring(data.data, np.uint8)
        color_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        try:
            self.color_image_pub.publish(self.bridge.cv2_to_imgmsg(color_image, "bgr8"))

        except CvBridgeError as e:
            print(e)

if __name__ == '__main__':
    rospy.init_node('bridge', anonymous=False)
    bridge = Bridge()
    rospy.spin()
