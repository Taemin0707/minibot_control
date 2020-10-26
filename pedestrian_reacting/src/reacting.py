#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import rospy
import numpy as np

from geometry_msgs.msg import Twist
from pedestrian_tracking.msg import PedestrianInfo, PedestrianInfos

class PedestrianReactor(object):
    """인식된 보행자의 위치에 따라 로봇의 속도를 조절한다."""

    def __init__(self):
        # 글로벌 변수 설정
        self.closest_distance = 0

        # 구독 설정
        rospy.Subscriber('regulated/cmd_vel', Twist, self.update_cmd_vel)
        rospy.Subscriber('recognition/pedestrian_infos', PedestrianInfos, self.update_distance)

        # 발행 설정
        self.regulated_cmd_vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)

    def update_cmd_vel(self, data):
        """
        """
        current_cmd_vel = data

        multiply_alpha = None

        # 구간 설정 파라미터 (a, b)
        # | 최소속도 | 선형제어 | 일반제어 |
        # |        a        b
          
        a = 0.7
        b = 1.5

        if self.closest_distance < 0.3:
            multiply_alpha = 0.3333

        elif self.closest_distance < 1.5:
            multiply_alpha = ((0.7 / (b - a)) * self.closest_distance) + 0.3333

        else:
            multiply_alpha = 1

        regulated_cmd_vel = Twist()
        regulated_cmd_vel.linear.x = current_cmd_vel.linear.x * multiply_alpha
        regulated_cmd_vel.linear.y = current_cmd_vel.linear.y * multiply_alpha
        regulated_cmd_vel.linear.z = current_cmd_vel.linear.z * multiply_alpha

        regulated_cmd_vel.angular.x = current_cmd_vel.angular.x
        regulated_cmd_vel.angular.y = current_cmd_vel.angular.y
        regulated_cmd_vel.angular.z = current_cmd_vel.angular.z

        self.regulated_cmd_vel_pub.publish(regulated_cmd_vel)

    def update_distance(self, data):
        """
        """
        num_data = len(data.pedestrian_infos)

        if num_data != 0:
            distances = []
            for i in range(num_data):
                point_x = data.pedestrian_infos[i].point.x
                point_y = data.pedestrian_infos[i].point.y

                point = [float(point_x), float(point_y)]

                distance = self.calculate_2d_distance(point)
                distances.append(distance)

            closest_distance = min(distances)

            if closest_distance != 0:
                print('가장 가까운 사람과의 거리는 : {0:.4f} 입니다.'.format(self.closest_distance))
            else:
                print('Missing Depth')       

            self.closest_distance = closest_distance

        else:
            self.closest_distance = 100
            # print('검출된 사람이 없습니다.')
        
    def calculate_2d_distance(self, point):
        """
        """
        origin_point = [0, 0]
        dist = np.sqrt((point[0] - origin_point[0])**2 + (point[1] - origin_point[1])**2)

        return dist


if __name__ == '__main__':
    rospy.init_node('reacting', anonymous=False)
    pedestrian_reactor = PedestrianReactor()
    rospy.spin()
