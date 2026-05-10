# main.py
import time
import random
from src.config import Config
from src.algorithms import greedy_search, run_a_star
from src.heuristics import get_classic_heuristic, get_manual_heuristic
from src.visualization import plot_evaluation_results

def run_batch_evaluation(bays=5, max_height=5, fill_rate=0.7, num_tests=8):
    print(f"\n{'='*50}\n 开始【纯公平随机场景】压测 ({bays}x{max_height}, 满载率{fill_rate*100}%)...\n{'='*50}")
    print(f"当前手动配置权重：\n f1 (阻碍) = {Config.A_WEIGHT}\n f2 (倒置) = {Config.B_WEIGHT}\n f3 (紧缺) = {Config.C_WEIGHT}\n")

    results = {
        'Greedy': {'time': [], 'relocs': []},
        'Classic_A': {'time': [], 'relocs': []},
        'Manual_A': {'time': [], 'relocs': []}
    }
    num_cnts = int(bays * max_height * fill_rate)
    
    for i in range(num_tests):
        state = [[] for _ in range(bays)]
        cnts = list(range(1, num_cnts + 1))
        random.shuffle(cnts)
        for c in cnts:
            state[random.choice([idx for idx in range(bays) if len(state[idx]) < max_height])].append(c)
        seq = list(range(1, num_cnts + 1))
        
        # 1. 测贪心
        t0 = time.time()
        rg = greedy_search(state, bays, max_height, seq)
        results['Greedy']['time'].append(time.time() - t0)
        results['Greedy']['relocs'].append(rg if rg else 0)
            
        # 2. 测手动特征 A*
        t0 = time.time()
        rm = run_a_star(state, bays, max_height, seq, get_manual_heuristic)
        results['Manual_A']['time'].append(time.time() - t0)
        results['Manual_A']['relocs'].append(rm)

        # 3. 测经典 A*
        print(f" [Test {i+1}] 手动A*完成，等待经典A* ...")
        t0 = time.time()
        
        # 包装一下经典启发式，让它的参数格式与自定义的一致
        classic_wrapper = lambda s, seq_, idx, mh: get_classic_heuristic(s, seq_[idx] if idx < len(seq_) else None)
        rc = run_a_star(state, bays, max_height, seq, classic_wrapper)
        
        results['Classic_A']['time'].append(time.time() - t0)
        results['Classic_A']['relocs'].append(rc)
        
    return results, num_cnts

if __name__ == '__main__':
    results, num_cnts = run_batch_evaluation()
    plot_evaluation_results(results, num_cnts)