# src/visualization.py
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt

def plot_evaluation_results(results, num_cnts):
    """绘制评测结果对比图"""
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    fig, axs = plt.subplots(2, 2, figsize=(16, 11))
    fig.patch.set_facecolor('#F8F9FA')
    
    labels = ['基础贪心', '经典 A*', '多维特征 A*']
    colors = ['#FA8072', '#A9A9A9', '#1E90FF'] 
    
    # 提取数据
    c_g, c_a, c_m = results['Greedy']['relocs'], results['Classic_A']['relocs'], results['Manual_A']['relocs']
    t_g, t_a, t_m = results['Greedy']['time'], results['Classic_A']['time'], results['Manual_A']['time']
    
    # 【修复点 1】：动态获取真实的测试轮数，而不是写死 8
    num_tests = len(c_g)
    x_axis = list(range(1, num_tests + 1))

    # --- 图 1：单次翻箱次数走势 ---
    axs[0, 0].plot(x_axis, c_g, 'o-', color=colors[0], linewidth=2, label=labels[0])
    axs[0, 0].plot(x_axis, c_a, 's--', color=colors[1], linewidth=2.5, label=labels[1])
    axs[0, 0].plot(x_axis, c_m, '^-', color=colors[2], linewidth=3, label=labels[2])
    axs[0, 0].set_ylabel('单次求解翻箱次数 (次)', fontweight='bold')
    axs[0, 0].set_xlabel('随机场景编号', fontweight='bold')
    axs[0, 0].set_title('【解的质量】完全公平场景下，寻找最优解的能力对比', fontweight='bold', pad=10)
    axs[0, 0].grid(True, linestyle='--', alpha=0.5)
    axs[0, 0].legend()

    # --- 图 2：单次计算耗时走势 ---
    axs[0, 1].plot(x_axis, t_g, 'o-', color=colors[0], linewidth=2, label=labels[0])
    axs[0, 1].plot(x_axis, t_a, 's--', color=colors[1], linewidth=2.5, label=labels[1])
    axs[0, 1].plot(x_axis, t_m, '^-', color=colors[2], linewidth=3, label=labels[2])
    axs[0, 1].set_ylabel('计算耗时 (秒)', fontweight='bold')
    axs[0, 1].set_xlabel('随机场景编号', fontweight='bold')
    axs[0, 1].set_title('【运算效率】同等求优条件下，计算时间对比', fontweight='bold', pad=10)
    axs[0, 1].grid(True, linestyle='--', alpha=0.5)
    axs[0, 1].legend()

    # --- 图 3：全局平均翻箱率 ---
    # 【修复点 2】：算平均值时除以 num_tests，不再除以 8
    avg_rates = [sum(c_g)/num_tests/num_cnts*100, sum(c_a)/num_tests/num_cnts*100, sum(c_m)/num_tests/num_cnts*100]
    axs[1, 0].bar(labels, avg_rates, color=colors, width=0.45)
    axs[1, 0].set_ylabel('平均翻箱率 (%)', fontweight='bold')
    axs[1, 0].set_title('【全局质量】算法平均翻箱率对比 (越低越好)', fontweight='bold', pad=10)
    axs[1, 0].grid(axis='y', linestyle='--', alpha=0.5)
    for i, v in enumerate(avg_rates):
        axs[1, 0].text(i, v + 1, f"{v:.1f}%", ha='center', va='bottom', fontweight='bold', fontsize=12)

    # --- 图 4：全局平均计算耗时 ---
    # 【修复点 3】：算平均值时除以 num_tests，不再除以 8
    avg_times = [sum(t_g)/num_tests, sum(t_a)/num_tests, sum(t_m)/num_tests]
    axs[1, 1].plot(labels, avg_times, 'o-', color=colors[2], linewidth=3, markersize=12)
    axs[1, 1].set_ylabel('平均计算耗时 (秒)', fontweight='bold')
    axs[1, 1].set_title('【全局速度】算法运算效率对比', fontweight='bold', pad=10)
    axs[1, 1].grid(True, linestyle='--', alpha=0.5)
    for i, v in enumerate(avg_times):
        offset = max(avg_times) * 0.08 if i != 1 else -max(avg_times) * 0.08
        va = 'bottom' if i != 1 else 'top'
        axs[1, 1].text(i, v + offset, f"{v:.4f} s", ha='center', va=va, fontweight='bold', fontsize=12)

    plt.tight_layout(pad=4.0)
    plt.show()