import gym

from gym.envs.mujoco.inverted_pendulum_v4 import InvertedPendulumEnv
import time
import numpy as np

class PID:
    def __init__(self, kp, ki, kd, dt):
        self.kp = kp  # 比例增益
        self.ki = ki  # 积分增益
        self.kd = kd  # 微分增益
        self.dt = dt  # 时间间隔

        self.previous_error = 0  # 上一个误差
        self.integral = 0  # 积分值

    def update(self, setpoint, measured_value):
        # 计算误差
        error = setpoint - measured_value

        # 计算积分
        self.integral += error * self.dt

        # 计算微分
        derivative = (error - self.previous_error) / self.dt

        # 计算 PID 输出
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)

        # 更新上一个误差
        self.previous_error = error

        return output


# 生成环境
env = InvertedPendulumEnv(render_mode="human")
# env = gym.make('InvertedPendulum-v4',  render_mode="human")
# 环境初始化
state = env.reset()


# PID

kp = 100
ki = 0
kd = 0.05
dt = 1.0  # 时间间隔为 1 秒

pid = PID(kp, ki, kd, env.dt)

setpoint = 0  # 目标值
measured_value = 0  # 初始测量值
# 循环交互
while True:
    # 渲染画面
    env.render()
    # 从动作空间随机获取一个动作
    measured_value = state[1]
    if not isinstance(measured_value, (int, float)):
        measured_value = 0.0
    action = pid.update(setpoint, measured_value)
    action = np.array([action])
    # action = env.action_space.sample()
    # agent与环境进行一步交互
    state, reward, done, _, info = env.step(action)
    print('state = {0}; reward = {1}'.format(state, reward))
    # 判断当前episode 是否完成
    if done:
        print('done')
        continue
    # time.sleep(1)
# 环境结束
env.close()