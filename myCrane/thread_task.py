import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import time

from opcuaclient import OPCUAClient

# 全局变量，用于存储滑块的位置和线程状态
x, y = 50, 25  # 初始位置
x_trolley = 0
y_trolley = 46
running = True  # 线程运行标志
trajectory_x = []  # 记录轨迹的 x 坐标
trajectory_y = []  # 记录轨迹的 y 坐标

def rotate_point(cx, cy, angle, px, py):
    """绕中心点旋转点"""
    s = np.sin(angle)
    c = np.cos(angle)

    # 移动点到原点
    px -= cx
    py -= cy

    # 旋转
    new_x = px * c - py * s
    new_y = px * s + py * c

    # 移回原点
    return new_x + cx, new_y + cy

def get_rotated_rectangle(x, y, width, height, angle):
    """获取旋转后的矩形的四个角的坐标"""
    angle_rad = np.radians(angle)  # 将角度转换为弧度
    half_width = width / 2
    half_height = height / 2

    # 矩形的四个角
    corners = [
        (-half_width + x, -half_height + y),
        (half_width + x, -half_height + y),
        (half_width + x, half_height + y),
        (-half_width + x, half_height + y),
    ]

    # 旋转每个角
    rotated_corners = [rotate_point(x, y, angle_rad, cx, cy) for cx, cy in corners]
    return np.array(rotated_corners)

def brarea2pltarea(xbr, ybr, width):
    xplt = xbr - width / 2
    yplt = 0
    wplt = width
    hplt = ybr
    return xplt, yplt, wplt, hplt

def update_position():
    """动态更新滑块位置的函数"""
    global x, y, x_trolley, running
    opcua_client.connect()  # 连接到服务器
    try:
        while running:
            value = opcua_client.read_node(node_id)  # 读取节点值
            x = value[0]
            y = value[1]
            x_trolley = value[2]
            print(f"当前值: {value}")
            time.sleep(0.1)  # 每秒读取一次
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        opcua_client.disconnect()  # 断开连接

def show_slider_animation():
    """显示滑块动画的函数"""
    global x, y, x_trolley, y_trolley, running, trajectory_x, trajectory_y
    # 创建图形和轴
    fig, ax = plt.subplots()
    ax.set_xlim(-10, 150)
    ax.set_ylim(-10, 50)

    # 创建一个正方形作为滑块
    width, height = 6, 1
    slider_polygon = plt.Polygon(get_rotated_rectangle(x, y, width, height, 40), color='blue')
    ax.add_patch(slider_polygon)

    # 创建一个正方形trolley
    trolley_square = plt.Rectangle((x_trolley - 0.5, y_trolley - 0.5), 1, 1, color='black')
    ax.add_patch(trolley_square)

    # 创建障碍物
    obstacles = [
        (75, 25, 50),
        (80, 30, 20),
        (120, 20, 10),
        (128.5, 10, 5),
        (80, 5, 75)
    ]
    for xbr, ybr, width in obstacles:
        xplt, yplt, wplt, hplt = brarea2pltarea(xbr, ybr, width)
        obstacle = plt.Rectangle((xplt, yplt), wplt, hplt, color='red')  # 障碍物位置和大小
        ax.add_patch(obstacle)

    # 轨迹线，设置为虚线
    trajectory_line, = ax.plot([], [], color='green', linestyle='--', label='traj')
    connection_line, = ax.plot([], [], color='orange', linestyle='-', label='line')  # 连接线
    ax.legend()

    # 更新函数
    def update(frame):
        slider_roate_angle = math.degrees(math.atan(-(x - x_trolley)/(y - y_trolley)))
        slider_polygon.set_xy(get_rotated_rectangle(x, y, 6, 1, slider_roate_angle))  # 更新滑块的位置
        trolley_square.set_xy((x_trolley - 0.5, y_trolley - 0.5))  # 更新 trolley 的位置

        # 记录轨迹
        trajectory_x.append(x)
        trajectory_y.append(y)

        # 更新轨迹线
        trajectory_line.set_data(trajectory_x, trajectory_y)

        # 更新连接线
        connection_line.set_data([x, x_trolley], [y, y_trolley])  # 连接滑块和 trolley

        return slider_polygon, trolley_square, trajectory_line, connection_line

    # 清除轨迹的函数
    def clear_trajectory(event):
        global trajectory_x, trajectory_y
        trajectory_x.clear()  # 清空 x 轨迹
        trajectory_y.clear()  # 清空 y 轨迹
        trajectory_line.set_data([], [])  # 更新轨迹线为空
        connection_line.set_data([], [])  # 更新连接线为空
        plt.draw()  # 重新绘制图形

    # 创建动画
    ani = FuncAnimation(fig, update, frames=np.arange(0, 100), interval=100)

    # 关闭窗口时的事件处理
    def on_close(event):
        global running
        running = False  # 设置标志，停止线程
        plt.close(fig)  # 关闭图形窗口

    # 连接关闭事件和按键事件
    fig.canvas.mpl_connect('close_event', on_close)
    fig.canvas.mpl_connect('key_press_event', clear_trajectory)

    plt.grid()
    plt.rcParams['font.sans-serif'] = ['Arial']  # 或者使用其他系统默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    plt.title('2D Animation with Movable Square Slider and Obstacle (Press D to Clear Trajectory)')
    plt.show()

if __name__ == "__main__":
    node_id = "ns=6;s=::AsGlobalPV:gActLoadPosition"
    opcua_client = OPCUAClient()

    # 启动更新位置的线程
    position_thread = threading.Thread(target=update_position)
    position_thread.start()

    # 显示滑块动画
    show_slider_animation()

    # 等待线程结束
    position_thread.join()
