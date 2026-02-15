"""
Python 数据可视化示例
====================
包含 6 种常见图表类型：
1. 折线图（Line Chart）
2. 柱状图（Bar Chart）
3. 散点图（Scatter Plot）
4. 饼图（Pie Chart）
5. 热力图（Heatmap）
6. 箱线图（Box Plot）

生成的图表保存为 visualization_dashboard.png
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # 无 GUI 环境使用 Agg 后端
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from matplotlib.patches import FancyBboxPatch

# ── 全局样式设置 ──────────────────────────────────────────────
sns.set_theme(style="whitegrid", font_scale=1.05)

# 配置中文字体（使用系统已安装的文泉驿微米黑）
from matplotlib.font_manager import FontProperties, fontManager
import os

# 注册字体
font_path = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
if os.path.exists(font_path):
    fontManager.addfont(font_path)
    chinese_font = "WenQuanYi Micro Hei"
else:
    chinese_font = "sans-serif"

plt.rcParams.update({
    "font.family":      "sans-serif",
    "font.sans-serif":  [chinese_font, "DejaVu Sans", "Arial"],
    "axes.unicode_minus": False,   # 正确显示负号
    "figure.facecolor": "#f8f9fa",
    "axes.facecolor":   "#ffffff",
    "axes.edgecolor":   "#cccccc",
    "grid.color":       "#e9ecef",
    "grid.linestyle":   "--",
    "grid.alpha":       0.7,
})

# 配色板
COLORS = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2",
           "#59a14f", "#edc948", "#b07aa1", "#ff9da7"]

np.random.seed(42)

# ── 构造示例数据 ──────────────────────────────────────────────

# 1) 月度销售数据
months = ["1月", "2月", "3月", "4月", "5月", "6月",
          "7月", "8月", "9月", "10月", "11月", "12月"]
product_a = [120, 135, 148, 160, 175, 190, 210, 225, 198, 180, 165, 200]
product_b = [90,  100, 115, 125, 140, 155, 145, 160, 170, 150, 135, 155]
product_c = [60,  75,  80,  95,  105, 110, 120, 130, 125, 115, 100, 118]

# 2) 各部门季度收入
departments = ["研发", "市场", "销售", "运营", "客服"]
q1 = [320, 210, 450, 180, 120]
q2 = [350, 240, 480, 200, 135]
q3 = [310, 260, 510, 190, 140]
q4 = [380, 280, 530, 220, 150]

# 3) 散点数据 —— 广告投入 vs 销售额
ad_spend   = np.random.uniform(10, 100, 80)
sales      = ad_spend * 2.5 + np.random.normal(0, 20, 80)
categories = np.random.choice(["线上", "线下", "社交媒体"], 80)

# 4) 市场份额
market_labels = ["产品A", "产品B", "产品C", "产品D", "其他"]
market_sizes  = [35, 25, 20, 12, 8]

# 5) 热力图 —— 各指标相关性
corr_labels = ["销售额", "利润", "客流量", "广告投入", "满意度", "退货率"]
corr_data   = np.array([
    [1.00, 0.85, 0.72, 0.65, 0.45, -0.30],
    [0.85, 1.00, 0.60, 0.50, 0.55, -0.40],
    [0.72, 0.60, 1.00, 0.70, 0.35, -0.20],
    [0.65, 0.50, 0.70, 1.00, 0.25, -0.15],
    [0.45, 0.55, 0.35, 0.25, 1.00, -0.60],
    [-0.30, -0.40, -0.20, -0.15, -0.60, 1.00],
])

# 6) 箱线图数据 —— 各城市房价分布
cities = ["北京", "上海", "广州", "深圳", "杭州"]
house_prices = {
    city: np.random.normal(loc=base, scale=spread, size=200)
    for city, base, spread in zip(
        cities, [65, 60, 35, 55, 40], [15, 12, 8, 13, 10]
    )
}

# ── 创建大画布 ────────────────────────────────────────────────
fig = plt.figure(figsize=(22, 15))
fig.suptitle("数据可视化仪表板  |  Data Visualization Dashboard",
             fontsize=22, fontweight="bold", color="#2c3e50", y=0.98)

gs = gridspec.GridSpec(2, 3, hspace=0.35, wspace=0.30,
                       left=0.06, right=0.96, top=0.92, bottom=0.06)

# ────────────────────────────────────────────────────────────
# 1) 折线图 —— 月度销售趋势
# ────────────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(months, product_a, marker="o", linewidth=2.5, color=COLORS[0],
         label="产品 A", markersize=5)
ax1.plot(months, product_b, marker="s", linewidth=2.5, color=COLORS[1],
         label="产品 B", markersize=5)
ax1.plot(months, product_c, marker="^", linewidth=2.5, color=COLORS[2],
         label="产品 C", markersize=5)
ax1.fill_between(months, product_a, alpha=0.08, color=COLORS[0])
ax1.fill_between(months, product_b, alpha=0.08, color=COLORS[1])
ax1.set_title("月度销售趋势", fontsize=14, fontweight="bold", pad=12)
ax1.set_ylabel("销售额（万元）")
ax1.legend(loc="upper left", framealpha=0.9)
ax1.tick_params(axis="x", rotation=45)

# ────────────────────────────────────────────────────────────
# 2) 分组柱状图 —— 各部门季度收入
# ────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
x = np.arange(len(departments))
w = 0.20
bars1 = ax2.bar(x - 1.5*w, q1, w, label="Q1", color=COLORS[0], edgecolor="white")
bars2 = ax2.bar(x - 0.5*w, q2, w, label="Q2", color=COLORS[1], edgecolor="white")
bars3 = ax2.bar(x + 0.5*w, q3, w, label="Q3", color=COLORS[2], edgecolor="white")
bars4 = ax2.bar(x + 1.5*w, q4, w, label="Q4", color=COLORS[3], edgecolor="white")
ax2.set_xticks(x)
ax2.set_xticklabels(departments)
ax2.set_title("各部门季度收入", fontsize=14, fontweight="bold", pad=12)
ax2.set_ylabel("收入（万元）")
ax2.legend(ncol=4, loc="upper right", fontsize=9, framealpha=0.9)

# ────────────────────────────────────────────────────────────
# 3) 散点图 —— 广告投入 vs 销售额
# ────────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[0, 2])
for i, cat in enumerate(["线上", "线下", "社交媒体"]):
    mask = categories == cat
    ax3.scatter(ad_spend[mask], sales[mask], c=COLORS[i],
                label=cat, alpha=0.7, edgecolors="white", s=60)
# 趋势线
z = np.polyfit(ad_spend, sales, 1)
p = np.poly1d(z)
x_line = np.linspace(ad_spend.min(), ad_spend.max(), 100)
ax3.plot(x_line, p(x_line), "--", color="#888888", linewidth=1.5, label="趋势线")
ax3.set_title("广告投入 vs 销售额", fontsize=14, fontweight="bold", pad=12)
ax3.set_xlabel("广告投入（万元）")
ax3.set_ylabel("销售额（万元）")
ax3.legend(framealpha=0.9)

# ────────────────────────────────────────────────────────────
# 4) 饼图 —— 市场份额
# ────────────────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 0])
explode = (0.05, 0.05, 0.05, 0.05, 0.05)
wedges, texts, autotexts = ax4.pie(
    market_sizes, labels=market_labels, autopct="%1.1f%%",
    startangle=140, colors=COLORS[:5], explode=explode,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
    textprops={"fontsize": 11},
)
for at in autotexts:
    at.set_fontweight("bold")
    at.set_color("white")
ax4.set_title("市场份额分布", fontsize=14, fontweight="bold", pad=12)

# ────────────────────────────────────────────────────────────
# 5) 热力图 —— 指标相关性
# ────────────────────────────────────────────────────────────
ax5 = fig.add_subplot(gs[1, 1])
im = sns.heatmap(
    corr_data, annot=True, fmt=".2f", cmap="RdYlBu_r",
    xticklabels=corr_labels, yticklabels=corr_labels,
    vmin=-1, vmax=1, linewidths=0.5, linecolor="white",
    cbar_kws={"shrink": 0.8}, ax=ax5,
)
ax5.set_title("业务指标相关性热力图", fontsize=14, fontweight="bold", pad=12)
ax5.tick_params(axis="x", rotation=30)
ax5.tick_params(axis="y", rotation=0)

# ────────────────────────────────────────────────────────────
# 6) 箱线图 —— 城市房价分布
# ────────────────────────────────────────────────────────────
ax6 = fig.add_subplot(gs[1, 2])
bp_data = [house_prices[c] for c in cities]
bp = ax6.boxplot(
    bp_data, tick_labels=cities, patch_artist=True, notch=True,
    medianprops={"color": "white", "linewidth": 2},
    whiskerprops={"linewidth": 1.5},
    capprops={"linewidth": 1.5},
)
for patch, color in zip(bp["boxes"], COLORS[:5]):
    patch.set_facecolor(color)
    patch.set_alpha(0.85)
    patch.set_edgecolor("white")
    patch.set_linewidth(1.5)
ax6.set_title("主要城市房价分布（千元/m²）", fontsize=14, fontweight="bold", pad=12)
ax6.set_ylabel("单价（千元/m²）")

# ── 保存输出 ──────────────────────────────────────────────────
output_path = "visualization_dashboard.png"
fig.savefig(output_path, dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor(), edgecolor="none")
plt.close(fig)
print(f"可视化仪表板已保存到: {output_path}")
print(f"图片尺寸: 22x15 英寸, DPI: 150")
