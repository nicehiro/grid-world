import gym
import numpy as np
from grid_world.envs.MAEAgent import MAEAgent
from grid_world.envs.grid_world_env import GridMatrix
from grid_world.envs.utils import AgentType, GridType
from gym import spaces
from gym.envs.classic_control import rendering
from gym.envs.classic_control import rendering
from gym.utils import seeding


class MAGridWorldEnv(gym.Env):
    '''格子世界环境，可以模拟各种不同的格子世界
    多个 Agent 环境
    '''
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 100
    }

    def __init__(self, n_width: int = 10,
                 n_height: int = 7,
                 u_size=40,
                 default_reward: float = 0,
                 default_type=0,
                 windy=False, ):
        """Initialize environment.
        """
        self.n_width = n_width
        self.n_height = n_height
        self.u_size = u_size
        self.default_reward = default_reward
        self.default_type = default_type
        self.windy = windy
        self.action_space = spaces.Discrete(4)

        # [(1,2,1), ...] 表示坐标 (1,2) 处为 type 1 的 grid
        self.types = []
        self.agents = {}
        self.viewer = None
        self.width = self.n_width * self.u_size
        self.height = self.n_height * self.u_size

        # 维护自己的 grid matrix 保存环境的 type
        # 环境不维护格子世界的 reward
        self.grids = GridMatrix(self.n_width,
                                self.n_height,
                                self.default_type,
                                self.default_reward,
                                0.0)

    def add_agent(self, agent):
        """添加 agent 到环境中
        """
        if isinstance(agent, MAEAgent):
            self.agents[agent.name] = agent
        else:
            raise Exception('invalid agent type! Expect is MAEAgent')

    def reset(self):
        """Random initialize agents' start position and their reward
        """
        self.grids.reset()
        for x, y, t in self.types:
            self.grids.set_type(x, y, t)
        grids_count = self.n_height * self.n_width
        state_map = {}
        for _, agent in self.agents.items():
            agent.start = np.random.randint(0, grids_count)
            agent.state = self._state_to_xy(agent.start)
        self.refresh_reward_for_agents()
        for name, agent in self.agents.items():
            state_map[name] = {}
            state_map[name]['state'] = agent.state
            state_map[name]['direction'] = self.get_direction(agent)
        return state_map

    def refresh_reward_for_agents(self):
        """为其他 agent 更新各自 reward 表格中的 reward 值
        对于多个 agent 的问题，结束的标志就是 agent 的位置
        """
        for _, agent in self.agents.items():
            agent.grids.reset()
            agent.ends.clear()
            for _, other in self.agents.items():
                poi = other.state
                reward = agent.get_reward(other)
                agent.grids.set_reward(poi[0], poi[1], reward)
                # 设置结束的标志
                agent.set_ends(other)

    def _state_to_xy(self, s):
        x = s % self.n_width
        y = int((s - x) / self.n_width)
        return x, y

    def _xy_to_state(self, x, y):
        return x + self.n_width * y

    def render(self, mode='human', close=False):
        """渲染环境
        """
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        u_size = self.u_size
        m = 2
        # 如果还没有设定屏幕对象，则初始化整个屏幕具备的元素。
        if self.viewer is None:
            self.viewer = rendering.Viewer(self.width, self.height)

            # 在Viewer里绘制一个几何图像的步骤如下：
            # 1. 建立该对象需要的数据本身
            # 2. 使用rendering提供的方法返回一个geom对象
            # 3. 对geom对象进行一些对象颜色、线宽、线型、变换属性的设置（有些对象提供一些个
            #    性化的方法来设置属性，具体请参考继承自这些Geom的对象），这其中有一个重要的
            #    属性就是变换属性，
            #    该属性负责对对象在屏幕中的位置、渲染、缩放进行渲染。如果某对象
            #    在呈现时可能发生上述变化，则应建立关于该对象的变换属性。该属性是一个
            #    Transform对象，而一个Transform对象，包括translate、rotate和scale
            #    三个属性，每个属性都由以np.array对象描述的矩阵决定。
            # 4. 将新建立的geom对象添加至viewer的绘制对象列表里，如果在屏幕上只出现一次，
            #    将其加入到add_onegeom(）列表中，如果需要多次渲染，则将其加入add_geom()
            # 5. 在渲染整个viewer之前，对有需要的geom的参数进行修改，修改主要基于该对象
            #    的Transform对象
            # 6. 调用Viewer的render()方法进行绘制
            ''' 绘制水平竖直格子线，由于设置了格子之间的间隙，可不用此段代码
            for i in range(self.n_width+1):
                line = rendering.Line(start = (i*u_size, 0),
                                      end =(i*u_size, u_size*self.n_height))
                line.set_color(0.5,0,0)
                self.viewer.add_geom(line)
            for i in range(self.n_height):
                line = rendering.Line(start = (0, i*u_size),
                                      end = (u_size*self.n_width, i*u_size))
                line.set_color(0,0,1)
                self.viewer.add_geom(line)
            '''

            # 绘制格子
            for x in range(self.n_width):
                for y in range(self.n_height):
                    v = [(x * u_size + m, y * u_size + m),
                         ((x + 1) * u_size - m, y * u_size + m),
                         ((x + 1) * u_size - m, (y + 1) * u_size - m),
                         (x * u_size + m, (y + 1) * u_size - m)]

                    rect = rendering.FilledPolygon(v)
                    rect.set_color(0.0, 0.5, 0.5)
                    self.viewer.add_geom(rect)

                    if self.grids.get_type(x, y) == 1:  # 障碍格子用深灰色表示
                        rect.set_color(0.3, 0.3, 0.3)
            # 绘制个体
        for _, agent in self.agents.items():
            agent_cir = rendering.make_circle(u_size / 4, 30, True)
            agent_cir.set_color(agent.color[0], agent.color[1], agent.color[2])
            self.viewer.add_onetime(agent_cir)
            agent_trans = rendering.Transform()
            agent_cir.add_attr(agent_trans)
            # 更新个体位置
            x, y = agent.state
            agent_trans.set_translation((x + 0.5) * u_size, (y + 0.5) * u_size)

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def step(self, action, agent_name):
        """环境中某个 agent 执行一个 action 返回当前的状态以及 reward 等信息
        """
        assert self.agents.get(agent_name, None) is not None, \
            "agent not in this environment"
        agent = self.agents[agent_name]
        old_x, old_y = agent.state
        new_x, new_y = old_x, old_y

        # wind effect:
        # 有风效果，其数字表示个体离开(而不是进入)该格子时朝向别的方向会被吹偏离的格子数
        if self.windy:
            if new_x in [3, 4, 5, 8]:
                new_y += 1
            elif new_x in [6, 7]:
                new_y += 2

        if action == 0:
            new_x -= 1  # left
        elif action == 1:
            new_x += 1  # right
        elif action == 2:
            new_y += 1  # up
        elif action == 3:
            new_y -= 1  # down

        elif action == 4:
            new_x, new_y = new_x - 1, new_y - 1
        elif action == 5:
            new_x, new_y = new_x + 1, new_y - 1
        elif action == 6:
            new_x, new_y = new_x + 1, new_y - 1
        elif action == 7:
            new_x, new_y = new_x + 1, new_y + 1
        # boundary effect
        if new_x < 0: new_x = 0
        if new_x >= self.n_width: new_x = self.n_width - 1
        if new_y < 0: new_y = 0
        if new_y >= self.n_height: new_y = self.n_height - 1

        # wall effect:
        # 类型为1的格子为障碍格子，不可进入
        if self.grids.get_type(new_x, new_y) == 1:
            new_x, new_y = old_x, old_y

        agent.reward = agent.grids.get_reward(new_x, new_y)
        agent.state = (new_x, new_y)
        done = agent.is_end_state()
        # 每走一步，其他 agent 的 ends 需要清空重新设置
        # 每走一步，更新 agent 的 reward
        self.refresh_reward_for_agents()
        # 求方向
        agent.directions = self.get_direction(agent)
        info = {"x": new_x, "y": new_y, "grids": self.grids}
        return agent.state, agent.directions, agent.reward, done, info

    def get_direction(self, dir_agent: MAEAgent):
        """以字典形式返回某个 dire_agent 观察所有 agent 的方向
        """
        directions = {}
        for name, agent in self.agents.items():
            direction = dir_agent.get_direction(agent)
            directions[name] = direction
        return directions

    def seed(self, seed):
        # 产生一个随机化时需要的种子，同时返回一个np_random对象，支持后续的随机化生成操作
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None


class MultiAgentMaze8x8(MAGridWorldEnv):
    """多 Agent 迷宫环境
    8x8
    """

    def __init__(self):
        super(MultiAgentMaze8x8, self).__init__(
            n_width=8,
            n_height=8,
            u_size=60,
            default_reward=0,  # 不重要，每个 agent 保存自己的 reward map
            default_type=0,
            windy=False
        )
        self.types = [(2, 2, 1), (5, 5, 1), (2, 5, 1), (5, 2, 1)]
