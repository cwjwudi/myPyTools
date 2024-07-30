import gym
import numpy as np
import keyboard
import random

from envs.InvertedPendulumEnv import InvertedPendulumEnv_Ctrl, InvertedPendulumEnv_Ctrl2

def PID_controller(state):
    # Controller
    pos_pole = state[1]
    vel_pole = state[3]
    pos_cart = state[0]
    vel_cart = state[2]

    u_pole = 5 * (pos_pole - 0) + 0.11 * vel_pole
    u_cart = 1 * (pos_cart - 0) + 0.2 * vel_cart
    torque = u_pole + u_cart
    torque = np.clip(torque, -3, 3)
    torque = np.array([torque])

    return torque


if __name__ == "__main__":
    # 生成环境
    env = InvertedPendulumEnv_Ctrl2(cfg="./envs/config.yaml")

    env.init_qpos = 0.2
    # 环境初始化
    state = env.reset([0.0, random.uniform(-0.2, 0.2)])
    # 循环交互
    while True:
        action = PID_controller(state)
        # contact with the env
        state, reward, done, _ = env.step(action)
        print('state = {0}; reward = {1}'.format(state, reward))

        if True == done:
            env.reset([0.0, random.uniform(-0.2, 0.2)])
            continue

        # 检查是否按下 'esc' 键
        if keyboard.is_pressed('esc'):
            print('Exiting...')
            break

    # 环境结束
    env.close()
