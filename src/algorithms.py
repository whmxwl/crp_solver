# src/algorithms.py
import heapq
from src.environment import SequenceCRPEnv

class Node:
    def __init__(self, state, seq_index, g, h, weight=1.0, parent=None):
        self.state = state
        self.seq_index = seq_index
        self.g = g
        self.h = h
        self.f = g + weight * h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

def state_to_tuple(state, seq_index):
    return (tuple(tuple(bay) for bay in state), seq_index)

def greedy_search(initial_state, bays, max_height, sequence, max_iters=500):
    """基础贪心算法"""
    env = SequenceCRPEnv(bays, max_height, initial_state, sequence)
    relocations, safeguard = 0, 0 
    while env.seq_index < len(sequence) and safeguard < max_iters:
        safeguard += 1
        target = env.get_current_target()
        if any(env.retrieve_container(i) for i in range(bays)): continue
            
        target_bay = next((i for i, b in enumerate(env.state) if target in b), -1)
        best_to_bay, min_h = -1, float('inf')
        for to_bay in range(bays):
            if to_bay != target_bay and len(env.state[to_bay]) < max_height:
                if len(env.state[to_bay]) < min_h:
                    min_h = len(env.state[to_bay])
                    best_to_bay = to_bay
        if best_to_bay == -1: return None 
        env.move_container(target_bay, best_to_bay)
        relocations += 1
    return relocations if safeguard < max_iters else None

def run_a_star(initial_state, bays, max_height, sequence, heuristic_func, max_iters=25000):
    """高度解耦的 A* 算法核心"""
    weight = 1.0 
    
    # 初始化传入的启发式函数
    start_h = heuristic_func(initial_state, sequence, 0, max_height)
        
    start_node = Node(initial_state, 0, 0, start_h, weight)
    open_list = [start_node]
    closed_set = {state_to_tuple(initial_state, 0)}
    
    iterations = 0
    while open_list and iterations < max_iters:
        iterations += 1
        curr = heapq.heappop(open_list)
        
        if curr.seq_index == len(sequence): return curr.g
            
        target = sequence[curr.seq_index]
        retrieved = False
        for i in range(bays):
            env = SequenceCRPEnv(bays, max_height, curr.state, sequence)
            env.seq_index = curr.seq_index
            if env.retrieve_container(i):
                new_state, new_idx = env.state, env.seq_index
                if state_to_tuple(new_state, new_idx) not in closed_set:
                    closed_set.add(state_to_tuple(new_state, new_idx))
                    h = heuristic_func(new_state, sequence, new_idx, max_height)
                    heapq.heappush(open_list, Node(new_state, new_idx, curr.g, h, weight, curr))
                retrieved = True
                break 
                
        if retrieved: continue
            
        target_bay = next((i for i, b in enumerate(curr.state) if target in b), -1)
        for to_bay in range(bays):
            if to_bay != target_bay:
                env = SequenceCRPEnv(bays, max_height, curr.state, sequence)
                env.seq_index = curr.seq_index
                if env.move_container(target_bay, to_bay):
                    new_state = env.state
                    if state_to_tuple(new_state, curr.seq_index) not in closed_set:
                        closed_set.add(state_to_tuple(new_state, curr.seq_index))
                        h = heuristic_func(new_state, sequence, curr.seq_index, max_height)
                        heapq.heappush(open_list, Node(new_state, curr.seq_index, curr.g + 1, h, weight, curr))
                        
    return curr.g + 5