"""
文件描述：用于色标检测的Modbus Slave通信
作者：Wenjie Cui，Dr. Zhu
创建日期：2024.5.27
最后修改日期：2024.5.27
"""



import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import time
import numpy as np

ClientToServer = []
reconnectCmd = 0
head_tail_distance_mm = 14 #落地首尾标
C1 = 0
C2 = 0

def num2register(num):  # 一个数字转换为modbustcp中的两个寄存器[低16位，高16位]
    return [num & 65535, (num >> 16) & 65535]


def register2num(register0, register1):  # modbustcp中的两个寄存器转换为一个数字[低16位，高16位]
    return register0 + (register1 << 16)



class PaintingModbus:
    def __init__(self, ipStr):

        self.modbus_server = self.modbusInit(ipStr)

    def modbusInit(self, ipStr):
        """
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
        """
        # 创建从站总服务器
        # server = modbus_tcp.TcpServer(address='127.0.0.1')  # address必须设置,port默认为502
        # server = modbus_tcp.TcpServer(address='192.168.137.66')  # address必须设置,port默认为502 工控机
        server = modbus_tcp.TcpServer(address=ipStr)  # address必须设置,port默认为502
        server.start()
        # 创建从站
        slave_1 = server.add_slave(1)  # slave_id = 1
        # 为从站添加存储区
        slave_1.add_block(block_name='0', block_type=cst.HOLDING_REGISTERS, starting_address=0, size=17)
        slave_1.add_block(block_name='1', block_type=cst.ANALOG_INPUTS, starting_address=100, size=74)
        print("Modbus tcp running...")

        return slave_1

    def get_modbus_data(self, camera_ix):
        """
        计算圆的面积

        参数:
        radius (float): 圆的半径

        返回:
        float: 圆的面积
        """
        global head_tail_distance_mm, ClientToServer, C1, C2
        modbusdata = self.modbus_server.get_values(block_name='0', address=0, size=17)  #更换参数
        ClientToServer = modbusdata
        mark_shape = modbusdata[0]
        mark_size = modbusdata[1] * 0.001  # um->mm
        #size_limit_min = modbusdata[3] * 0.01  #更换参数
        #size_limit_max = modbusdata[4] * 0.01  #更换参数
        size_limit_min = 0.6
        size_limit_max = 1.2
        # 根据相机索引号选择对应的数据
        if camera_ix == 0:
            #filed_of_view_X_mm = modbusdata[5]  #更换参数

            ### 设置初始状态下的长度范围，对应像素宽的物理宽
            filed_of_view_X_mm = 50
            #exposure_time = modbusdata[7]  #更换参数

            ### 设置曝光时间
            exposure_time = max(modbusdata[2],30) #standard 26以上限制
        elif camera_ix == 1:
            #filed_of_view_X_mm = modbusdata[6]  #更换参数

            ### 设置初始状态下的长度范围，对应像素宽的物理宽
            filed_of_view_X_mm = 50
            #exposure_time = modbusdata[8]  #更换参数

            ### 设置曝光时间
            exposure_time = max(modbusdata[3],30)
        head_tail_distance_mm = modbusdata[4]
        # image_save = modbusdata[5]
        image_save = 0
        # img_view = modbusdata[6]
        img_view = 1
        camera_run_type = modbusdata[7]
        reconnectCmd = modbusdata[8]
        C1 = modbusdata[15]
        C2 = modbusdata[16]

        # 对数据做一些限制
        if mark_shape not in [0, 1]:
            mark_shape = 0
        if mark_size <= 0:
            mark_size = 0.1
        if size_limit_min < 0:
            size_limit_min = 0
        if size_limit_max < 0:
            size_limit_max = 0
        if size_limit_max < size_limit_min:
            size_limit_max, size_limit_min = size_limit_min, size_limit_max  # 交换数据
        # if filed_of_view_X_mm <= 0:
        #     filed_of_view_X_mm = 0.1
        exposure_time = max(10, exposure_time)
        exposure_time = min(exposure_time, 100) #ultrashort 26以下
        head_tail_distance_mm = max(10, head_tail_distance_mm)
        head_tail_distance_mm = min(40, head_tail_distance_mm)
        if image_save not in [0, 1]:
            image_save = 0
        if img_view not in [0, 1]:
            img_view = 0
        if camera_run_type not in [0, 1]:
            camera_run_type = 0
        if reconnectCmd not in [0, 1]:
            reconnectCmd = 0

        return [mark_shape, mark_size, size_limit_min, size_limit_max, exposure_time, head_tail_distance_mm,
                image_save, img_view, camera_run_type, reconnectCmd]

    def set_modbus_data(self, result_pos, ix):
        values = []
        mark_num = min(result_pos.shape[0], 5)
        self.modbus_server.set_values(block_name='1', address=100 + ix + 14, values=[mark_num])
        pixel_pos_x = [0, 0, 0, 0, 0]
        pixel_pos_y = [0, 0, 0, 0, 0]
        color_mark = [0, 0, 0, 0, 0]
        for i, r in enumerate(result_pos):
            if i > 4:
                break
            pixel_pos_x[i] = int(r[0] * 100)
            pixel_pos_y[i] = int(r[1] * 100)
            color_mark[i] = int(r[3])


        pixel_pos_x_register, pixel_pos_y_register, color_register = [], [], []
        for x, y, z in zip(pixel_pos_x, pixel_pos_y, color_mark):
            pixel_pos_x_register = pixel_pos_x_register + num2register(x)
            pixel_pos_y_register = pixel_pos_y_register + num2register(y)
            color_register = color_register + [z]
        # 需添加坐标补齐处理，全部对至5色标，对位应满足要求
        values = values + pixel_pos_x_register + pixel_pos_y_register + color_register
        # self.modbus_server.set_values(block_name='0', address=100 + ix * 100 + 4, values=values)  #更换参数
        self.modbus_server.set_values(block_name='1', address=100 + ix * 25 + 16, values = values)
        # print(self.modbus_server.get_values(block_name='1', address=100, size=74))
        # self.modbus_server.set_values(block_name='1', address=100 + ix * 2 + 11, values = [mark_num])
        # self.modbus_server.set_values(block_name='1', address=100 + ix * 1 + 15, values = [mark_num])
        # self.modbus_server.set_values(block_name='1', address=100 + ix * 25 + 16, values = pixel_pos_x_register)
        return values

if __name__ == "__main__":
    ipStr = "127.0.0.1"

    print_modbus = PaintingModbus(ipStr)

    res = [
        [5.47750008e+02, 4.00249996e+02, 4.50000000e+01, 3.00000000e+00, 8.40000000e+01, 1.00000000e+00, 0.00000000e+00,
         0.00000000e+00],
        [7.04250008e+02, 3.89250004e+02, 4.50000000e+01, 3.00000000e+00, 1.40000000e+02, 1.00000000e+00, 0.00000000e+00,
         0.00000000e+00],
        [8.64500008e+02, 3.91500004e+02, 4.50000000e+01, 2.00000000e+00, 9.30000000e+01, 1.00000000e+00, 0.00000000e+00,
         0.00000000e+00],
        [1.03181693e+03, 3.88795391e+02, 4.81798325e+01, 0.00000000e+00, 1.60000000e+01, 1.00000000e+00, 0.00000000e+00,
         0.00000000e+00],
        [1.18750001e+03, 3.88500000e+02, 4.50000000e+01, 3.00000000e+00, 3.00000000e+01, 1.00000000e+00, 0.00000000e+00,
         0.00000000e+00]]

    result_pos = np.array(res)

    print_modbus.set_modbus_data(result_pos=result_pos, ix=0)
    i = 0
    while True:
        data = print_modbus.get_modbus_data(0)
        i = i+1
        time.sleep(1)
        print("{}, 数据: {}".format(i, data))


