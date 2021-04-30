import gym
from stable_baselines3 import PPO
from postgres_env import DiscreteEnv
from parameter import Parameter
# initialize parameters
N = 10
parameters = [Parameter(str(i), 0, 100, i%100, i%100+1) for i in range(N)]


env = DiscreteEnv(parameters)
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=2000)
# obs = env.reset()
# for i in range(2000):
#   print(f'step {i}')
#   action, _states = model.predict(obs)
#   obs, rewards, done, info = env.step(action)
  # env.render()