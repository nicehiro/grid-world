from grid_world.envs.grid_world_env import GridMatrix
from grid_world.envs.utils import AgentType


class MAEAgent():
    """多个 agent 存在的环境中 agent 的基类
    """

    def __init__(self, start, default_reward, name, color,
                 env, default_type:AgentType, default_value=0.0):
        """初始化Agent

        Params:
        env: where agent should be
        start: start position of the agent. Should be a tuple
        default_type: what type of the agent
        default_reward: what default reward will get when agent act
        """
        self.action_space = env.action_space
        self.grids = GridMatrix(n_width=env.n_width,
                                n_height=env.n_height,
                                default_reward=default_reward,
                                default_type=env.default_type,
                                default_value=default_value)
        self.start = start
        self.agent_type = default_type
        self.default_reward = default_reward
        # 当前 agent 的信息 (x, y, d) d 表示方向
        self.state = ()
        # 结束的位置 可以有多个
        self.ends = []
        self.reward = 0.0
        # 此 agent 的标识
        self.name = name
        # 此 agent 观察所有 agent 的方向
        self.directions = {}
        # (r, g, b)
        self.color = color

    def act(self, observation, reward, done):
        """Return action based on current env's observation,
        reward, done information
        """
        pass

    def get_reward(self, agent):
        """获取 agent 对于当前 agent 的 reward

        如果两个 agent 类型相同，reward = default_reward
        如果 A 是追逐者，B 是逃跑者，B 对于 A reward = 1;
        A 对于 B reward = -1
        """
        if self.agent_type == agent.agent_type:
            return self.default_reward
        elif self.agent_type == AgentType.Chaser and agent.agent_type == AgentType.Runner:
            return -2
        elif self.agent_type == AgentType.Runner and agent.agent_type == AgentType.Chaser:
            return 2

    def set_ends(self, agent):
        """为当前 agent 设置结束的位置
        """
        if self.agent_type != agent.agent_type:
            self.ends.append(agent.state)

    def is_end_state(self):
        return self.state in self.ends

    def get_direction(self, agent):
        """求 agent 在当前 agent 的方向
        """
        x, y = self.state
        a_x, a_y = agent.state
        if a_x == x and a_y == y:
            return 0
        elif a_x == x and a_y > y:
            return 1
        elif a_x > x and a_y > y:
            return 2
        elif a_x > x and a_y == y:
            return 3
        elif a_x > x and a_y < y:
            return 4
        elif a_x == x and a_y < y:
            return 5
        elif a_x < x and a_y < y:
            return 6
        elif a_x < x and a_y == y:
            return 7
        elif a_x < x and a_y > y:
            return 8
