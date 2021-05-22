import numpy as np
from datetime import datetime
from os import path

import gym
from gym.envs.registration import register
from stable_baselines3 import A2C, DQN, DDPG, PPO, SAC, TD3
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import make_vec_env

from parameter import parameters

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
    id='Postgres-v0',
    entry_point='envs.postgres_env:PostgresEnvContinuous'
)
register(
    id='Postgres-v1',
    entry_point='envs.postgres_env:PostgresEnvDiscrete'
)

# create log file
log_file = path.abspath('log.txt')
f = open(log_file, 'a+')

# create the env
env = gym.make('Postgres-v1', parameters=parameters, baseline_throughput=400, logger=f)
#env = make_vec_env('Postgres-v0', env_kwargs={'parameters': parameters})
print(type(env))
#check_env(env)

# initialize model
# model = DDPG("MlpPolicy", env, verbose=1)
# model = DQN("MlpPolicy", env, verbose=1)
model = A2C("MlpPolicy", env, verbose=1)

# learn
f.write('\nstarted training')
start = datetime.now()
model.learn(total_timesteps=5)
end = datetime.now()
print(f'training time: {end-start}')

obs = env.reset()
actions = []
states = []
all_rewards = []

f.write('\nrunning trained model')

# run the trained model
for i in range(1):
  print(f'trained model step {i}')
  action, _states = model.predict(obs)
  obs, reward, done, info = env.step(action)
  env.render()
  all_rewards.append(reward)

# print(actions)
# print(states)
# print(all_rewards)
# print(np.mean(all_rewards))

# set parameter values back to default
env.reset()
f.close()
