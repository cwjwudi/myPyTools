import xml.etree.ElementTree as ET

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

# 输出所有的Segment实例

print(f'RowSeg={seg_row}, RowCol={seg_col}')
for segment in segment_list:
    print(segment)
