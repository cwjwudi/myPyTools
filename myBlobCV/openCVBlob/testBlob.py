import cv2
import numpy as np
import time

pi = 3.14159

im = cv2.imread("blob_detection.jpg", cv2.IMREAD_GRAYSCALE)

params = cv2.SimpleBlobDetector_Params()

# 设置参数
params.minThreshold = 14
params.maxThreshold = 54
params.filterByArea = True
params.minArea = 1000
params.maxArea = 2000
params.filterByCircularity = True
params.minCircularity = 0.78
params.filterByConvexity = False
params.filterByInertia = False

# 创建检测器
detector = cv2.SimpleBlobDetector_create(params)

# 测量程序运行时间
start_time = time.time()

# 运行检测器
keypoints = detector.detect(im)

# 计算程序运行时间
end_time = time.time()
execution_time = (end_time - start_time) * 1000
print("程序运行时间：", execution_time, "毫秒")

# 打印每个Blob的面积
for i, keypoint in enumerate(keypoints):
    r = keypoint.size / (2 * pi)
    A = pi * r*r
    print("Blob", i+1, "的面积大小：", A)


# 绘制关键点
with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# 显示结果
cv2.imshow("Keypoints", with_keypoints)
cv2.waitKey(0)
