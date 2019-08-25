from gym.envs.registration import register

register(
    id='large-gridworld-v0',
    entry_point='grid_world.envs:LargeGridWorld',
)

register(
    id='simple-grid-world-v0',
    entry_point='grid_world.envs:SimpleGridWorld',
)


register(
    id='windy-grid-world-v0',
    entry_point='grid_world.envs:WindyGridWorld',
)

register(
    id='random-walk-v0',
    entry_point='grid_world.envs:RandomWalk',
)

register(
    id='cliff-walk-v0',
    entry_point='grid_world.envs:CliffWalk',
)

register(
    id='skull-and-treature-v0',
    entry_point='grid_world.envs:SkullAndTreasure',
)

register(
    id='movan-world-v0',
    entry_point='grid_world.envs:MovanWorld',
)
