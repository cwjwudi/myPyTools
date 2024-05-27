"""
文件描述：用于测试modbus_tk master
作者：Wenjie Cui
创建日期：2024.5.27
最后修改日期：2024.5.27
参考：https://blog.csdn.net/wsnd123321/article/details/126138031
"""


import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp, hooks
import numpy as np
import pandas as pd

master = modbus_tcp.TcpMaster()
master.set_timeout(5.0)
print("connected")

# 连接从站读取数据，一次最多读取125个寄存器，由于2个寄存器为一个数据，故 size 设置为124
data = []  # 存放读取的数据
data += master.execute(  # 向从站发报文读取[0,123]区间的寄存器数据
    1,  # 从站标识符
    cst.READ_HOLDING_REGISTERS,  # 功能码
    0,  # 起始寄存器地址
    124,  # 读取的寄存器数量
    data_format='62f',  # 数据解码格式
)
data += master.execute( # 向从站发送报文读取[124,247]区间的寄存器数据
    1, cst.READ_HOLDING_REGISTERS, 124, 124, data_format='62f'
)

# 将数据保存到csv文件中
if len(data) % 4 != 0:  # 如果数据长度不是4的倍数，则用 0 补齐
    for i in range(0, 4 - len(data) % 4):
        data.append(0)
data = np.reshape(data, (-1, 4))  # 将数据重新转为4列的二维数组
# print(data, data.shape) # 打印数据
df = pd.DataFrame(
    data, columns=['timestamp', 'lon', 'lat', 'cog']
)  # 将数据转为DataFrame，设置列名
df.to_csv('data_recv.csv', index=False)  # 将数据保存到csv文件中
