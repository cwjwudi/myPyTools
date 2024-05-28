# circle_detection_blob.py

import cv2
import numpy as np
import time

def detect_circles_and_draw_rectangles(image_path):
    # 读取图像
    image = cv2.imread(image_path,  cv2.IMREAD_COLOR)

    # 转换图像为灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 设置参数
    params = cv2.SimpleBlobDetector_Params()

    # 过滤参数
    params.filterByArea = True
    params.minArea = 100
    params.filterByCircularity = True
    params.minCircularity = 0.8

    # 创建Blob检测器
    detector = cv2.SimpleBlobDetector_create(params)

    start_time = time.time()
    # 检测blob
    keypoints = detector.detect(gray)

    end_time = time.time()

    execution_time = (end_time - start_time) * 1000
    print("程序运行时间：", execution_time, "毫秒")
    # 绘制blob
    for keypoint in keypoints:
        x = int(keypoint.pt[0])
        y = int(keypoint.pt[1])
        radius = int(keypoint.size / 2)

        # 绘制圆
        cv2.circle(image, (x, y), radius, (0, 255, 0), 2)

        # 计算最小外接矩形
        rect_x = x - radius
        rect_y = y - radius
        rect_w = 2 * radius
        rect_h = 2 * radius

        # 绘制最小外接矩形
        cv2.rectangle(image, (rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h), (255, 0, 0), 2)

    # 显示结果
    cv2.imshow('Blob Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    image_path = '../myPrintMachine/mypic/image_14us.jpg'
    detect_circles_and_draw_rectangles(image_path)
