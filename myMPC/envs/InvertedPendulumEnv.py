from typing import Optional, Tuple

from gym.core import ObsType
from gym.envs.mujoco.inverted_pendulum_v4 import InvertedPendulumEnv
import numpy as np
import gym
from gym import spaces
import mujoco
import mujoco_viewer
import yaml



class InvertedPendulumEnv_Ctrl(InvertedPendulumEnv):
    """
    | Num | Observation                                   | Min  | Max | Name (in corresponding XML file) | Joint | Unit                      |
    | --- | --------------------------------------------- | ---- | --- | -------------------------------- | ----- | ------------------------- |
    | 0   | position of the cart along the linear surface | -Inf | Inf | slider                           | slide | position (m)              |
    | 1   | vertical angle of the pole on the cart        | -Inf | Inf | hinge                            | hinge | angle (rad)               |
    | 2   | linear velocity of the cart                   | -Inf | Inf | slider                           | slide | velocity (m/s)            |
    | 3   | angular velocity of the pole on the cart      | -Inf | Inf | hinge                            | hinge | anglular velocity (rad/s) |
    """
    def step(self, a):
        reward = 1.0
        self.do_simulation(a, self.frame_skip)
        ob = self._get_obs()
        terminated = bool(not np.isfinite(ob).all() or (np.abs(ob[1]) > 0.5))
        if self.render_mode == "human":
            self.render()
        return ob, reward, terminated, False, {}


class InvertedPendulumEnv_Ctrl2(gym.Env):
    def __init__(self, cfg, **kwargs):
        with open(cfg, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        self.config = data
        self.model = self.config['system']['root_path'] + self.config['system']['mjcf_path']
        self.visual = self.config['system']['visual']
        self.model = mujoco.MjModel.from_xml_path(self.model)
        self.data = mujoco.MjData(self.model)
        if self.visual:
            render_resolution = self.config['system']['render_resolution']
            self.viewer = mujoco_viewer.MujocoViewer(self.model, self.data, width=render_resolution[0], height=render_resolution[1])
            self.viewer._render_every_frame = False     # 默认不加速显示

        # Observation space and State space
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32)
        self.action_space = spaces.Box(low=np.array([-3] * 1), high=np.array([3] * 1))
        self.init_pos = self.config['init_state']['pos']

        self.simrate = self.config['control']['decimation']  # simulate X mujoco steps with same pd target. 50 brings simulation from 2000Hz to exactly 40Hz
        self.time = 0  # number of time steps in current episode
        self.time_limit = self.config['env']['time_limit']

    def step_simulation(self, action):
        self.data.ctrl[0] = action

        mujoco.mj_step(self.model, self.data)

    def get_state(self):
        state = np.concatenate([self.data.qpos, self.data.qvel]).ravel()
        return state

    def step(self, action):

        for _ in range(self.simrate):
            self.step_simulation(action)

        self.time += 1

        obs = self.get_state()

        if self.visual:
            self.render()
        reward = 1
        done = False
        if np.abs(obs[1]) > 0.5 or self.time > self.time_limit:
            done = True
        return obs, reward, done, {}

    def reset(self, pos_offset):
        qpos_init = np.array(self.init_pos)
        qpos_init = qpos_init + np.array(pos_offset)
        qvel_zero = np.array([0] * self.model.nv)
        qacc_zero = np.array([0] * self.model.nv)

        self.data.qpos = qpos_init
        self.data.qvel = qvel_zero
        self.data.qacc = qacc_zero
        self.data.time = 0.0
        mujoco.mj_forward(self.model, self.data)

        self.time = 0

        return self.get_state()

    def render(self):
        return self.viewer.render()

    def close(self):
        self.viewer.close()
