import gym
from gym import error, spaces, utils
from gym.utils import seeding
from dataclasses import dataclass
import numpy as np

from connectors.database import PGConn
from connectors.benchmark import OLTPAutomator
from parameter import create_parameters


class PostgresEnvDiscrete(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, baseline_throughput, evaluate_after_each_step, episode_len=1, logger=open('log.txt', 'a+')):
        super(PostgresEnvDiscrete, self).__init__()

        # the connectors
        self.postgres_connector = PGConn()
        self.oltp_connector = OLTPAutomator(suppress_logging=True)
        self.postgres_connector.reinit_database()

        self.parameters = create_parameters(self.postgres_connector)


        # Action space: 2xN + 1
        # action for incrementing or decrementing each parameter
        # + an action for keeping the config unchanged 
        self.action_space = spaces.Discrete(2*len(self.parameters)+1)
        
        # Observation space: observe the current parameter config
        self.observation_space = spaces.Box(
                low=np.array([param.min_val for param in self.parameters]),
                high=np.array([param.max_val for param in self.parameters]),
                dtype=np.float)

        self.episode = 0
        self.steps_taken = 0
        self.done = False
        self.episode_len = episode_len
        self.evaluate_after_each_step = evaluate_after_each_step
        self.baseline_throughput = baseline_throughput
        self.prev_throughput = baseline_throughput

        self.logger = logger
        
        self.updated_restart_parameter = False
        self.reset()

    def step(self, action):
        assert(not self.done)
        self.log(f'\n\t\tstep {self.steps_taken}')
        self.log(f'\n\t\t\taction: {action}')
        

        # change the configuration for the chosen parameter
        index = action // 2
        
        # change parameter config (unless we chose the last action)
        if index < len(self.parameters):
            inc = action % 2
            param = self.parameters[index]

            self.log(f'\n\t\t\told value for {param.name}: {param.current_val}')
        
            if inc:
                param.inc()
            else:
                param.dec()
        
            if param.requires_restart:
                self.updated_restart_parameter = True
            
            self.log(f'\n\t\t\tnew value for {param.name}: {param.current_val}')
        
        else:
            self.log('\n\t\t\tno changes to parameter vals')
        
        self.state = np.array([param.current_val for param in self.parameters])
        
        self.steps_taken += 1
        self.done = (self.steps_taken == self.episode_len) 

        throughput = None

        if self.done or self.evaluate_after_each_step:
            # run the benchmark, set the reward to be the change in throughput
            self.oltp_connector.run_data()
            throughput = self.oltp_connector.get_throughput()
        
            self.reward = (throughput - self.prev_throughput)/self.baseline_throughput

            self.log(f'\n\t\t\tprev throughput: {self.prev_throughput}, new throughput: {throughput}')
            self.log(f'\n\t\t\treward: {self.reward}')

            self.prev_throughput = throughput
        else:
            self.reward = 0

        return self.state, self.reward, self.done, {'throughput': throughput}

    def reset(self):
        self.episode += 1
        self.steps_taken = 0
        self.done = False
        self.log(f'\n\tepisode {self.episode}')
        
        # reset parameter values
        self.postgres_connector.reset()
        if self.updated_restart_parameter:
            self.postgres_connector.restart()
        for param in self.parameters:
            param.reset(update_db=False)

        # periodically reinit database
        if (self.episode % 25) == 0:
            self.postgres_connector.reinit_database()

        self.updated_restart_parameter = False
        
        self.state = np.array([param.current_val for param in self.parameters])
        
        # self.oltp_connector.reinit_database()

        # change this later to adjust for changing throughput over time
        self.prev_throughput = self.baseline_throughput

        return self.state

    def render(self, mode='human'):
        pass

    def close (self):
        pass
    
    def log(self, message):
        self.logger.write(message)
        print(message)
