import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

import re


def extract_number(segment_string):
    """
    从给定的字符串中提取数字。

    参数:
    segment_string (str): 输入的字符串，例如 'Segment[11]'。

    返回:
    int: 提取出的数字，如果没有找到数字则返回 None。
    """
    match = re.search(r'\d+', segment_string)
    if match:
        return int(match.group(0))  # 返回提取的数字作为整数
    return None  # 如果没有找到数字，返回 None


# 定义一个结构体类来存储Segment的属性
class Segment:
    def __init__(self, segment_id, x, y, name, is_master):
        self.segment_id = segment_id
        self.x = x
        self.y = y
        self.name = name
        self.is_master = is_master

    def __repr__(self):
        return (f"Segment(ID={self.segment_id}, X={self.x}, Y={self.y}, "
                f"Name={self.name}, IsMaster={self.is_master})")


# 解析XML文件
tree = ET.parse('CfgLayout.layout6d')  # 假设文件名为 example.xml
root = tree.getroot()

# 获取SegRow和SegCol的值
seg_row_property = root.find(".//Group[@ID='Segments']/Property[@ID='SegRow']")
seg_col_property = root.find(".//Group[@ID='Segments']/Property[@ID='SegCol']")

seg_row = seg_row_property.get('Value') if seg_row_property is not None else None
seg_col = seg_col_property.get('Value') if seg_col_property is not None else None

# 找到所有的 Segment 组
segments = root.findall(".//Group[@ID='Segments']/Group")

# 创建一个列表来存储所有的Segment实例
segment_list = []

for segment in segments:
    # 获取各个属性
    segment_id = segment.attrib['ID']
    x_property = segment.find("Property[@ID='X']")
    y_property = segment.find("Property[@ID='Y']")
    name_property = segment.find("Property[@ID='Name']")
    is_master_property = segment.find("Property[@ID='IsMaster']")

    # 获取属性值
    x_value = x_property.get('Value') if x_property is not None else None
    y_value = y_property.get('Value') if y_property is not None else None
    name_value = name_property.get('Value') if name_property is not None else None
    is_master_value = is_master_property.get('Value') if is_master_property is not None else None

    # 创建Segment实例并添加到列表
    segment_instance = Segment(segment_id, x_value, y_value, name_value, is_master_value)
    segment_list.append(segment_instance)

# 创建图形
fig, ax = plt.subplots()

# 存储关键点和对应的标记
key_points = []
markers = []

# 定义颜色列表
colors = ['blue', 'green', 'red', 'orange', 'purple', 'cyan']

# 绘制方块
for segment in segment_list:
    if segment.x is not None and segment.y is not None:
        x = float(segment.x) * 0.24
        y = float(segment.y) * 0.24
        size = 0.24

        # 计算颜色索引
        x_index = int(segment.x)
        color_index = int(x_index // 3) % len(colors)  # 每3个大方块换一种颜色
        # print(f'x,y:({x}, {y}), index:{color_index}')
        color = colors[color_index]

        # 绘制小正方形并计算其四个角和中心
        for i in range(2):
            for j in range(2):
                small_x = x + (i * size / 2)
                small_y = y + (j * size / 2)

                # 计算小正方形的四个角和中心
                corners = [
                    (small_x, small_y),  # 左下角
                    (small_x + size / 2, small_y),  # 右下角
                    (small_x, small_y + size / 2),  # 左上角
                    (small_x + size / 2, small_y + size / 2),  # 右上角
                    (small_x + size / 4, small_y + size / 4)  # 中心
                ]

                # 添加到关键点列表
                key_points.extend(corners)

                # 绘制小正方形
                ax.add_patch(plt.Rectangle((small_x, small_y), size / 2, size / 2, fill=True, edgecolor='black',
                                           facecolor=color))

                # 只在左下角的小方块中显示Segment ID
                if i == 0 and j == 0:  # 左下角小方块
                    ax.text(small_x + size / 4, small_y + size / 4, extract_number(segment.segment_id),
                            ha='center', va='center', fontsize=12, color='white')

# 添加坐标显示文本
text = ax.text(0, 0, '', fontsize=12, color='black')


# 定义鼠标移动事件的回调函数
def on_move(event):
    if event.inaxes:  # 确保鼠标在坐标轴内
        mouse_x, mouse_y = event.xdata, event.ydata
        closest_point = None
        min_distance = float('inf')

        # 检查鼠标与关键点的距离
        for point in key_points:
            distance = np.sqrt((mouse_x - point[0]) ** 2 + (mouse_y - point[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_point = point

        # 如果距离小于一定阈值，显示坐标并标记选中点
        if min_distance < 0.1:  # 可以调整这个阈值
            text.set_position(closest_point)
            text.set_text(f'({closest_point[0]:.2f}, {closest_point[1]:.2f})')

            # 更新标记
            if markers:
                for marker in markers:
                    marker.remove()  # 清除之前的标记
                markers.clear()

            # 添加新的标记
            marker = ax.plot(closest_point[0], closest_point[1], 'ro', markersize=8)  # 红色圆点
            markers.append(marker[0])  # 存储标记以便后续清除
        else:
            text.set_text('')  # 鼠标不在关键点附近时清空文本

        fig.canvas.draw_idle()  # 更新图形


# 连接鼠标移动事件
fig.canvas.mpl_connect('motion_notify_event', on_move)

# 设置坐标轴范围
ax.set_xlim(0, 6)
ax.set_ylim(0, 1)

# 显示图形
ax.set_aspect('equal', adjustable='box')
plt.show()
