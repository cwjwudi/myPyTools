import xml.etree.ElementTree as ET

# 解析XML文件
tree = ET.parse('CfgLayout.xml')  # 假设文件名为 example.xml
root = tree.getroot()

# 找到所有的 Segment 组
segments = root.findall(".//Group[@ID='Segments']/Group")

for segment in segments:
    # 获取各个属性
    x_property = segment.find("Property[@ID='X']")
    y_property = segment.find("Property[@ID='Y']")
    name_property = segment.find("Property[@ID='Name']")
    is_master_property = segment.find("Property[@ID='IsMaster']")

    # 获取属性值
    x_value = x_property.get('Value') if x_property is not None else None
    y_value = y_property.get('Value') if y_property is not None else None
    name_value = name_property.get('Value') if name_property is not None else None
    is_master_value = is_master_property.get('Value') if is_master_property is not None else None

    # 输出结果
    print(f"Segment ID: {segment.attrib['ID']}")
    print(f"  X: {x_value}")
    print(f"  Y: {y_value}")
    print(f"  Name: {name_value}")
    print(f"  IsMaster: {is_master_value}")
    print()
