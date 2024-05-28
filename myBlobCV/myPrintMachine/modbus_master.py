from modbus_tk import modbus_tcp, defines
import time

# 创建 Modbus TCP 主站
master = modbus_tcp.TcpMaster(host="127.0.0.1", port=502)

try:
    # 连接主站
    master.open()

    while True:
        # 要写入的数据
        address = 0x0001  # 从站地址
        start_address = 0  # 起始寄存器地址，对应 40001
        values_to_write = [10, 20, 30, 40, 50]  # 要写入的值

        # 将数据写入从站的保持寄存器
        master.execute(address, defines.WRITE_MULTIPLE_REGISTERS, start_address, output_value=values_to_write)

        print(f'Write values: {values_to_write}')

        time.sleep(1)  # 等待1秒钟

finally:
    # 关闭主站连接
    master.close()
