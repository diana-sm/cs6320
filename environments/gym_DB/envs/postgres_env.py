import gym
from gym import error, spaces, utils
from gym.utils import seeding
from dataclasses import dataclass
import numpy as np

class PostgresEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, parameters):
        super(PostgresEnv, self).__init__()

        # The list of parameters we configure
        self.parameters = parameters

        # Action space: 2xN - dimensional array where N = num parameters
        # Represents a change in parameter configs
        self.action_space = spaces.MultiDiscrete(
            [[param.min_val-param.max_val, param.max_val-param.min_val] for param in parameters]
            )
        
        # Observation space: average throughput in queries/second
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=1)

    def step(self, action):
        # change the parameter configurations (making sure to keep the min and max bounds)
        for param, delta in parameters, action:
            new_val = param.current_val + delta
            new_val = max(new_val, param.min_val)
            new_val = min(new_val, param.max_val)
        
        # TODO: set new parameter values in postgres
        # TODO: run benchmark with new value, get observation

        return observation, reward, done, info

    def reset(self):
        # reset parameter values
        for param in self.params:
            param.current_val = param.default_val
        
        # TODO: reset parameter values in postgres
        # TODO: run benchmark, get observations
        return observation

    def render(self, mode='human'):
        pass

    def close (self):
        pass