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
            self.viewer = mujoco_viewer.MujocoViewer(self.model, self.data)

        self.termination = False

        # state buffer
        self.state_buffer = []
        self.buffer_size = self.config['env']['state_buffer_size']  # 3

        # Observation space and State space
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32)
        self.action_space = spaces.Box(low=np.array([-3] * 1), high=np.array([3] * 1))

        # self.action_high = np.array([0.26, 0.39, 0.9, 0.55, 0.8, 0.26, 0.39, 0.9, 0.55, 0.8], dtype=np.float32)
        # self.action_space = spaces.Box(-self.action_high, self.action_high, dtype=np.float32)

        self.P = np.array(self.config['control']['P'])
        self.D = np.array(self.config['control']['D'])

        self.simrate = self.config['control']['decimation']  # simulate X mujoco steps with same pd target. 50 brings simulation from 2000Hz to exactly 40Hz
        self.time = 0  # number of time steps in current episode

        self.time_limit = self.config['env']['time_limit']

    def step_simulation(self, action):
        self.data.ctrl[0] = action

    def get_state(self):
        state = np.concatenate([self.data.qpos, self.data.qvel]).ravel()
        return state

    def step(self, action):

        for _ in range(self.simrate):
            self.step_simulation(action)

        self.time += 1

        obs = self.get_state()

        # 保持身体高度
        if self.visual:
            self.render()
        reward = 1
        done = False
        return obs, reward, done, {}