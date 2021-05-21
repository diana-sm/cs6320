import numpy as np
from datetime import datetime

import gym
from gym.envs.registration import register
from stable_baselines3 import A2C, DQN, DDPG, PPO, SAC, TD3
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import make_vec_env

from parameter import Parameter

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

# initialize parameters
random_page_cost = Parameter("random_page_cost", "", 1, 4, 4, 4, 0.5)
io_concurrency = Parameter("effective_io_concurrency", "", 1, 1000, 1, 1, 10)
parameters = [random_page_cost, io_concurrency]

# create the env with the parameters
env = gym.make('Postgres-v0', parameters=parameters, baseline_throughput=62)
#env = make_vec_env('Postgres-v0', env_kwargs={'parameters': parameters})
print(type(env))
check_env(env)

# initialize model
# model = DDPG("MlpPolicy", env, verbose=1)
# model = DQN("MlpPolicy", env, verbose=1)
model = PPO("MlpPolicy", env, verbose=1)

# learn
start = datetime.now()
model.learn(total_timesteps=5)
end = datetime.now()
print(f'training time: {end-start}')

obs = env.reset()
actions = []
states = []
all_rewards = []

# run the trained model
for i in range(5):
  print(f'trained model step {i}')
  action, _states = model.predict(obs)
  obs, rewards, done, info = env.step(action)
  env.render()

  actions.append(round(action[0],2))
  states.append(round(env.state[0],2))
  all_rewards.append(rewards)

print(actions)
print(states)
# print(all_rewards)
print(np.mean(all_rewards))
