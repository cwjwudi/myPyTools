import gym
import keyboard
import random
import numpy as np

from LQR import LQR
from envs.InvertedPendulumEnv import InvertedPendulumEnv_Ctrl2

Q = np.eye(5)
Q[0, 0] = 10
Q[1, 1] = 15
Q[2, 2] = 30
Q[3, 3] = 6
Q[4, 4] = 1

x_n = 4
u_n = 1

G = np.loadtxt('./envs/G.txt')
H = np.loadtxt('./envs/H.txt').reshape(4, 1)
F_t = np.concatenate([G, H], axis=1)

f_t = np.zeros((x_n, 1))
C_t = Q
c_t = np.zeros((x_n+u_n, 1))


if __name__ == "__main__":
    # 生成环境
    env = InvertedPendulumEnv_Ctrl2(cfg="./envs/config.yaml")

    env.init_qpos = 0.2
    # 环境初始化
    # state = env.reset([0.0, random.uniform(-0.2, 0.2)])
    state = env.reset([0.0, 0.0])


    lqr = LQR(x_n, u_n, F_t, f_t, C_t, c_t)
    x_0 = state.copy().reshape(x_n, 1)
    T = 100
    t = 15
    i = 0
    # 循环交互
    while True:
        # contact with the env

        u_seq = lqr(x_0, T)
        for j in range(t):
            action = np.clip(u_seq[j][0], -10, 10)
            obs, _, done, _ = env.step(action)
            print("Step[{}]| Obs:{}| Control:{}".format(i, obs, u_seq[j][0]))
            x_0 = obs.copy().reshape(x_n, 1)
            i += 1
        # # Use Ctrl + c to stop
        # except KeyboardInterrupt:
        #     print("stop")


        if True == done:
            env.reset([0.0, random.uniform(-0.2, 0.2)])
            continue

        # 检查是否按下 'esc' 键
        if keyboard.is_pressed('esc'):
            print('Exiting...')
            break

    # 环境结束
    env.close()
