# -*- coding: utf-8 -*-

from modbus_tk import modbus_tcp, defines
import time

# 创建 Modbus TCP 主站
master = modbus_tcp.TcpMaster(host="127.0.0.1", port=502)

try:
    # 连接主站
    master.open()

    while True:
        # 要读取的数据
        address = 0x0001  # 从站地址
        start_address = 30101  # 起始寄存器地址，对应 30101
        number_of_registers = 50  # 要读取的寄存器数量

        # 读取从站的保持寄存器数据
        response = master.execute(address, defines.READ_HOLDING_REGISTERS, start_address, number_of_registers)

        # 解析响应数据
        if response:
            data_read = response[0]
            print(f'Read values: {data_read}')

        time.sleep(1)  # 等待1秒钟

finally:
    # 关闭主站连接
    master.close()
