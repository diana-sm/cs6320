import gym
from gym import error, spaces, utils
from gym.utils import seeding
from dataclasses import dataclass
import numpy as np

class SimpleEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(SimpleEnv, self).__init__()

        # Action space: 0 or 1
        self.action_space = spaces.Discrete(2)
        
        # Observation = state
        self.observation_space = self.action_space

        # State: 0 or 1
        self.state = 0

        self.steps_taken = 0

        

    def step(self, action):
        self.steps_taken += 1
        done = (self.steps_taken == 1000)

        self.state = (self.state + action) % 2
        observation = self.state
        reward = self.state
        return observation, reward, done, {}

    def reset(self):
        self.steps_taken = 0
        self.state = 0
        return 0

    def render(self, mode='human'):
        pass

    def close (self):
        pass

class SimpleContinuousEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(SimpleContinuousEnv, self).__init__()

        N = 1

        # Size
        self.N = N

        # Action space: 2xN - dimensional array where N = num parameters
        # Represents new parameter config
        self.action_space = spaces.Box(
            low=-1, 
            high=1,
            shape=(N,),
            dtype=np.float32)
        
        # Observation space: observe the current parameter config
        self.observation_space = spaces.Box(
            low=-1, 
            high=1,
            shape=(N,),
            dtype=np.float32)

        self.steps_taken = 0
        self.state = np.repeat(0.5, N)

    def step(self, action):
        distance = 0.0
        for i in range(self.N):
            new_state = self.state[i] + action[i]
            new_state = max(new_state, -1)
            new_state = min(new_state, 1)
            self.state[i] = new_state
            distance += np.sum(new_state**2)
            # print(f'new state: {new_state}')
            # print(f'distance: {(10-new_state)**2}')
        
        # print(distance)
        observation = self.state
        reward = -distance
        # print(type(reward))
        # print(f'state: {self.state[0]}, reward: {reward}')
       
        self.steps_taken += 1
        if (self.steps_taken % 100) == 0:
            print(self.steps_taken)
        # done = (self.steps_taken == 1000)
        done = (distance < self.N * (0.05**2))
        # print(done)

        return observation, reward, done, {}

    def reset(self):
        self.steps_taken = 0
        
        self.state = np.repeat(0.5, self.N)
        observation = self.state
        return observation

    def render(self, mode='human'):
        pass

    def close (self):
        pass