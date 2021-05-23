import numpy as np
from datetime import datetime
from os import path

import gym
from gym.envs.registration import register
from stable_baselines3 import A2C, DQN, DDPG, PPO, SAC, TD3
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import make_vec_env

# register envs
register(
    id='SimpleDiscrete-v0',
    entry_point='envs.test_envs:SimpleDiscreteEnv'
) 
register(
    id='SimpleContinuous-v0',
    entry_point='envs.test_envs:SimpleContinuousEnv'
)
register(
        id='Postgres-Sim-v0',
        entry_point='envs.simulated_postgres_env:PostgresSimEnv'
)
register(
    id='Postgres-v1',
    entry_point='envs.postgres_env:PostgresEnvDiscrete'
)

# create log file
log_file = path.abspath('log.txt')
f = open(log_file, 'a+')

all_states = []
all_throughputs = []

start = datetime.now()
episode_len = 4
for i in range(1):
    # create env and model
    env = gym.make('Postgres-v1', baseline_throughput=190, episode_len=episode_len, logger=f)
    model = A2C("MlpPolicy", env, verbose=1)

    # learn
    print('started training')
    f.write('\nstarted training')
    #start = datetime.now()
    model.learn(total_timesteps=300)
    #end = datetime.now()
    #print(f'training time: {end-start}')

    f.write('\nrunning trained model')
    # run the trained model
    states = []
    throughputs = []

    # once the model is trained, run the learning 5x, use the config with the best throughput
    for j in range(5):
        obs = env.reset()
        for k in range(episode_len):
            action, _states = model.predict(obs)
            obs, reward, done, info = env.step(action)
            env.render()
            #print({param.name : f'{param.default_val} -> {param.current_val}' for param in env.parameters})
        states.append({param.name : f'{param.default_val} -> {param.current_val}' for param in env.parameters})
        throughputs.append(info['throughput'])

    all_states.append(states)
    all_throughputs.append(throughputs)

print(all_states)
print(all_throughputs)

end = datetime.now()
print(f'total time = {end-start}')

# set parameter values back to default
env.reset()
f.close()
