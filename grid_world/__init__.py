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

register(
    id='maze8x8-v0',
    entry_point='grid_world.envs:Maze8x8',
)

register(
    id='multi-agent-8x8-v0',
    entry_point='grid_world.envs:MultiAgentMaze8x8',
)
