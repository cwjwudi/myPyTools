# -*- coding: utf-8 -*-
"""
文件描述：主程序
作者：Wenjie Cui
创建日期：2024.5.28
最后修改日期：2024.5.28
"""

from printing_blob import MarkDetect
from printing_modbus import PaintMachineModbusServer

import threading
import time
import yaml
import cv2
import numpy as np
from array import array


class GlobalData:
    def __init__(self, yaml_path: str):
        self.C2 = None
        self.C1 = None
        self.mark_num = None
        self.resolution_X = None
        self.head_tail_distance_mm = None
        self.field_of_view_X_mm = None
        self.initGlobalData(yaml_path)

    def initGlobalData(self, yaml_path: str) -> None:
        # 加载并读取 YAML 文件
        with open(yaml_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        self.field_of_view_X_mm = data['field_of_view_X_mm']  # 长度 落地
        self.head_tail_distance_mm = data['head_tail_distance_mm']
        self.resolution_X = data['resolution_X']
        self.mark_num = data['mark_num']

        self.C1 = data['blob']['C1']
        self.C2 = data['blob']['C2']


def run_in_thread(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


def get_img():
    img = cv2.imdecode(np.fromfile("mypic/Image__2024-04-24__ExposTime50ms.jpg", dtype=np.uint8), 1)
    return img


def update_para(ix: int):
    data = print_modbus.readPrintMachinePara(camera_ix=ix)
    # [mark_shape, mark_size, size_limit_min, size_limit_max, exposure_time, head_tail_distance_mm,
    #  image_save, img_view, camera_run_type, reconnectCmd, C1, C2]
    para = array('i', [data[5], data[-2], data[-1]])
    return para


def pre_detect(ix: int):
    img = get_img()
    para = update_para(ix=ix)
    return img, para


def post_detect(result_pos, ix: int):
    pass


@run_in_thread
def run(ix: int):
    # rl
    mark_detect = MarkDetect(config_path)
    interval = 0.1
    while True:
        start_time = time.time()

        img, para = pre_detect(ix=ix)
        result_pos = mark_detect.mark_detect(img=img, para=para)
        post_detect(result_pos=result_pos, ix=ix)

        task_time = time.time() - start_time

        wait_time = interval - task_time
        print("ix={}, wait_time={:.2f}ms".format(ix, wait_time * 1000))
        if wait_time > 0:
            time.sleep(wait_time)


if __name__ == "__main__":
    config_path = 'config.yaml'

    globalData = GlobalData(config_path)
    print_modbus = PaintMachineModbusServer(ipStr="127.0.0.1")

    run(0)
    run(1)

    print("main thread over")
