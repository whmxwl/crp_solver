# main.py
import time
import random
import argparse
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
        # 【修改点】：用 rm_cost, _ 拆包，只取第一个返回值
        rm_cost, _ = run_a_star(state, bays, max_height, seq, get_manual_heuristic)
        results['Manual_A']['time'].append(time.time() - t0)
        results['Manual_A']['relocs'].append(rm_cost)

        # 3. 测经典 A*
        print(f" [Test {i+1}] 手动特征 A* 已极速完成，正在等待经典 A* ...")
        t0 = time.time()
        
        classic_wrapper = lambda s, seq_, idx, mh: get_classic_heuristic(s, seq_[idx] if idx < len(seq_) else None)
        # 【修改点】：用 rc_cost, _ 拆包，只取第一个返回值
        rc_cost, _ = run_a_star(state, bays, max_height, seq, classic_wrapper)
        
        results['Classic_A']['time'].append(time.time() - t0)
        results['Classic_A']['relocs'].append(rc_cost)
        
    return results, num_cnts

if __name__ == '__main__':
    # 1. 初始化解析器
    parser = argparse.ArgumentParser(description="Container Relocation Problem (CRP) Benchmark Solver")
    
    # 2. 添加你想让用户控制的参数
    parser.add_argument('--bays', type=int, default=5, help='集装箱巷道数量 (默认: 5)')
    parser.add_argument('--height', type=int, default=5, help='每个巷道的最大高度 (默认: 5)')
    parser.add_argument('--fill', type=float, default=0.7, help='初始场景满载率 (默认: 0.7)')
    parser.add_argument('--tests', type=int, default=8, help='测试轮数 (默认: 8)')
    
    # 3. 解析终端输入的参数
    args = parser.parse_args()
    
    # 4. 把解析出来的参数传给运行函数
    results, num_cnts = run_batch_evaluation(
        bays=args.bays, 
        max_height=args.height, 
        fill_rate=args.fill, 
        num_tests=args.tests
    )
    
    plot_evaluation_results(results, num_cnts)