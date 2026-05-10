# src/environment.py
import copy
from typing import List, Optional

class SequenceCRPEnv:
    """
    集装箱倒箱问题 (CRP) 的物理环境模拟器。
    负责管理集装箱的状态、出库逻辑以及合法的移动操作。
    """
    
    def __init__(self, bays: int, max_height: int, initial_state: List[List[int]], target_sequence: List[int]):
        """
        初始化 CRP 环境。
        
        Args:
            bays (int): 巷道(贝位)的总数量。
            max_height (int): 每个巷道允许堆放的最大高度。
            initial_state (List[List[int]]): 初始的集装箱分布状态。
            target_sequence (List[int]): 目标出库序列。
        """
        self.bays = bays
        self.max_height = max_height
        self.state = copy.deepcopy(initial_state)
        self.sequence = target_sequence
        self.seq_index = 0

    def get_current_target(self) -> Optional[int]:
        """
        获取当前需要出库的目标集装箱编号。
        
        Returns:
            Optional[int]: 当前目标集装箱的编号。如果所有集装箱已出库，则返回 None。
        """
        return self.sequence[self.seq_index] if self.seq_index < len(self.sequence) else None

    def retrieve_container(self, bay_index: int) -> bool:
        """
        尝试从指定的巷道出库集装箱（只有当最顶层的集装箱是当前目标时才能成功）。
        
        Args:
            bay_index (int): 尝试出库的巷道索引。
            
        Returns:
            bool: 如果出库成功返回 True，否则返回 False。
        """
        target = self.get_current_target()
        if target is not None and len(self.state[bay_index]) > 0:
            if self.state[bay_index][-1] == target:
                self.state[bay_index].pop()
                self.seq_index += 1
                return True
        return False

    def move_container(self, from_bay: int, to_bay: int) -> bool:
        """
        将一个集装箱从起始巷道移动到目标巷道。
        
        Args:
            from_bay (int): 起始巷道的索引。
            to_bay (int): 目标巷道的索引。
            
        Returns:
            bool: 如果移动合法并成功执行则返回 True，如果目标巷道已满或起始巷道为空则返回 False。
        """
        if len(self.state[from_bay]) == 0 or len(self.state[to_bay]) >= self.max_height:
            return False 
        self.state[to_bay].append(self.state[from_bay].pop())
        return True