import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

head_tail_distance_mm = 14 #落地首尾标
C1 = 0
C2 = 0
# 0-青色， 1-红， 2-黄， 3-黑
class MarkDetect:
    def __init__(self):
        global head_tail_distance_mm
        # 调试控制参数
        self.plt_show = 0  # 是否进行检测过程的图片显示
        self.profile_enable = 0  # 是否分析代码耗时

        ### 设置初始状态下的长度范围，对应像素宽的物理宽
        self.field_of_view_X_mm = 50  #长度 落地
        self.resolution_X = 2048
        self.mark_num = 5
        # self.head_tail_pixel = 700
        self.head_tail_x_pixel = 0
        self.head_tail_y_pixel = 0
        self.mark_detect_num = 0
        self.detect_step = 0
        self.mark_type_ix = -1



        # 菱形标+圆形标

        self.mark_type = 0  # 0：菱形标，1：圆形标
        self.mark_width = [1, 1.5] # 菱形对角线 圆形直径
        self.mark_height = [1, 1.5]
        self.rectangularity = [1, 0.785]  # PI/4 = 0.785
        self.limit = [0.6, 1.2]  # [0.7, 1.2]，筛选面积和长宽的最大最小倍数范围

        # 检测算法相关参数
        self.scaling = 3  # 3，先缩小3倍粗检测，时间花费和精度都比较合适
        self.blur_kernel = 35  # 9，处理之前高斯滤波窗口大小，9比较合适
        self.adaptive_block = 67  # 67，自适应二值化的窗口大小，对于目前测试的大小矩形标和三角标都较为合适
        self.C = 3  # 12，自适应二值化的阈值偏差, 光亮直接相关！！！！！
        self.par = []
        self.mark_area = []


        # 两个相机，但是目前该函数中只使用一个相机，两个相机在两个线程中分别用该函数实现，所以这里self.camera_ix直接设置为0，2相机可行？
        self.global_ymin = -1
        self.global_ymax = -1
        self.global_ROI_enable = 1
        self.camera_ix = 0 #改！
        self.par_init()

    def par_init(self):
        # 圆标直径1-1.5mm，转换为对应的像素大小，（2048/50）* [1, 1.5]
        self.mark_width = [i * self.resolution_X / self.field_of_view_X_mm for i in self.mark_width]
        self.mark_height = [i * self.resolution_X / self.field_of_view_X_mm for i in self.mark_height]
        self.mark_area = [i * j * k for i, j, k in zip(self.mark_width, self.mark_height, self.rectangularity)]
        self.par = []
        # 根据预先设定的筛选大小范围self.limit，分别计算scaling和不scaling参数，计算长、宽、面积的限制
        for n in [1, self.scaling]:  # 参数预先计算
            n2 = n * n
            area_limit = [[area * self.limit[0] / n2, area * self.limit[1] / n2] for area in self.mark_area]
            width_limit = [[w * self.limit[0] / n, w * self.limit[1] / n] for w in self.mark_width]
            height_limit = [[h * self.limit[0] / n, h * self.limit[1] / n] for h in self.mark_height]
            # 矩形度，菱形是1，圆形是0.785，根据self.limit设置放缩的范围
            rectangularity_limit = [[rec * self.limit[0], rec * self.limit[1]] for rec in self.rectangularity]
            blur_kernel = int(round(self.blur_kernel / n, 0))
            blur_kernel = blur_kernel if blur_kernel % 2 else blur_kernel + 1
            adaptive_block = int(round(self.adaptive_block / n, 0))
            adaptive_block = adaptive_block if adaptive_block % 2 else adaptive_block + 1
            self.par.append(
                [n, n2, area_limit, width_limit, height_limit, rectangularity_limit, blur_kernel, adaptive_block])


    def mark_detect(self, img):
        global head_tail_distance_mm, C1, C2
        self.head_tail_pixel = float(head_tail_distance_mm / self.field_of_view_X_mm) * 2048

        scaling = self.scaling

        # 计算原始大小
        origin_img_width, origin_img_height = img.shape[1], img.shape[0]

        _ymin, _ymax, _enable = self.global_ymin, self.global_ymax, self.global_ROI_enable
        if _ymin >= 0 and _ymax >= 0 and _enable:
            img = img[self.global_ymin:self.global_ymax, :]
            # 整张图resize一下，粗检测
            img_in = cv2.cvtColor(img[0:-1:scaling, 0:-1:scaling, :], cv2.COLOR_RGB2GRAY)  # 起始终止步长，resize重新处理
            img_HSV = cv2.cvtColor(img[0:-1:scaling, 0:-1:scaling, :], cv2.COLOR_RGB2HSV)  # 起始终止步长，resize重新处理
            # img_in = cv2.cvtColor(img[0:-1:scaling, 0:-1:scaling, :], cv2.COLOR_RGB2GRAY)  # 起始终止步长，resize重新处理
            # img_HSV = cv2.cvtColor(img[0:-1:scaling, 0:-1:scaling, :], cv2.COLOR_RGB2HSV)  # 起始终止步长，resize重新处理
        else:
            # 工艺一：对整图resize，进行第一次粗检测
            # 0:-1:scaling这个切片的含义是从第一个像素开始（索引0），到倒数第二个像素结束（索引-1，不包含-1）
            # 步长为scaling。这样就实现了对图像进行缩放的效果。
            img_in = cv2.cvtColor(img[0:-1:scaling, 0:-1:scaling, :], cv2.COLOR_RGB2GRAY)  # 将RGB图像转换为灰度图像
            img_HSV = cv2.cvtColor(img[0:-1:scaling, 0:-1:scaling, :], cv2.COLOR_RGB2HSV)  # 将RGB图像转换为HSV颜色空间
            # cv2.imshow("draw",img_HSV)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        self.detect_step = 0
        result_gray, img_, binary_img = self.mark_detect_single_channel(img_in, img_HSV, self.detect_step, n=scaling)

        # # 工艺二：找出粗检测的范围，进行精检测
        if scaling != 1:
            accurate_result = []
            for x_center, y_center, cnt, rect, box, *o in result_gray:
                x, y = box[:, 0].min(), box[:, 1].min()
                w, h = box[:, 0].max() - x, box[:, 1].max() - y
                x, y, w, h = x * scaling, y * scaling, w * scaling, h * scaling
                edge = 20
                xmin = max(x - edge, 0)
                xmax = min(x + w + edge, img.shape[1])
                ymin = max(y - edge, 0)
                ymax = min(y + h + edge, img.shape[0])
                im_in = img[ymin:ymax, xmin:xmax]
                im_in = cv2.cvtColor(im_in, cv2.COLOR_RGB2GRAY)
                img_HSV = img[ymin:ymax, xmin:xmax]
                img_HSV = cv2.cvtColor(img_HSV, cv2.COLOR_RGB2HSV)
                self.detect_step = 1
                result_, img_, binary_img_ = self.mark_detect_single_channel(im_in, img_HSV, self.detect_step, n=1,
                                                                             xmin=xmin, ymin=ymin)
                if len(result_) > 0:
                    accurate_result.append(result_[0])
            result_gray = accurate_result
        result_pos_gray = np.array(
            [[x_center, y_center, rect[2], color, mark_Value, detect_step, meangray_dis, rectangularity] for
             x_center, y_center, cnt, rect, box, color, mark_Value, detect_step, meangray_dis, rectangularity, *o in
             result_gray])  # 矩阵
        result_pos = result_pos_gray.copy()  # copy

        # 如果只检测出了部分色标（大于一个，小于全部），则尝试单独取0通道检测其他色标
        if 1 <= len(result_gray) < self.mark_num:
            # 在上面灰度图检测出来色标的情况下，根据所有色标位置，截取色标所在周边的图像，取该截取图像的某个单独通道，再检测一遍
            if C2 != 0:
                self.C = C2
            else:
                self.C = 4

            # 将检测范围改为y方向的小范围内，大概100多的像素范围
            ymax, ymin = result_pos_gray[:, 1].max(), result_pos_gray[:, 1].min()
            ymin = int(max(ymin - self.mark_height[self.mark_type_ix] - 20, 0))
            ymax = int(min(ymax + self.mark_height[self.mark_type_ix] + 20, img.shape[0]))

            img_R_channel = img[ymin:ymax, :, 0]
            img_HSV = img[ymin:ymax, :]
            img_HSV = cv2.cvtColor(img_HSV, cv2.COLOR_RGB2HSV)
            self.detect_step = 2

            self.plt_show = 0   # 检测补测部分的代码
            result_R_channel, img_, binary_img = self.mark_detect_single_channel(img_R_channel, img_HSV, self.detect_step,
                                                                                 n=1, xmin=0, ymin=ymin)
            result_pos_R_channel = np.array(
                [[x_center, y_center, rect[2], color, mark_Value, detect_step, meangray_dis, rectangularity] for
                 x_center, y_center, cnt, rect, box, color, mark_Value, detect_step, meangray_dis, rectangularity, *o in
                 result_R_channel])

            if C1 != 0:
                self.C = C1
            else:
                self.C = 3

            # 第二次检测出至少一个色标的情况下，尝试合并
            if len(result_R_channel) >= 1:
                # result_pos_R_channel = result_pos_R_channel[np.argsort(result_pos_R_channel[:, 0])]  # 排序
                for i, r in enumerate(result_pos_R_channel):  # i序号 r内容
                    x_distance = result_pos[:, 0] - r[0]  # 上次和这次x差别
                    if np.abs(x_distance).min() > (
                            self.mark_height[self.mark_type_ix] + self.mark_width[self.mark_type_ix]) * 0.5:
                        result_pos = np.concatenate((result_pos, result_pos_R_channel[i:i + 1]), axis=0)

        # 对检测结果中明显存在角度偏差的菱形对象进行删除
        if self.mark_type == 0:
            # 计算中点（平均值）
            midpoint = np.mean(result_pos[:, 2])
            # 计算每个数据点与中点的绝对偏差
            deviations = np.abs(result_pos[:, 2] - midpoint)
            # 找到偏离度较大的值
            n_outliers = result_pos.shape[0] - self.mark_num
            outlier_indices = np.argsort(deviations)[-n_outliers:]

        result_pos = np.delete(result_pos, outlier_indices, axis=0)


        if result_pos.shape[0] >= 3:  # 至少检出3个时，则下一次检测色标根据本次色标截取ROI
            # 将色标在图中的大致位置记录下来，下次检测时先默认检测该大致位置内的图片
            _ymin, _ymax, _enable = self.global_ymin, self.global_ymax, self.global_ROI_enable
            if self.global_ymin >= 0 and self.global_ymax >= 0 and _enable:
                result_pos[:, 1] = result_pos[:, 1] + self.global_ymin
            if abs(result_pos[:, 1].max() - result_pos[:, 1].min()) < self.mark_height[self.mark_type_ix] * 2:
                self.global_ymin = int(max(result_pos[:, 1].min() - self.mark_height[self.mark_type_ix] * 2, 0))
                self.global_ymax = int(
                    min(result_pos[:, 1].max() + self.mark_height[self.mark_type_ix] * 2, origin_img_height))

                # if abs(min(result_pos[:, 1].max()) - max(result_pos[:, 1].min())) < self.mark_height[self.mark_type_ix] * 4:
                #     self.global_ymin = int(max(result_pos[:, 1].min() - self.mark_height[self.mark_type_ix] * 4, 0))
                #     self.global_ymax = int(min(result_pos[:, 1].max() + self.mark_height[self.mark_type_ix] * 4, origin_img_height))

            # if _enable:
            #     if abs(result_pos[:, 1].max() - result_pos[:, 1].min()) < self.mark_height[self.mark_type_ix] * 4:
            #         result_pos[:, 1] = result_pos[:, 1] + _ymin
            #         self.global_ymin = int(max(result_pos[:, 1].min() - self.mark_height[self.mark_type_ix] * 4, 0))
            #         self.global_ymax = int(min(result_pos[:, 1].max() + self.mark_height[self.mark_type_ix] * 4, origin_img_height))
        else:
            self.global_ymin = -1
            self.global_ymax = -1

        detection_success = 0
        if result_pos.shape[0] >= 2:  # 至少检出2个
            detection_success = 1
            self.mark_detect_num = result_pos.shape[0]
            result_pos = result_pos[np.argsort(result_pos[:, 0])]  # 排序
            # 根据首尾标校准距离 result_pos[:, :2] = result_pos[:, :2] * self.head_tail_distance_mm / (result_pos[-1,
            # 0] - result_pos[0, 0])  #更换参数

            # 计算首尾标间距
            breakflag = 0
            head_tail = 0
            # print(self.head_tail_pixel)
            for i in range(0, result_pos.shape[0] - 1):
                for j in range(i + 1, result_pos.shape[0]):
                    if result_pos[i, 3] == result_pos[j, 3]:
                        self.head_tail_x_pixel = abs(result_pos[j, 0] - result_pos[i, 0])
                        self.head_tail_y_pixel = abs(result_pos[j, 1] - result_pos[i, 1])
                        head_tail = math.sqrt(self.head_tail_x_pixel ** 2 + self.head_tail_y_pixel ** 2)
                        if 0.8 * self.head_tail_pixel < head_tail < 1.2 * self.head_tail_pixel:
                            # print(head_tail, self.head_tail_pixel)
                            if abs(j - i) == 4:  # 首尾间距，防止识别错颜色
                                self.head_tail_pixel = head_tail
                                breakflag = 1
                                break
                if breakflag == 1:
                    break
            # print(detection_success)
        else:
            detection_success = 0

        return detection_success, result_pos

    def mark_detect_single_channel(self, img, img_HSV, detect_step,n=1, xmin=0, ymin=0):
        if n == 1:
            n, n2, area_limit, width_limit, height_limit, rectangularity_limit, blur_kernel, adaptive_block = self.par[
                0]
        else:   # n为scaling，如果scaling不为1，则执行 self.par[1]
            n, n2, area_limit, width_limit, height_limit, rectangularity_limit, blur_kernel, adaptive_block = self.par[
                1]

        # img = img[0:-1:n, 0:-1:n]
        # img_bilateralFilter = cv2.bilateralFilter(img, blur_kernel, 15, 5)
        # img_medianBlur = cv2.medianBlur(img, blur_kernel)
        img_Gaussian = cv2.GaussianBlur(img, (blur_kernel, blur_kernel), 0)
        binary_img = cv2.adaptiveThreshold(img_Gaussian, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                                           adaptive_block, self.C)
        # binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_ERODE, np.ones((3, 3), np.uint8), iterations=1)
        contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]  # 寻找轮廓
        # contours 在这种情况下是ndarray，(N, 1, 2) 的形式表示：
        # N：表示轮廓上的点的数量。
        # 1：表示每个点有一个维度。
        # 2：表示每个点有两个值，分别是 x 和 y 坐标。
        # 打印包含轮廓的图片用于测试
        if self.plt_show == 1:
            for i, contour in enumerate(contours):
                cnt_area = cv2.contourArea(contour)
                for [a1, a2] in area_limit:
                    if a1 < cnt_area < a2:
                        # 在图片显示面积符合要求的图形
                        print("No: {}, Area: {}".format(i, cnt_area))
                        cv2.drawContours(img_HSV, contours, i, (0, 0, 255), 3)  # 用红色线条绘制第一个轮廓
            cv2.imshow('binary_img', img_HSV)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        ### 输出黑白图，用户调试CV参数
        # cv2.imshow("draw",binary_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # 遍历所有轮廓，并进行判断
        result = []
        for cnt in contours:
            area = cv2.contourArea(cnt)

            # 面积粗检,多种色标
            area_ok = 0
            for [a1, a2] in area_limit:
                if a1 < area < a2:
                    area_ok = 1
                    break
            if not area_ok:
                continue

            rect = cv2.minAreaRect(cnt)  # 轮廓最小外接矩形
            w, h = rect[1]

            size_ok = 0
            for [w1, w2], [h1, h2] in zip(width_limit, height_limit):  #外接矩形宽高判断
                if (w1 < w < w2 and h1 < h < h2) or (w1 < h < w2 and h1 < w < h2):
                    size_ok = 1
                    break
            if not size_ok: continue

            # if not 30 < abs(rect[2]) < 60:
            #     continue  # 菱形角度判断

            # 再综合判断一下，同时确定是哪种类型的色标，面积长宽矩形度色标类型判断 根据矩形度判断是否一致


            # ! 以下这段逻辑混乱，建议重构矩形度判断函数
            # mark_ok = 0
            # self.mark_type_ix = -1  # ix这里选择range(len(width_limit))，实际上就是0和1，和self.mark_type统一
            # for [w1, w2], [h1, h2], [a1, a2], [r1, r2], ix in zip(width_limit, height_limit, area_limit,
            #                                                       rectangularity_limit, range(len(width_limit))):
            #     if (a1 < area < a2) and ((w1 < w < w2 and h1 < h < h2) or (w1 < h < w2 and h1 < w < h2)) and (
            #             r1 < area / (w * h) < r2):
            #         mark_ok = 1
            #         self.mark_type_ix = ix
            #         break    # 先验证是否为菱形，如果在菱形的范围内，直接跳过，否则验证是否在圆形范围内

            # 矩形度判断
            mark_ok = self.isMarkOk(area, w, h)

            if mark_ok == 0:
                continue


            # 计算色标中心点   在色标中点的一定范围内搜索，HSV的h平均值
            x_center, y_center = rect[0]
            # print(x_center, y_center)
            hValue = img_HSV[int(y_center),int(x_center)][0]
            hValue_Center = img_HSV[int(y_center), int(x_center)][0]
            hValues = []
            hValue_min = img_HSV[int(y_center),int(x_center)][0]
            hValue_max = img_HSV[int(y_center),int(x_center)][0]
            # int(max((y_center - h/4),0) 排除图片顶部
            # int(min((y_center + h/4 + 1),img.shape[0])) 排除图片底部
            for y_mark in range(int(max((y_center - h/4),0)),int(min((y_center + h/4 + 1),img.shape[0]))):
                for x_mark in range(int(max((x_center - w/4),0)), int(min((x_center + w/4 + 1),img.shape[1]))):
                    if img_HSV[int(y_mark ),int(x_mark)][0] > hValue_max:
                        hValue_max = img_HSV[int(y_mark ),int(x_mark)][0]
                    elif img_HSV[int(y_mark ),int(x_mark)][0] < hValue_min:
                        hValue_min = img_HSV[int(y_mark), int(x_mark)][0]
                    hValues.append(img_HSV[int(y_mark ),int(x_mark)][0])
            hValues = sorted(hValues)
            hValue = hValues[int(len(hValues)/2)]   # hValues排序后，取中点值


            # 搜索HSV的v平均值
            vValue = img_HSV[int(y_center),int(x_center)][2]
            vValues = []
            for y_mark in range(int(max((y_center - h/4),0)),int(min((y_center + h/4 + 1),img.shape[0]))):
                for x_mark in range(int(max((x_center - w/4),0)), int(min((x_center + w/4 + 1),img.shape[1]))):
                    vValues.append(img_HSV[int(y_mark ),int(x_mark)][2])
            vValues = sorted(vValues)
            vValue = vValues[int(len(vValues)/2)]
            # vValue = min(vValues)
            mark_V = int(vValue)

            color = 3  # 0-青色， 1-红， 2-黄， 3-黑

            # if mark_V < 95:
            #     # color = 3
            #     hValue = max(hValues)
            # else:
            #     hValues = sorted(hValues)
            #     hValue = hValues[int(len(hValues)/2)]


            mark_Value = int(hValue)
            if 5 < mark_Value < 30:
                color = 0 #青
            elif 75 <= mark_Value <= 120:
                color = 2 #黄
            elif 140 < mark_Value < 169:
                color = 1 #红
            # elif 173 < mark_Value <= 180:
            #     color = 3 #黑

            if (mark_V < 90) and ((int(hValue_min) < 6) or (int(hValue_max) > 173)): #和照片亮度相关！光圈，光照，曝光时间
                 color = 3

            x_center, y_center = x_center + xmin, y_center + ymin

            # 计算外接最小举行顶点
            box = cv2.boxPoints(rect)  # 外接矩形的定点坐标
            box = np.intp(box)  # 坐标整型化

            cal_other_output = 0  # area 矩形度，灰度对比
            if cal_other_output:
                # 计算实际尺寸和标准尺寸的比值
                area_rate = area * n2 / self.mark_area[self.mark_type_ix]
                w_rate = w * n / self.mark_width[self.mark_type_ix]
                h_rate = h * n / self.mark_height[self.mark_type_ix]

                # 计算矩形度
                rectangularity = area / (w * h)

                # 计算色标与背景灰度差别
                xmin1, xmax1 = box[:, 0].min(), box[:, 0].max()
                ymin1, ymax1 = box[:, 1].min(), box[:, 1].max()
                xmin2 = max(xmin1 - (xmax1 - xmin1), 0)
                xmax2 = min(xmax1 + (xmax1 - xmin1), img.shape[1])
                ymin2 = max(ymin1 - (ymax1 - ymin1), 0)
                ymax2 = min(ymax1 + (ymax1 - ymin1), img.shape[0])
                meangray1 = img[ymin1:ymax1, xmin1:xmax1].mean()
                meangray2 = img[ymin2:ymax2, xmin2:xmax2].mean()
                meangray_dis = abs(meangray1 - meangray2)
            else:
                meangray_dis, rectangularity, area_rate, w_rate, h_rate = 0, 0, 0, 0, 0

            result.append([x_center, y_center, cnt, rect, box, color, mark_Value, detect_step, meangray_dis, rectangularity, area_rate, w_rate, h_rate])

            # for i in range(0, len(result)-1):
            #     if (result[:, 7].min() <= result[i, 7] <= (result[:, 7].min() + 20)) and (result[i, 7] < 90):
                    # result[i, 5] = 3

            # for i, r in enumerate(result):  # i序号 r内容
            #     if (result[:, 7].min() <= result[i, 7] <= (result[:, 7].min() + 20)) and (result[i, 7] < 90):
            #         result[i, 5] = 3
                # x_distance = result[:, 0] - r[0]  # 上次和这次x差别
                # if np.abs(x_distance).min() > (
                #         self.mark_height[self.mark_type_ix] + self.mark_width[self.mark_type_ix]) * 0.5:
                #     result_pos = np.concatenate((result_pos, result_pos_R_channel[i:i + 1]), axis=0)


        if self.plt_show:
            binary_img_plt = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2RGB)
            img_plt = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            img_plt2 = img_plt.copy()
            plt.figure(figsize=(23, 12))
            for x_center, y_center, cnt, rect, *o in result:
                cv2.drawContours(img_plt, [cnt], -1, (0, 0, 255), 2)
                cv2.drawContours(binary_img_plt, [cnt], -1, (0, 0, 255), 2)
                box = cv2.boxPoints(rect)  # 外接矩形的定点坐标
                box = np.intp(box)  # 坐标整型化
                cv2.drawContours(img_plt2, [box], -1, (0, 0, 255), 2)
            plt.subplot(2, 2, 1), plt.imshow(img_plt, 'gray'), plt.title("img_color")
            plt.subplot(2, 2, 2), plt.imshow(binary_img_plt, 'gray'), plt.title('binary_img')
            plt.subplot(2, 2, 3), plt.imshow(img_plt2, 'gray'), plt.title('binary_img')
            plt.show()
            # 等待用户按下键盘上的任意键
            plt.waitforbuttonpress()

        return result, img, binary_img


    def isMarkOk(self, area, w, h):
        mark_ok = 0
        rectangularity = area / (w * h)
        if 0.5 < rectangularity <= 0.85:
            self.mark_type_ix = 1  # 圆形
        elif 1 >= rectangularity > 0.85:
            self.mark_type_ix = 0  # 菱形

        if self.mark_type_ix == self.mark_type:
            mark_ok = 1  # 计算出的矩形度和设置的mark_type一致

        return mark_ok

if __name__ == "__main__":

    mark_detect = MarkDetect()

    ### 使用本地图片覆盖掉获取的图片，用于调试
    img_default = cv2.imdecode(np.fromfile("./mypic/Image__2024-04-24__ExposTime50ms.jpg", dtype=np.uint8), 1)

    detection_success, result_pos = mark_detect.mark_detect(img_default)

    for row in result_pos:
        # print("No: {}, Area: {}".format(i, cnt_area))
        point = (int(row[0]), int(row[1]))
        cv2.circle(img_default, point, radius=3, color=(0, 0, 255), thickness=-1)
    cv2.imshow('binary_img', img_default)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(detection_success)
    print(result_pos)
