# -*- coding: utf-8 -*-
"""
文件描述：工具性程序
作者：Wenjie Cui
创建日期：2024.5.28
最后修改日期：2024.5.28
"""

import threading


def num2register(num):  # 一个数字转换为modbustcp中的两个寄存器[低16位，高16位]
    return [num & 65535, (num >> 16) & 65535]


def register2num(register0, register1):  # modbustcp中的两个寄存器转换为一个数字[低16位，高16位]
    return register0 + (register1 << 16)


def run_in_thread(func):
    def wrapper(*args, **kwargs):
        event = threading.Event()
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread, event

    return wrapper


def stop_thread(thread: threading.Thread, event: threading.Event):
    if thread.is_alive():
        event.clear()
        thread.join()
        print("Thread {} has been stoped!".format(thread.name))
