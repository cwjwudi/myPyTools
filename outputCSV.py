from typing import Union, Dict, List, Any
from PySide6.QtWidgets import QFileDialog
import os
import yaml
import csv


def getPath(root_path):
    md_path_list: List[str] = []
    # 读取所有的文件名
    for root, dirs, files in os.walk(root_path):
        # 忽略包含 .obsidian 的文件夹
        dirs[:] = [d for d in dirs if not d.endswith('.obsidian')]
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                md_path_list.append(file_path)

    return md_path_list


def has_separator_line(content):
    for line in content.splitlines():
        if line.strip() == '---':
            return True
    return False


def analyStatus(root_path, name):
    outputData = []

    data_path_list = getPath(root_path)
    # 读取文件夹下的所有文件
    for filename in data_path_list:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            # 判断是否有‘---’标识符
            if has_separator_line(content):
                yaml_content = content.split('---')[1]  # 取出第一个 '---' 后的部分
            else:
                continue
            # 如果有，开始提取其中的关键字
            try:
                data = yaml.load(yaml_content, Loader=yaml.FullLoader)
                assignee = data.get('Assign to person', None)  # 如果 'Assign to person' 为空，则默认为 'None'
                # 统计分配的工程师
                if name == assignee:
                    data['filename'] = os.path.basename(filename)  # 将文件名添加到字典中
                    outputData.append(data)
            except yaml.YAMLError as e:
                print(f"Error in {filename}: {e}")

    # for _data in outputData:
    #     print(_data)

    return outputData


if __name__ == '__main__':
    # root_path = r'D:\projects\40_TSQ\tsq_support\2024年3月试运行'

    root_path = r'D:\projects\40_TSQ\tsq_support'
    name = 'Ma Ruiqi'

    data = analyStatus(root_path, name)

    # 检查并统一 'Cost' 字段名称为 'Time Cost'
    # 检查并填充 'Star' 字段
    for entry in data:
        if 'Cost' in entry:
            entry['Time Cost'] = entry.pop('Cost')  # 将 'Cost' 改为 'Time Cost'
        else:
            entry['Time Cost'] = 0  # 如果没有 'Cost' 字段，填充为 0

        if 'Star' not in entry:
            entry['Star'] = 0  # 如果没有 'Star' 字段，填充为 0

    # 指定CSV文件名
    csv_file = 'output.csv'

    # 写入CSV文件
    with open(csv_file, mode='w', newline='', encoding='gbk') as file:
        # 获取字典的字段名
        fieldnames = data[0].keys()

        # 创建CSV写入器
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # 写入表头
        writer.writeheader()

        # 写入数据
        writer.writerows(data)

    print(f"数据已写入 {csv_file}")