# ablation_w3_test.py
import time
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from src.config import Config
from src.algorithms import run_a_star
from src.heuristics import get_manual_heuristic

def run_w3_sensitivity_analysis():
    print("🚀 开始特征参数 w3 (空间紧缺度) 的敏感性与消融实验...")
    
    # 构造一个高满载率场景，逼近空间极限，这样w3的作用才会凸显
    bays, max_height, fill_rate = 5, 5, 0.72 
    num_cnts = int(bays * max_height * fill_rate)
    
    # 设定我们要测试的 C_WEIGHT (空间紧缺度) 的不同候选值
    test_weights = [0.0, 0.2, 0.5, 1.0, 2.0]
    
    # 固定生成一个随机场景
    random.seed(42) 
    state = [[] for _ in range(bays)]
    cnts = list(range(1, num_cnts + 1))
    random.shuffle(cnts)
    for c in cnts:
        # 倾向于把箱子堆高，制造空间紧缺的假象
        valid_bays = [idx for idx in range(bays) if len(state[idx]) < max_height]
        state[random.choice(valid_bays)].append(c)
    seq = list(range(1, num_cnts + 1))

    results_time = []
    results_cost = []

    # 保持 A(w1) 和 B(w2) 参数不变
    original_a = Config.A_WEIGHT
    original_b = Config.B_WEIGHT
    original_c = Config.C_WEIGHT
    
    Config.A_WEIGHT = 1.0
    Config.B_WEIGHT = 1.0  # 使用我们刚刚证明的最优值
    
    for w in test_weights:
        Config.C_WEIGHT = w
        print(f"正在测试 w3 (C_WEIGHT) = {w} ...")
        
        t0 = time.time()
        # 加入超时机制，防止w=0时陷入极度漫长的搜索
        g_cost, _ = run_a_star(state, bays, max_height, seq, get_manual_heuristic, max_iters=25000)
        elapsed_time = time.time() - t0
        
        results_time.append(elapsed_time)
        results_cost.append(g_cost if g_cost != float('inf') else 99) # 99代表无解或超时
        print(f"  -> 耗时: {elapsed_time:.3f}s, 翻箱数: {g_cost}")

    # 恢复原始配置
    Config.A_WEIGHT = original_a
    Config.B_WEIGHT = original_b
    Config.C_WEIGHT = original_c

    # ---------------- 绘图与排版优化部分 ----------------
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F8F9FA')
    ax1.set_facecolor('#F8F9FA')

    # 绘制左侧 Y 轴（计算耗时 - 绿线）
    color1 = '#2E8B57'  # 海洋绿
    # 【已修改】横坐标标签加入 LaTeX 语法 $w_3$
    ax1.set_xlabel('空间紧缺度特征参数 ($w_3$)', fontweight='bold')
    ax1.set_ylabel('算法求解耗时 (秒)', color=color1, fontweight='bold')
    line1 = ax1.plot(test_weights, results_time, 'o-', color=color1, linewidth=3, label='计算耗时')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # 剔除不合理的负数时间坐标，并将最大值拉高，为上方留出绝对空白
    max_time = max(results_time)
    ax1.set_ylim(-0.002, max_time * 2 if max_time > 0.01 else 0.03)

    # 绘制右侧 Y 轴（翻箱次数 - 紫线）
    ax2 = ax1.twinx()
    color2 = '#8A2BE2'  # 蓝紫色
    ax2.set_ylabel('最终求解翻箱次数', color=color2, fontweight='bold')
    line2 = ax2.plot(test_weights, results_cost, 's--', color=color2, linewidth=2.5, label='翻箱次数')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # 为右侧 Y 轴增加顶部留白空间，防止紫线顶到天花板
    ax2.set_ylim(min(results_cost) - 0.5, max(results_cost) + 1.5)

    # 合并图例
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    
    # 将图例放置在安全的“左上角 (upper left)”
    ax1.legend(lines, labels, loc='upper left', frameon=True, framealpha=0.9, edgecolor='#CCCCCC', borderpad=0.8)

    # 【已修改】标题加入 LaTeX 语法 $w_3$
    plt.title('特征参数 (空间紧缺度 $w_3$) 敏感性与消融分析', fontweight='bold', pad=15)
    
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    run_w3_sensitivity_analysis()