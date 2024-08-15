import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt


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
tree = ET.parse('CfgLayout.xml')  # 假设文件名为 example.xml
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

# # 绘制Segment方块
# plt.figure(figsize=(10, 10))

# 创建图形
fig, ax = plt.subplots()

# 绘制方块
for segment in segment_list:
    if segment.x is not None and segment.y is not None:
        x = float(segment.x) * 0.24
        y = float(segment.y) * 0.24
        size = 0.24

        for i in range(2):
            for j in range(2):
                small_x = x + (i * size / 2)
                small_y = y + (j * size / 2)
                ax.add_patch(plt.Rectangle((small_x, small_y), size / 2, size / 2, fill=True, edgecolor='black', facecolor='blue'))

# 添加坐标显示文本
text = ax.text(0, 0, '', fontsize=12, color='black')

# 定义鼠标移动事件的回调函数
def on_move(event):
    if event.inaxes:  # 确保鼠标在坐标轴内
        x, y = event.xdata, event.ydata
        text.set_position((x, y))
        text.set_text(f'({x:.2f}, {y:.2f})')
        fig.canvas.draw_idle()  # 更新图形

# 连接鼠标移动事件
fig.canvas.mpl_connect('motion_notify_event', on_move)

# 设置坐标轴范围
plt.xlim(0, 4)  # 根据需要调整
plt.ylim(0, 1)  # 根据需要调整
plt.grid(False)
plt.title('Segments Visualization')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.gca().set_aspect('equal', adjustable='box')

# 显示图形
ax.set_aspect('equal', adjustable='box')
plt.show()