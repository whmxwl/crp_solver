# demo_animation.py
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

from src.algorithms import run_a_star
from src.heuristics import get_manual_heuristic

def generate_random_scenario(bays=5, max_height=5, fill_rate=0.7):
    """生成一个随机的初始状态"""
    state = [[] for _ in range(bays)]
    num_cnts = int(bays * max_height * fill_rate)
    cnts = list(range(1, num_cnts + 1))
    random.shuffle(cnts)
    for c in cnts:
        state[random.choice([idx for idx in range(bays) if len(state[idx]) < max_height])].append(c)
    seq = list(range(1, num_cnts + 1))
    return state, seq, max_height

def draw_state(ax, state, target_seq, max_height):
    """在画布上绘制当前帧的集装箱状态"""
    ax.clear()
    bays = len(state)
    
    # 画背景网格线和地平线
    ax.set_xlim(-0.5, bays - 0.5)
    ax.set_ylim(0, max_height + 1)
    ax.axhline(0, color='black', linewidth=3)
    ax.set_xticks(range(bays))
    ax.set_xticklabels([f"巷道 {i+1}" for i in range(bays)], fontweight='bold')
    ax.set_yticks(range(max_height + 1))
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    # 【修复点】：动态找出场地上的真实目标
    # 1. 扫描当前场地，记录所有还没出库的箱子
    remaining_containers = set()
    for bay in state:
        remaining_containers.update(bay)
        
    # 2. 按出库顺序找，第一个还在场地上的就是当前急需出库的 VIP 目标
    current_target = None
    for t in target_seq:
        if t in remaining_containers:
            current_target = t
            break

    if current_target:
        # 标题颜色也改成了红色，视觉效果更好
        ax.set_title(f"A* 算法智能倒箱演示 | 当前优先目标: [ 箱号 {current_target} ]", 
                     fontsize=14, fontweight='bold', pad=20, color='#FF6347')
    else:
        ax.set_title("所有集装箱已成功出库！", fontsize=16, fontweight='bold', color='green') 

    # 逐个画出集装箱 (使用矩形 Patch)
    box_width = 0.8
    box_height = 0.9
    for bay_idx, bay in enumerate(state):
        for level, container_id in enumerate(bay):
            # 如果是当前目标箱，给它高亮红色
            color = '#FF6347' if container_id == current_target else '#4682B4'
            
            rect = patches.Rectangle(
                (bay_idx - box_width/2, level),  # 左下角坐标
                box_width, box_height,           # 宽, 高
                linewidth=2, edgecolor='black', facecolor=color, alpha=0.9
            )
            ax.add_patch(rect)
            # 在箱子中间写上编号
            ax.text(bay_idx, level + box_height/2, str(container_id), 
                    ha='center', va='center', color='white', fontweight='bold', fontsize=12)
def play():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    print("🎲 正在生成随机场景...")
    state, seq, max_height = generate_random_scenario(bays=5, max_height=5, fill_rate=0.7)
    
    print("🧠 A* 算法正在疯狂思考中...")
    # 运行算法，拿回完整的操作路径
    g_cost, path = run_a_star(state, len(state), max_height, seq, get_manual_heuristic)
    
    if not path:
        print("❌ 哎呀，算法没找到解（超时了）。再运行一次试试吧！")
        return

    print(f"✅ 思考完毕！总共发生了 {g_cost} 次翻箱。准备播放动画...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')

    # 动画更新函数
    def update(frame):
        # 深拷贝一份序列，避免画图时改乱了原数据
        draw_state(ax, path[frame], list(seq), max_height)

    # 核心：使用 FuncAnimation 驱动动画
    # frames=len(path) 表示总帧数，interval=800 表示每帧停留 0.8 秒
    anim = FuncAnimation(fig, update, frames=len(path), interval=800, repeat=False)
    
    # 手动分配边距
    plt.subplots_adjust(top=0.85, bottom=0.1, left=0.05, right=0.95)
    plt.show()

if __name__ == '__main__':
    play()