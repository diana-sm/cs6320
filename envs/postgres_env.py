import gym
from gym import error, spaces, utils
from gym.utils import seeding
from dataclasses import dataclass
import numpy as np

class DiscreteEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, parameters):
        super(DiscreteEnv, self).__init__()

        # The list of parameters we configure
        self.parameters = parameters

        # Action space: 2xN - dimensional array where N = num parameters
        # Represents new parameter config
        self.action_space = spaces.MultiDiscrete([param.max_val-param.min_val for param in parameters])
        
        # Observation space: observe the current parameter config
        self.observation_space = spaces.MultiDiscrete([param.max_val-param.min_val for param in parameters])

        self.steps_taken = 0

    def step(self, action):
        # set the new configurations for the parameters
        for i in range(len(self.parameters)):
            param = self.parameters[i]
            new_val = param.min_val + action[i]
            param.current_val = new_val
        
        observation = np.array([param.current_val - param.min_val for param in self.parameters])
        print(observation)
        
        # TODO: set new parameter values in postgres
        # TODO: run benchmark with new value, get observation
        # TODO: decide when we are done

        # for now, make the algorithm search for config where all params are set to 10
        # -> reward = distance from [10, 10, ..., 10]
        distance = np.sum(np.abs(10-observation))
        print(distance)
        max_reward = np.sum([param.max_val for param in self.parameters])
        reward = (max_reward - distance)/max_reward
        print(f'reward = {reward}')

        # for now, say we are done after taking 1000 steps
        self.steps_taken += 1
        done = (self.steps_taken == 1000)
        print(observation)

        return observation, reward, done, {}

    def reset(self):
        # reset parameter values
        for param in self.parameters:
            param.current_val = param.default_val
        
        # TODO: reset parameter values in postgres

        observation = np.array([param.current_val - param.min_val for param in self.parameters])
        print(observation)
        return observation

    def render(self, mode='human'):
        pass

    def close (self):
        pass