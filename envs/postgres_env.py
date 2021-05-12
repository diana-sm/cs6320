import gym
from gym import error, spaces, utils
from gym.utils import seeding
from dataclasses import dataclass
import numpy as np

from connectors.database import PGConn
from connectors.benchmark import OLTPAutomator


class PostgresEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, parameters):
        super(PostgresEnv, self).__init__()

        # The list of parameters we configure
        self.parameters = parameters

        # the connectors
        self.postgres_connector = PGConn()
        self.oltp_connector = OLTPAutomator(suppress_logging=True)
        #self.oltp_connector.reinit_database()

        # Action space: 2xN - dimensional array where N = num parameters
        # Represents new parameter config
        self.action_space = spaces.Box(
            low=-1, 
            high=1,
            shape=(len(parameters),),
            dtype=np.float32)
        
        # Observation space: observe the current parameter config
        self.observation_space = spaces.Box(
                low=np.array([param.min_val for param in parameters]),
                high=np.array([param.max_val for param in parameters]),
                dtype=np.float32)

        self.steps_taken = 0
        

        print(self.action_space)

    def step(self, action):
        print(f'step {self.steps_taken}')
        print(f'action: {action}')
        print(f'old parameters: {[(param.name, param.current_val) for param in self.parameters]}')
        # set the new configurations for the parameters
        for i in range(len(self.parameters)):
            param = self.parameters[i]
            delta = action[i]*(param.max_val-param.min_val)
            new_val = round(param.current_val + delta)
            new_val = max(param.min_val, new_val)
            new_val = min(param.max_val, new_val)
            if new_val != param.current_val:
                param.current_val = new_val
                self.postgres_connector.param_set(param.name, param.current_val)
        
        print(f'new parameters: {[(param.name, param.current_val) for param in self.parameters]}')
        
        observation = np.array([param.current_val for param in self.parameters])
        
        # run the benchmark
        self.oltp_connector.run_data()
        reward = self.oltp_connector.get_throughput()

        print(f'throughput: {reward}')

        # for now, say we are done after taking 1000 steps
        self.steps_taken += 1
        done = (self.steps_taken == 5)
        # print(observation)

        return observation, reward, done, {}

    def reset(self):
        self.steps_taken = 0
        
        # reset parameter values
        for param in self.parameters:
            if param.current_val != param.default_val:
                param.current_val = param.default_val
                self.postgres_connector.param_set(param.name, param.current_val)
        
        observation = np.array([param.current_val for param in self.parameters])
        
        # reinitialize database
        self.oltp_connector.reinit_database()

        print(observation)
        print("-"*100)
        return observation

    def render(self, mode='human'):
        pass

    def close (self):
        pass
