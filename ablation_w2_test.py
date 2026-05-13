# ablation_test.py
import time
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from src.config import Config
from src.algorithms import run_a_star
from src.heuristics import get_manual_heuristic

def run_weight_sensitivity_analysis():
    print("🚀 开始特征权重 w2 (优先级倒置) 的敏感性与消融实验...")
    bays, max_height, fill_rate = 5, 5, 0.7
    num_cnts = int(bays * max_height * fill_rate)
    
    # 设定我们要测试的 B_WEIGHT (优先级倒置) 的不同候选值
    test_weights = [0.0, 1.0, 3.0, 6.0, 10.0]
    
    # 固定生成一个复杂的随机场景，确保控制变量
    random.seed(42) 
    state = [[] for _ in range(bays)]
    cnts = list(range(1, num_cnts + 1))
    random.shuffle(cnts)
    for c in cnts:
        state[random.choice([idx for idx in range(bays) if len(state[idx]) < max_height])].append(c)
    seq = list(range(1, num_cnts + 1))

    results_time = []
    results_cost = []

    # 保持 A 和 C 权重不变，动态修改 B 权重进行测试
    original_b = Config.B_WEIGHT
    
    for w in test_weights:
        Config.B_WEIGHT = w
        print(f"正在测试 w2 (B_WEIGHT) = {w} ...")
        
        t0 = time.time()
        g_cost, _ = run_a_star(state, bays, max_height, seq, get_manual_heuristic, max_iters=30000)
        elapsed_time = time.time() - t0
        
        results_time.append(elapsed_time)
        results_cost.append(g_cost)
        print(f"  -> 耗时: {elapsed_time:.3f}s, 翻箱数: {g_cost}")

    # ---------------- 绘图与排版优化部分 ----------------
    # 恢复原始配置
    Config.B_WEIGHT = original_b

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F8F9FA')
    ax1.set_facecolor('#F8F9FA')

    # 绘制左侧 Y 轴（计算耗时 - 红线）
    color1 = '#FF6347'
    # 加入 LaTeX 语法 $w_2$
    ax1.set_xlabel('优先级倒置特征参数 ($w_2$)', fontweight='bold')
    ax1.set_ylabel('算法求解耗时 (秒)', color=color1, fontweight='bold')
    line1 = ax1.plot(test_weights, results_time, 'o-', color=color1, linewidth=3, label='计算耗时')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # 【终极修复】：强制 Y 轴从微小的负数开始，确保 0 点数据不贴底边，并拉高天花板
    max_time = max(results_time)
    ax1.set_ylim(-0.02, max_time * 1.25 if max_time > 0 else 0.1)

    # 绘制右侧 Y 轴（翻箱次数 - 蓝线）
    ax2 = ax1.twinx()
    color2 = '#4682B4'
    ax2.set_ylabel('最终求解翻箱次数', color=color2, fontweight='bold')
    line2 = ax2.plot(test_weights, results_cost, 's--', color=color2, linewidth=2.5, label='翻箱次数')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # 【终极修复】：为右侧 Y 轴增加顶部留白空间
    ax2.set_ylim(min(results_cost) - 0.5, max(results_cost) + 1.5)

    # 合并图例
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    
    # 图例放在右上角安全区
    ax1.legend(lines, labels, loc='upper right', frameon=True, framealpha=0.9, edgecolor='#CCCCCC', borderpad=0.8)

    # 加入 LaTeX 语法 $w_2$
    plt.title('特征参数 (优先级倒置 $w_2$) 敏感性与消融分析', fontweight='bold', pad=15)
    
    # 自动调整整体布局，防止坐标轴文字或标题被窗口边缘裁切
    fig.tight_layout()
    
    plt.show()

if __name__ == '__main__':
    run_weight_sensitivity_analysis()