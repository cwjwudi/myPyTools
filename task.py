from typing import Union, Dict, List, Any
from PySide6.QtWidgets import QFileDialog
import os
import yaml

def add(a: Union[float, int],
        b: Union[float, int]) -> float:
    """
    计算两数之和 (取到小数点后两位)
    :param a: 第一个数
    :param b: 第二个数
    :return: 两数之和
    """
    return round(a + b, 2)

def has_separator_line(content):
    for line in content.splitlines():
        if line.strip() == '---':
            return True
    return False

def analyStatus(root_path):
    status_dict = {}
    assignee_dict = {}

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
                status = data.get('Status', None)
                assignee = data.get('Assign to person', 'None')  # 如果 'Assign to person' 为空，则默认为 'None'
                if status:
                    status_dict[status] = status_dict.get(status, 0) + 1
                assignee_dict[assignee] = assignee_dict.get(assignee, 0) + 1  # 无论 'Assign to person' 是否为空，都进行统计
            except yaml.YAMLError as e:
                print(f"Error in {filename}: {e}")

    # for status, count in status_dict.items():
    #     print(f"Status: {status}, Count: {count}")
    #
    # for assignee, count in assignee_dict.items():
    #     print(f"Assignee: {assignee}, Count: {count}")

    return status_dict, assignee_dict

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


if __name__ == '__main__':
    print(add(1, 2))  # result: 3
