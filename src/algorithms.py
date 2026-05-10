# src/algorithms.py
import heapq
from typing import List, Tuple, Optional, Callable, Set
from src.environment import SequenceCRPEnv

class Node:
    """
    A* 搜索树中的节点，记录当前状态及其搜索代价。
    """
    def __init__(self, state: List[List[int]], seq_index: int, g: int, h: float, weight: float = 1.0, parent: Optional['Node'] = None):
        """
        初始化搜索节点。
        
        Args:
            state (List[List[int]]): 当前的集装箱状态 (二维列表)。
            seq_index (int): 当前已出库的目标序列索引。
            g (int): 实际代价（从起点到当前状态发生的"翻箱"总步数）。
            h (float): 启发式代价（当前状态距离全部出库的预估步数）。
            weight (float): 启发式函数的权重（用于 Weighted A*）。
            parent (Optional['Node']): 父节点，用于寻路结束后回溯完整动作路径。
        """
        self.state = state
        self.seq_index = seq_index
        self.g = g
        self.h = h
        self.f = g + weight * h
        self.parent = parent

    def __lt__(self, other: 'Node') -> bool:
        """定义节点间的比较规则，优先队列(heapq)会根据 f 值从小到大弹出节点。"""
        return self.f < other.f

def state_to_tuple(state: List[List[int]], seq_index: int) -> Tuple[Tuple[Tuple[int, ...], ...], int]:
    """
    将可变的列表状态转换为不可变的元组状态，以便存入哈希集合 (closed_set) 中进行查重。
    """
    return (tuple(tuple(bay) for bay in state), seq_index)

def greedy_search(initial_state: List[List[int]], bays: int, max_height: int, sequence: List[int], max_iters: int = 500) -> Optional[int]:
    """
    基础贪心算法：每次遇到阻碍箱，就盲目地把它丢到当前高度最低的巷道里。
    
    Args:
        initial_state (List[List[int]]): 初始状态。
        bays (int): 巷道数量。
        max_height (int): 最大高度。
        sequence (List[int]): 目标出库序列。
        max_iters (int): 防死循环的最大迭代次数。
        
    Returns:
        Optional[int]: 成功则返回总翻箱次数，陷入死胡同或超时则返回 None。
    """
    env = SequenceCRPEnv(bays, max_height, initial_state, sequence)
    relocations, safeguard = 0, 0 
    while env.seq_index < len(sequence) and safeguard < max_iters:
        safeguard += 1
        target = env.get_current_target()
        
        # 尝试直接出库
        if any(env.retrieve_container(i) for i in range(bays)): 
            continue
            
        # 寻找目标箱所在位置
        target_bay = next((i for i, b in enumerate(env.state) if target in b), -1)
        
        # 贪心策略：找一个没满且高度最低的巷道放进去
        best_to_bay, min_h = -1, float('inf')
        for to_bay in range(bays):
            if to_bay != target_bay and len(env.state[to_bay]) < max_height:
                if len(env.state[to_bay]) < min_h:
                    min_h = len(env.state[to_bay])
                    best_to_bay = to_bay
                    
        if best_to_bay == -1: 
            return None 
            
        env.move_container(target_bay, best_to_bay)
        relocations += 1
        
    return relocations if safeguard < max_iters else None

def run_a_star(initial_state: List[List[int]], bays: int, max_height: int, sequence: List[int], heuristic_func: Callable, max_iters: int = 25000) -> int:
    """
    高度解耦的 A* 算法核心，支持动态注入任意启发式函数。
    
    Args:
        initial_state (List[List[int]]): 初始状态。
        bays (int): 巷道数量。
        max_height (int): 最大高度。
        sequence (List[int]): 目标出库序列。
        heuristic_func (Callable): 计算 h 值的回调函数。格式要求见 src.heuristics。
        max_iters (int): 防死机/超时的最大扩展节点数。
        
    Returns:
        int: 找到的最优翻箱次数（若超时则返回当前 g 值 + 惩罚值）。
    """
    weight = 1.0 
    start_h = heuristic_func(initial_state, sequence, 0, max_height)
    start_node = Node(initial_state, 0, 0, start_h, weight)
    
    open_list = [start_node]
    closed_set = {state_to_tuple(initial_state, 0)}
    iterations = 0
    
    while open_list and iterations < max_iters:
        iterations += 1
        curr = heapq.heappop(open_list)
        
        # 终止条件：所有箱子已出库完毕
        if curr.seq_index == len(sequence): 
            return curr.g
            
        target = sequence[curr.seq_index]
        retrieved = False
        
        # 动作分支 1：如果可以出库，优先出库
        for i in range(bays):
            env = SequenceCRPEnv(bays, max_height, curr.state, sequence)
            env.seq_index = curr.seq_index
            if env.retrieve_container(i):
                new_state, new_idx = env.state, env.seq_index
                if state_to_tuple(new_state, new_idx) not in closed_set:
                    closed_set.add(state_to_tuple(new_state, new_idx))
                    h = heuristic_func(new_state, sequence, new_idx, max_height)
                    # 注意：出库不属于"翻箱"，所以代价 curr.g 保持不变
                    heapq.heappush(open_list, Node(new_state, new_idx, curr.g, h, weight, curr))
                retrieved = True
                break 
                
        if retrieved: 
            continue
            
        # 动作分支 2：无法出库时，只能执行"翻箱" (Relocation)
        target_bay = next((i for i, b in enumerate(curr.state) if target in b), -1)
        if target_bay != -1:
            for to_bay in range(bays):
                if to_bay != target_bay:
                    env = SequenceCRPEnv(bays, max_height, curr.state, sequence)
                    env.seq_index = curr.seq_index
                    if env.move_container(target_bay, to_bay):
                        new_state = env.state
                        if state_to_tuple(new_state, curr.seq_index) not in closed_set:
                            closed_set.add(state_to_tuple(new_state, curr.seq_index))
                            h = heuristic_func(new_state, sequence, curr.seq_index, max_height)
                            # 注意：执行了翻箱动作，代价 curr.g + 1
                            heapq.heappush(open_list, Node(new_state, curr.seq_index, curr.g + 1, h, weight, curr))
                        
    return curr.g + 5 # 如果跑满 25000 次还没找到，给 5 个翻箱的超时惩罚