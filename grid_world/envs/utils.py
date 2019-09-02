from enum import Enum, unique


@unique
class AgentType(Enum):
    """Agent 类型枚举类
    """
    # 追逐者
    Chaser = 1
    # 逃跑者
    Runner = 2


@unique
class GridType(Enum):
    """Grid 类型枚举类
    """
    # 普通 可走
    Normal = 1
    # 砖块 不可走
    Brick = 2
    # 无底洞 游戏结束
    Hole = 3
