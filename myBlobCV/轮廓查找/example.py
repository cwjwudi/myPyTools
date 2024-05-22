import cv2
import numpy as np

# 加载图像并转为灰度图
image = cv2.imread('./36.jpeg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 二值化处理
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 查找轮廓
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for i,contour in  enumerate(contours):
    cnt_area = cv2.contourArea(contour)
    print(cnt_area)
    if cnt_area>200:
        cv2.drawContours(image, contours, i, (0, 0, 255), 3)  # 用红色线条绘制第一个轮廓
# # 绘制第一个轮廓
# cv2.drawContours(image, contours, 0, (0, 0, 255), 3)  # 用红色线条绘制第一个轮廓
# #计算第一个轮廓面积
# cnt_area = cv2.contourArea(contours[0])
# print(cnt_area)
cv2.imshow('erzhihua', thresh)
cv2.imwrite("36_erzhihua.jpg",thresh)
cv2.imshow('Contours', image)
cv2.imwrite("36_Contours.jpg",image)
cv2.waitKey(0)
cv2.destroyAllWindows()
