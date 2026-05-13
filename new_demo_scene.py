import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def draw_custom_state(state, target_seq, title, filename):
    bays = len(state)
    max_height = 5
    
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')

    ax.set_xlim(-0.5, bays - 0.5)
    ax.set_ylim(0, max_height + 1)
    ax.axhline(0, color='black', linewidth=3)
    ax.set_xticks(range(bays))
    ax.set_xticklabels([f"巷道 {i+1}" for i in range(bays)], fontweight='bold')
    ax.set_yticks(range(max_height + 1))
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    remaining = set()
    for bay in state:
        remaining.update(bay)
        
    current_target = None
    for t in target_seq:
        if t in remaining:
            current_target = t
            break

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15, color='#FF6347')

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

    plt.subplots_adjust(top=0.85, bottom=0.1, left=0.1, right=0.95)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

# Case 01
state_01 = [
    [8, 1, 9, 10],
    [11, 2, 12],
    [13, 14, 3, 15],
    [4, 5, 6],
    [7, 16, 17]
]
draw_custom_state(state_01, list(range(1, 18)), "Case 01：常规乱序场景\n当前优先出库目标: [ 箱号 1 ]", "case01.png")

# Case 02
state_02 = [
    [1, 7, 15, 17],
    [2, 11, 16],
    [3, 8, 12, 14],
    [4, 9, 13],
    [5, 6, 10]
]
draw_custom_state(state_02, list(range(1, 18)), "Case 02：深度倒置场景\n当前优先出库目标: [ 箱号 1 ]", "case02.png")

# Case 03
state_03 = [
    [1, 15, 16, 17, 14],
    [2, 13, 12, 11, 10],
    [3, 9, 8, 7, 6],
    [4, 5],
    []
]
draw_custom_state(state_03, list(range(1, 18)), "Case 03：空间濒危场景\n当前优先出库目标: [ 箱号 1 ]", "case03.png")

print("Generated.")