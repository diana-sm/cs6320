from gym.envs.registration import register

register(
    id='postgres',
    entry_point='gym_DB.envs:PostgresEnv',
)