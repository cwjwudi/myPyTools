# -*- coding: utf-8 -*-
import yaml


class GlobalData:
    def __init__(self, yaml_path: str):
        self.C2 = None
        self.C1 = None
        self.mark_num = None
        self.resolution_X = None
        self.head_tail_distance_mm = None
        self.field_of_view_X_mm = None
        self.initGlobalData(yaml_path)

        self.stop_print_machine = False

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