import gym

from gym.envs.mujoco.inverted_pendulum_v4 import InvertedPendulumEnv
import time
import numpy as np


class InvertedPendulumEnv_Ctrl(InvertedPendulumEnv):
    def step(self, a):
        reward = 1.0
        self.do_simulation(a, self.frame_skip)
        ob = self._get_obs()
        terminated = bool(not np.isfinite(ob).all() or (np.abs(ob[1]) > 0.5))
        if self.render_mode == "human":
            self.render()
        return ob, reward, terminated, False, {}


# 生成环境
env = InvertedPendulumEnv_Ctrl(render_mode="human")
env.init_qpos = 0.2
# env = gym.make('InvertedPendulum-v4',  render_mode="human")
# 环境初始化
state = env.reset()
state = state[0]
# 循环交互
while True:
    # 渲染画面
    env.render()
    # 从动作空间随机获取一个动作
    pos_pole = state[1]
    vel_pole = state[3]

    pos_cart = state[0]
    vel_cart = state[2]

    u_pole = 5*(pos_pole - 0) + 0.11*vel_pole
    u_cart = 1*(pos_cart - 0) + 0.2*vel_cart
    action = u_pole + u_cart
    action = np.array([action])


    # action = env.action_space.sample()
    # agent与环境进行一步交互
    state, reward, done, _, info = env.step(action)
    print('state = {0}; reward = {1}'.format(state, reward))
    # 判断当前episode 是否完成
    if done:
        print('done')
        break
    # time.sleep(1)
# 环境结束
env.close()