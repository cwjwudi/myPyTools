import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
import csv
import re
import tkinter as tk
from tkinter import simpledialog
import pandas as pd
from sympy import false
from datetime import datetime



def extract_number(segment_string):
    match = re.search(r'\d+', segment_string)
    if match:
        return int(match.group(0))
    return None

class MouseEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'MouseEvent(x={self.x}, y={self.y})'

class Segment:
    def __init__(self, segment_id, x, y, name, is_master):
        self.segment_id = segment_id
        self.x = x
        self.y = y
        self.name = name
        self.is_master = is_master
        self.size = 0.24

    def __repr__(self):
        return (f"Segment(ID={self.segment_id}, X={self.x}, Y={self.y}, "
                f"Name={self.name}, IsMaster={self.is_master})")

class Square:
    def __init__(self, patch, original_color, segment_id, x, y):
        self.patch = patch
        self.original_color = original_color
        self.segment_id = segment_id
        self.x = x
        self.y = y
        self.size = 0.12
        self.area_name = ""

    def __repr__(self):
        return (f"Square(patch={self.patch}, "
                f"original_color={self.original_color}, "
                f"segment_id={self.segment_id}, "
                f"x={self.x},"
                f"y={self.y},"
                f"size={self.size})")

def getSmallSegments(segment_list):
    global colors
    key_points = []
    squares = []
    size = 0.24
    for segment in segment_list:
        if segment.x is not None and segment.y is not None:
            x = float(segment.x) * size
            y = float(segment.y) * size


            x_index = int(segment.x)
            color_index = int(x_index // 3) % len(colors)
            color = colors[color_index]

            corners = [
                (x, y),
                (x + size, y),
                (x, y + size),
                (x + size, y + size),
                (x + size / 2, y + size / 2)
            ]

            key_points.extend(corners)

            square_patch = plt.Rectangle((x, y), size , size , fill=True,
                                         edgecolor='white', facecolor=color)
            square = Square(patch=square_patch, original_color=color,
                            segment_id=extract_number(segment.segment_id),
                            x=x, y=y)
            squares.append(square)


    return squares, key_points


def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    segments = root.findall(".//Group[@ID='Segments']/Group")
    segment_list = []

    for segment in segments:
        segment_id = segment.attrib['ID']
        x_property = segment.find("Property[@ID='X']")
        y_property = segment.find("Property[@ID='Y']")
        name_property = segment.find("Property[@ID='Name']")
        is_master_property = segment.find("Property[@ID='IsMaster']")

        x_value = x_property.get('Value') if x_property is not None else None
        y_value = y_property.get('Value') if y_property is not None else None
        name_value = name_property.get('Value') if name_property is not None else None
        is_master_value = is_master_property.get('Value') if is_master_property is not None else None

        segment_instance = Segment(segment_id, x_value, y_value, name_value, is_master_value)
        segment_list.append(segment_instance)

    return segment_list

def setup_plot(segment_list, rectangles):
    global colors
    fig, ax = plt.subplots()
    markers = []

    # 获取所有小方块，加入图中
    squares, key_points = getSmallSegments(segment_list)
    size = 0.24
    for iter in range(len(squares)):
        ax.add_patch(squares[iter].patch)
        # 标注文本
        if iter % 4 == 0:
            ax.text(squares[iter].x + size / 4, squares[iter].y + size / 4,
                    squares[iter].segment_id, ha='center', va='center', fontsize=12, color='white')

    text = ax.text(0, 0, '', fontsize=12, color='black')

    """
    2024.10.9
    根据读取的point，绘制区域
    """
    for rectangle in rectangles:
        bottom_left = (rectangle['bottom_left_x'], rectangle['bottom_left_y'])  # 左下角坐标
        top_right = (rectangle['top_right_x'], rectangle['top_right_y'])  # 右上角坐标

        # 绘制矩形
        rect_patch = plt.Rectangle(bottom_left,
                                    top_right[0] - bottom_left[0],
                                    top_right[1] - bottom_left[1],
                                    fill=True, edgecolor='black', facecolor='white', linewidth=2)
        ax.add_patch(rect_patch)
        # ax.text(bottom_left[0] + size / 4, bottom_left[1] + size / 4,
        #         rectangle['nick_name'] + str(int(rectangle['index'])), ha='center', va='center', fontsize=6, color='black')

        ax.text(bottom_left[0] + size / 4, bottom_left[1] + size / 4,
                rectangle['nick_name'], ha='center', va='center', fontsize=6, color='black')
        # 计算矩形的四个角点
        bottom_right = (top_right[0], bottom_left[1])
        top_left = (bottom_left[0], top_right[1])
        points = [bottom_left, top_right, bottom_right, top_left]
        # 把矩形的四个角的点加入关键点，可以被捕获
        key_points.extend(points)



    def on_move(event):
        if event.inaxes:
            mouse_x, mouse_y = event.xdata, event.ydata
            closest_point = None
            min_distance = float('inf')

            for point in key_points:
                distance = np.sqrt((mouse_x - point[0]) ** 2 + (mouse_y - point[1]) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_point = point

            if min_distance < 0.1:
                text.set_position(closest_point)
                text.set_text(f'({closest_point[0]:.2f}, {closest_point[1]:.2f})')

                if markers:
                    for marker in markers:
                        marker.remove()
                    markers.clear()

                marker = ax.plot(closest_point[0], closest_point[1], 'ro', markersize=8)
                markers.append(marker[0])
            else:
                text.set_text('')

            fig.canvas.draw_idle()

    def on_click(event):
        global click_color_index

        if event.inaxes:
            mouse_x, mouse_y = event.xdata, event.ydata

            def contain_point(rect, point):
                left_bottom_x = rect.get_x()
                left_bottom_y = rect.get_y()
                right_top_x = left_bottom_x + rect.get_width()
                right_top_y = left_bottom_y + rect.get_height()

                return (point.x > left_bottom_x and point.x < right_top_x) and (point.y > left_bottom_y and point.y < right_top_y)

            for square in squares:
                rect = square.patch
                mouse_event = MouseEvent(mouse_x, mouse_y)
                if contain_point(rect, mouse_event):
                    if event.button == 1:  # 左键点击
                        new_color = colors[click_color_index % len(colors)]
                        click_color_index += 1
                        rect.set_facecolor(new_color)
                        fig.canvas.draw_idle()
                    elif event.button == 3:  # 右键点击
                        # 弹出输入框获取新的 area_name
                        root = tk.Tk()
                        root.withdraw()  # 隐藏主窗口
                        new_area_name = simpledialog.askstring("Input", "Enter new area name:", parent=root)
                        if new_area_name is not None:
                            square.area_name = new_area_name
                            print(f"Updated area_name of segment {square.segment_id} to '{new_area_name}'")
                            # 更新文本显示
                            ax.text(square.x + square.size / 4, square.y + square.size / 4,
                                    square.area_name, ha='center', va='center', fontsize=10, color='white')
                        break

    # 连接事件
    fig.canvas.mpl_connect('motion_notify_event', on_move)
    fig.canvas.mpl_connect('button_press_event', on_click)

    ax.set_xlim(-0.1, 7)
    ax.set_ylim(-0.1, 0.6)
    ax.set_aspect('equal', adjustable='box')

    # 启用缩放功能
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.title("Right-click to edit area name, Left-click to change color")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    plt.show()

"""
2024.10.9
读取xls中的所有area点位
"""
def read_rectangles(file_path: str, sheet_name: str):
    rectangles = []
    # 使用 pandas 读取 Excel 文件
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    for index, row in df.iterrows():
        if pd.isna(row['name']) == false:  # 空行不读取
            rectangles.append(row)

    return rectangles


def generate_area_ID(base_name, number):
    number_str = str(int(number))
    zero_str = ''
    if int(number/10) == 0:
        zero_str = '00'
    elif int(number/100) == 0:
        zero_str = '0'
    # 组合字符串
    area_name = f"{base_name}{zero_str}{number_str}"
    return area_name

"""
2024.10.9
生成区域定义程序，并保存成文件
"""
def generate_navigation_definition(rectangles):
    # 打开一个文本文件以写入
    with open('actCfgArea.st', 'w', encoding="GB2312") as f:
        # 生成当前日期
        current_date = datetime.now().strftime("%Y年%m月%d日")

        # 文件内容
        head_content = f"""(* 
          文件名: actCfgArea.st
          描述: 自动生成的点位定义程序
          日期: {current_date}

          说明:
          - 该程序为自动生成，正确性需要自行判断
          - 请查看输出图形区域定义是否符合要求
        *) \nACTION actCfgArea: \n\n"""

        f.write(head_content)  # 写入程序头

        for rectangle in rectangles:
            area_index = int(rectangle['index'])
            AreaID = generate_area_ID(rectangle['name'] , rectangle['index'])
            Vaild = True
            StationID = int(rectangle['station_id'])
            BottomLeft_X = rectangle['bottom_left_x']
            BottomLeft_Y = rectangle['bottom_left_y']
            TopRight_X = rectangle['top_right_x']
            TopRight_Y = rectangle['top_right_y']

            f.write(f"gArea[{area_index}].Cfg.AreaID := '{AreaID}';\n")
            f.write(f"gArea[{area_index}].Cfg.Vaild := {Vaild};\n")
            f.write(f"gArea[{area_index}].Cfg.StationID := {StationID};\n")
            f.write(f"gArea[{area_index}].Cfg.BottomLeft.X := {BottomLeft_X:.3f};\n")
            f.write(f"gArea[{area_index}].Cfg.BottomLeft.Y := {BottomLeft_Y:.3f};\n")
            f.write(f"gArea[{area_index}].Cfg.TopRight.X := {TopRight_X:.3f};\n")
            f.write(f"gArea[{area_index}].Cfg.TopRight.Y := {TopRight_Y:.3f};\n\n")

        f.write("END_ACTION")

    print("数据已成功保存到 actCfgArea.st")

def main():
    segment_list = parse_xml('CfgLayout.layout6d')
    rectangles = read_rectangles('rectangles_old.xlsx', 'rectangles')
    generate_navigation_definition(rectangles)
    setup_plot(segment_list, rectangles)

if __name__ == "__main__":
    click_color_index = 0
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'cyan']

    main()
