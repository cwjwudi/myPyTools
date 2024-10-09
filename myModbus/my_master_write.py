"""
 2024.10.9
 用于测试任务链解析
 """

import modbus_tk
import modbus_tk.modbus_tcp as modbus_tcp

try:
    # 连接到 Modbus Slave
    master = modbus_tcp.TcpMaster('127.0.0.1', 502)  # 使用你的设备 IP
    master.set_timeout(5.0)

    # 要写入的字符串
    string_to_write = "1-2-3-4-5-6-7-8"

    # 将字符串转换为字节
    byte_array = string_to_write.encode('ascii')

    # 将字节转换为 16 位整数
    registers = []
    for i in range(0, len(byte_array), 2):
        if i + 1 < len(byte_array):
            # byte 8bit，而modbus寄存器16bit，所以要把数据左移到高位
            registers.append((byte_array[i+1] << 8) + byte_array[i])
        else:
            registers.append(byte_array[i])

    # 写入 Holding Registers，从地址 4008 开始（Modbus 0-based）
    start_address = 7  # 确保这个地址是正确的
    response = master.execute(1, 16, start_address, len(registers), registers)

    print("写入成功:", string_to_write, "响应:", response)

except modbus_tk.modbus.ModbusError as e:
    print("Modbus 错误:", e)

except Exception as e:
    print("发生错误:", e)

finally:
    master.close()
