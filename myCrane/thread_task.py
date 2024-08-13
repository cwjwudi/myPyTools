import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import time

from opcuaclient import OPCUAClient

# 全局变量，用于存储滑块的位置和线程状态
x, y = 50, 25  # 初始位置
running = True  # 线程运行标志

def update_position():
    """动态更新滑块位置的函数"""
    global x, y, running
    opcua_client.connect()  # 连接到服务器
    try:
        while running:
            value = opcua_client.read_node(node_id)  # 读取节点值
            x = value[0]
            y = value[1]
            print(f"当前值: {value}")
            time.sleep(0.2)  # 每0.2秒读取一次
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        opcua_client.disconnect()  # 断开连接

def show_slider_animation():
    """显示滑块动画的函数"""
    global x, y, running
    # 创建图形和轴
    fig, ax = plt.subplots()
    ax.set_xlim(-10, 120)
    ax.set_ylim(-10, 50)

    # 创建一个正方形作为滑块
    slider_square = plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color='blue')
    ax.add_patch(slider_square)

    # 创建障碍物
    obstacle = plt.Rectangle((0.5, 0.5), 2, 2, color='red')  # 障碍物位置和大小
    ax.add_patch(obstacle)

    # 更新函数
    def update(frame):
        global x, y
        slider_square.set_xy((x - 0.5, y - 0.5))  # 更新滑块的位置
        return slider_square,

    # 创建动画
    ani = FuncAnimation(fig, update, frames=np.arange(0, 100), interval=100)

    # 关闭窗口时的事件处理
    def on_close(event):
        global running
        running = False  # 设置标志，停止线程
        plt.close(fig)  # 关闭图形窗口

    # 连接关闭事件
    fig.canvas.mpl_connect('close_event', on_close)

    plt.grid()
    plt.title('2D Animation with Movable Square Slider and Obstacle')
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
