import gym
from gym import error, spaces, utils
from gym.utils import seeding
from dataclasses import dataclass
import numpy as np

from connectors.database import PGConn
from connectors.benchmark import OLTPAutomator


class PostgresEnvDiscrete(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, parameters, baseline_throughput, logger = open('log.txt', 'a+')):
        super(PostgresEnvDiscrete, self).__init__()

        # The list of parameters we configure
        self.parameters = parameters

        # the connectors
        #self.postgres_connector = PGConn()
        self.oltp_connector = OLTPAutomator(suppress_logging=True)
        #self.oltp_connector.reinit_database()

        # Action space: 2xN - each action represents incrementing or decrementing a parameter
        self.action_space = spaces.Discrete(2*len(parameters))
        
        # Observation space: observe the current parameter config
        self.observation_space = spaces.Box(
                low=np.array([param.min_val for param in parameters]),
                high=np.array([param.max_val for param in parameters]),
                dtype=np.int)

        self.episode = 0
        self.steps_taken = 0
        self.done = False

        self.baseline_throughput = baseline_throughput
        self.prev_throughput = baseline_throughput

        self.logger = logger

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
        
        changed_value = False
        if inc:
            changed_value = param.inc()
        else:
            changed_value = param.dec()
        
        print(f'new value for {param.name}: {param.current_val}')
        self.logger.write(f'\n\t\t\tnew value for {param.name}: {param.current_val}')
        
        self.state = np.array([param.current_val for param in self.parameters])
        
        # run the benchmark, set the reward to be the change in throughput
        self.oltp_connector.run_data()
        throughput = self.oltp_connector.get_throughput()
        
        print(f'prev throughput: {self.prev_throughput}, new throughput: {throughput}')
        self.logger.write(f'\n\t\t\tprev throughput: {self.prev_throughput}, new throughput: {throughput}')
        self.reward = throughput - self.prev_throughput
        self.prev_throughput = throughput

        # for now, end each episode after one step
        self.steps_taken += 1
        self.done = (self.steps_taken == 1)
        print(f'done = {self.done}')
        # print(observation)

        return self.state, self.reward, self.done, {}

    def reset(self):
        self.episode += 1
        self.steps_taken = 0
        self.done = False
        self.logger.write(f'\n\tepisode {self.episode}')
        
        # reset parameter values
        for param in self.parameters:
            param.reset()
        
        self.state = np.array([param.current_val for param in self.parameters])
        
        # self.oltp_connector.reinit_database()

        # change this later to adjust for changing throughput over time
        self.prev_throughput = self.baseline_throughput

        return self.state

    def render(self, mode='human'):
        pass

    def close (self):
        pass
