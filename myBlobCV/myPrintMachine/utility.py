# -*- coding: utf-8 -*-
"""
文件描述：工具性程序
作者：Wenjie Cui
创建日期：2024.5.28
最后修改日期：2024.5.28
"""

def num2register(num):  # 一个数字转换为modbustcp中的两个寄存器[低16位，高16位]
    return [num & 65535, (num >> 16) & 65535]


def register2num(register0, register1):  # modbustcp中的两个寄存器转换为一个数字[低16位，高16位]
    return register0 + (register1 << 16)