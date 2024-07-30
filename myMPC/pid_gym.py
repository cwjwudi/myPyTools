import gym
import numpy as np
import keyboard

from env.InvertedPendulumEnv import InvertedPendulumEnv_Ctrl, InvertedPendulumEnv_Ctrl2



if __name__ == "__main__":
    # 生成环境
    # env = InvertedPendulumEnv_Ctrl2(cfg="./env/config.yaml")
    env = InvertedPendulumEnv_Ctrl(render_mode="human")

    env.init_qpos = 0.2
    # 环境初始化
    state = env.reset()
    state = state[0]
    # 设置完成时间，单位s
    done_time = 10.0
    total_time = 0.0
    # 循环交互
    while True:
        # render
        env.render()

        # Controller
        pos_pole = state[1]
        vel_pole = state[3]
        pos_cart = state[0]
        vel_cart = state[2]

        u_pole = 5 * (pos_pole - 0) + 0.11 * vel_pole
        u_cart = 1 * (pos_cart - 0) + 0.2 * vel_cart
        action = u_pole + u_cart
        action = np.clip(action, -3, 3)
        action = np.array([action])

        # contact with the env
        state, reward, done, _, info = env.step(action)
        print('state = {0}; reward = {1}'.format(state, reward))

        # 计算是否达到done时间
        total_time = total_time + env.dt
        if total_time > done_time:
            done = True

        # 判断当前episode 是否完成
        if done:
            print('done')
            break

        # 检查是否按下 'q' 键
        if keyboard.is_pressed('q'):
            print('Exiting...')
            break

    # 环境结束
    env.close()
