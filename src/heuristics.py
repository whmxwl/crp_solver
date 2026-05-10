# src/heuristics.py
from src.config import Config

def get_classic_heuristic(state, target):
    """经典弱启发：只看目标上方的阻碍数"""
    if target is None: return 0
    for bay in state:
        if target in bay: return len(bay) - 1 - bay.index(target)
    return 0

def get_manual_heuristic(state, sequence, seq_index, max_height):
    """【核心】基于手动配置参数的三维特征启发式函数"""
    target = sequence[seq_index] if seq_index < len(sequence) else None
    if target is None: return 0.0

    # 特征 1：直接阻碍数
    f1 = 0
    for bay in state:
        if target in bay:
            f1 = len(bay) - 1 - bay.index(target)
            break
            
    # 特征 2：全局优先级倒置数
    f2 = 0
    for bay in state:
        l_bay = len(bay)
        for i in range(l_bay):
            for j in range(i + 1, l_bay):
                if bay[i] < bay[j]: 
                    f2 += 1
                    
    # 特征 3：空间紧缺度
    f3 = sum(1 for bay in state if len(bay) >= max_height - 1)
    
    # 套用手动调节的公式
    h = Config.A_WEIGHT * f1 + Config.B_WEIGHT * f2 + Config.C_WEIGHT * f3
    return max(0.0, h)