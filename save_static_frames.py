import os
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from src.algorithms import run_a_star
from src.heuristics import get_manual_heuristic

def draw_state(ax, state, target_seq, max_height, step, total_steps):
    """绘制当前状态并保存为静态图"""
    ax.clear()
    bays = len(state)
    
    ax.set_xlim(-0.5, bays - 0.5)
    ax.set_ylim(0, max_height + 1)
    ax.axhline(0, color='black', linewidth=3)
    ax.set_xticks(range(bays))
    ax.set_xticklabels([f"巷道 {i+1}" for i in range(bays)], fontweight='bold')
    ax.set_yticks(range(max_height + 1))
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    remaining_containers = set()
    for bay in state:
        remaining_containers.update(bay)
        
    current_target = None
    for t in target_seq:
        if t in remaining_containers:
            current_target = t
            break

    if current_target:
        ax.set_title(f"状态 $S_{{{step}}}$ | 当前优先出库目标: [ 箱号 {current_target} ]\n进度: {step}/{total_steps}", 
                     fontsize=14, fontweight='bold', pad=15, color='#FF6347')
    else:
        ax.set_title(f"状态 $S_{{{step}}}$ | 所有集装箱已成功出库！\n进度: {step}/{total_steps}", 
                     fontsize=14, fontweight='bold', pad=15, color='green') 

    box_width = 0.8
    box_height = 0.9
    for bay_idx, bay in enumerate(state):
        for level, container_id in enumerate(bay):
            color = '#FF6347' if container_id == current_target else '#4682B4'
            rect = patches.Rectangle(
                (bay_idx - box_width/2, level),
                box_width, box_height,
                linewidth=2, edgecolor='black', facecolor=color, alpha=0.9
            )
            ax.add_patch(rect)
            ax.text(bay_idx, level + box_height/2, str(container_id), 
                    ha='center', va='center', color='white', fontweight='bold', fontsize=12)

def generate_thesis_frames():
    # 论文配图建议使用小规模场景，便于读者理解
    bays = 3
    max_height = 3
    
    # 固定随机种子，确保每次运行生成的场景一模一样
    random.seed(42) 
    
    # 手动定义一个具有代表性的初始状态 (为了演示翻箱和出库)
    # 巷道1：底2，顶1 (目标1在底部，被2压住，发生倒置)
    # 巷道2：底3
    # 巷道3：空
    initial_state = [
        [1, 2],  # 注意：Python列表末尾是栈顶。底层是1，顶层是2。目标1被2压住。
        [3],
        []
    ]
    target_sequence = [1, 2, 3] # 出库顺序 1 -> 2 -> 3
    
    print("🧠 正在计算最优倒箱路径...")
    g_cost, path = run_a_star(initial_state, bays, max_height, target_sequence, get_manual_heuristic)
    
    if not path:
        print("❌ 算法未能找到解。")
        return

    # 创建保存图片的文件夹
    output_dir = "thesis_frames"
    os.makedirs(output_dir, exist_ok=True)
    
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')

    total_steps = len(path) - 1
    
    print(f"✅ 找到最优解！共需经历 {total_steps} 个状态转移，正在导出图片...")
    for step, state in enumerate(path):
        draw_state(ax, state, target_sequence, max_height, step, total_steps)
        plt.subplots_adjust(top=0.85, bottom=0.1, left=0.1, right=0.95)
        
        filepath = os.path.join(output_dir, f"state_S{step}.png")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')  # 输出高清300dpi图片
        print(f"保存成功: {filepath}")

    print(f"🎉 全部图片已导出至 '{output_dir}/' 文件夹！")

if __name__ == '__main__':
    generate_thesis_frames()