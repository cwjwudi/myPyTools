"""
文件描述：用于测试modbus_tk slave
作者：Wenjie Cui
创建日期：2024.5.27
最后修改日期：2024.5.27
参考：https://blog.csdn.net/wsnd123321/article/details/126138031
"""


import sys

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp, hooks
import struct
import pandas as pd
'''
可使用的函数:
创建从站: server.add_slave(slave_id)
    slave_id(int):从站id
为从站添加存储区: slave.add_block(block_name, block_type, starting_address, size)
    block_name(str):block名
    block_type(int):block类型,COILS = 1,DISCRETE_INPUTS = 2,HOLDING_REGISTERS = 3,ANALOG_INPUTS = 4
    starting_address(int):起始地址
    size(int):block大小
设置block值:slave.set_values(block_name, address, values)
    block_name(str):block名
    address(int):开始修改的地址
    values(a list or a tuple or a number):要修改的一个(a number)或多个(a list or a tuple)值
获取block值:slave.get_values(block_name, address, size)
    block_name(str):block名
    address(int):开始获取的地址
    size(int):要获取的值的数量
'''
# 创建从站总服务器
server = modbus_tcp.TcpServer(address='127.0.0.1')  # address必须设置,port默认为502
print("running...")
print("enter 'quit' for closing the server")
server.start()

# 创建从站
slave_1 = server.add_slave(1)  # slave_id = 1
# 为从站添加存储区
slave_1.add_block(
    '0', cst.HOLDING_REGISTERS, 0, 1200
)  # block_name = '0', block_type = cst.HOLDING_REGISTERS, starting_address = 0, size = 1200

# 将数据存入寄存器
data = pd.read_csv('modbus_tcp.csv').values  # 读取数据data
num_array = data.flatten()  # 将data压为一维数组

registers_list = []  # 要存入寄存器的数据

# 将数据转化为32位float格式，每个数据4个字节 -> 占2个寄存器
for num in num_array:
    pi_bytes = [int(a_byte) for a_byte in struct.pack("f", num)]
    pi_register1 = pi_bytes[0] * 256 + pi_bytes[1]
    pi_register2 = pi_bytes[2] * 256 + pi_bytes[3]
    registers_list.append(pi_register1)
    registers_list.append(pi_register2)
slave_1.set_values(
    '0', 0, registers_list
)  # 将数据存入寄存器, block_name = '0', address = 0, values = registers_list

while True:
    cmd = sys.stdin.readline()  # input
    args = cmd.split(' ')  # 按空格分割输入

    if cmd.find('quit') == 0:  # 指令 quit -> 退出服务器
        print('bye-bye')
        break
