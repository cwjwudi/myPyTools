import cv2
import numpy as np


# 定义滑动条回调函数
def update_blob_params(x):
    global params, detector
    params.minThreshold = int(cv2.getTrackbarPos("Min Threshold", "Blob Detection"))
    params.maxThreshold = int(cv2.getTrackbarPos("Max Threshold", "Blob Detection"))
    params.minArea = int(cv2.getTrackbarPos("Min Area", "Blob Detection"))
    params.maxArea = int(cv2.getTrackbarPos("Max Area", "Blob Detection"))

    # 确保minThreshold小于等于maxThreshold
    if params.minThreshold > params.maxThreshold:
        params.minThreshold = params.maxThreshold

    # 确保minArea小于等于maxArea
    if params.minArea > params.maxArea:
        params.minArea = params.maxArea

    params.minCircularity = float(cv2.getTrackbarPos("Min Circularity", "Blob Detection")) / 100.0
    # print("min circularity:", params.minCircularity)
    detector = cv2.SimpleBlobDetector_create(params)


# 读取图像
im = cv2.imread("blob_detection.jpg", cv2.IMREAD_GRAYSCALE)

# 创建Blob检测器
params = cv2.SimpleBlobDetector_Params()

params.filterByArea = True
params.filterByCircularity = True
params.filterByConvexity = False
params.filterByInertia = False

detector = cv2.SimpleBlobDetector_create(params)

# 创建窗口并添加滑动条
cv2.namedWindow("Blob Detection")
cv2.createTrackbar("Min Threshold", "Blob Detection", int(params.minThreshold), 255, update_blob_params)
cv2.createTrackbar("Max Threshold", "Blob Detection", int(params.maxThreshold), 255, update_blob_params)
cv2.createTrackbar("Min Area", "Blob Detection", int(params.minArea), 10000, update_blob_params)
cv2.createTrackbar("Max Area", "Blob Detection", int(params.maxArea), 10000, update_blob_params)
cv2.createTrackbar("Min Circularity", "Blob Detection", int(params.minCircularity * 100), 100, update_blob_params)

while True:
    # 运行Blob检测器
    keypoints = detector.detect(im)

    # 在图像上绘制中点
    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # 显示图像
    cv2.imshow("Blob Detection", im_with_keypoints)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # 按下ESC键退出
        break

cv2.destroyAllWindows()
