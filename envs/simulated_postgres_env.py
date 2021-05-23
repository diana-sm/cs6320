import gym
from gym import error, spaces, utils
from gym.utils import seeding
from dataclasses import dataclass
import numpy as np

from connectors.database import PGConn
from connectors.benchmark import OLTPAutomator
from parameter import create_parameters


class PostgresSimEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, baseline_throughput, logger = open('log.txt', 'a+')):
        super(PostgresSimEnv, self).__init__()

        # the connectors
        self.postgres_connector = PGConn()

        self.parameters = create_parameters(self.postgres_connector)

        # Action space: 2xN - each action represents incrementing or decrementing a parameter
        self.action_space = spaces.Discrete(2*len(self.parameters))
        
        # Observation space: observe the current parameter config
        self.observation_space = spaces.Box(
                low=np.array([param.min_val for param in self.parameters]),
                high=np.array([param.max_val for param in self.parameters]),
                dtype=np.float)

        self.episode = 0
        self.steps_taken = 0
        self.done = False

        self.baseline_throughput = baseline_throughput
        self.prev_throughput = baseline_throughput

        self.logger = logger
        
        self.updated_restart_parameter = False
        self.reset()

    def step(self, action):
        assert(not self.done)
        print(f'episode {self.episode} step {self.steps_taken}')
        print(f'action: {action}')
        self.logger.write(f'\n\t\tstep {self.steps_taken}')
        self.logger.write(f'\n\t\t\taction: {action}')
        

        # change the configuration for the chosen parameter
        index = action // 2
        inc = action % 2
        param = self.parameters[index]

        print(f'old value for {param.name}: {param.current_val}')
        self.logger.write(f'\n\t\t\told value for {param.name}: {param.current_val}')
        
        if inc:
            #param.inc()
            param.inc(update_db=False)
        else:
            #param.dec()
            param.dec(update_db=False)
        
        if param.requires_restart:
            self.updated_restart_parameter = True
            
        print(f'new value for {param.name}: {param.current_val}')
        self.logger.write(f'\n\t\t\tnew value for {param.name}: {param.current_val}')
        
        self.state = np.array([param.current_val for param in self.parameters])
        
        # simulate the throughput
        mean, sd = param.throughput_distribution[param.current_val]
        throughput = np.random.normal(mean, sd)
        
        self.reward = (throughput - self.prev_throughput)/self.baseline_throughput

        print(f'prev throughput: {self.prev_throughput}, new throughput: {throughput}')
        self.logger.write(f'\n\t\t\tprev throughput: {self.prev_throughput}, new throughput: {throughput}')
        self.logger.write(f'\n\t\t\treward: {self.reward}')

        self.prev_throughput = throughput

        # end each episode after one step
        self.steps_taken += 1
        self.done = (self.steps_taken == 1)
        print(f'done = {self.done}')
        # print(observation)

        return self.state, self.reward, self.done, {'throughput': throughput}

    def reset(self):
        self.episode += 1
        self.steps_taken = 0
        self.done = False
        self.logger.write(f'\n\tepisode {self.episode}')
        
        # reset parameter values

        for param in self.parameters:
            param.reset(update_db=False)

        self.updated_restart_parameter = False        
        self.state = np.array([param.current_val for param in self.parameters])
        self.prev_throughput = self.baseline_throughput
        return self.state

    def render(self, mode='human'):
        pass

    def close (self):
        pass
