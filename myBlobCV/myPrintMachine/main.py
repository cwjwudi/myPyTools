# -*- coding: utf-8 -*-
"""
文件描述：主程序
作者：Wenjie Cui
创建日期：2024.5.28
最后修改日期：2024.5.28
"""

from printing_blob import MarkDetect
from printing_modbus import PaintMachineModbusServer
import yaml

class GlobalData():
    def __init__(self, yaml_path: str):
        self.initGlobalData(yaml_path)

    def initGlobalData(self, yaml_path: str):
        # 加载并读取 YAML 文件
        with open(yaml_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        self.field_of_view_X_mm = data['field_of_view_X_mm']  #长度 落地
        self.head_tail_distance_mm = data['head_tail_distance_mm']
        self.resolution_X = data['resolution_X']
        self.mark_num = data['mark_num']

        self.C1 = data['blob']['C1']
        self.C2 = data['blob']['C2']



if __name__ == "__main__":
    config_path = 'config.yaml'

    mark_detect = MarkDetect(config_path)

    globalData = GlobalData(config_path)

    print(globalData.C1)

