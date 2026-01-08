"""
心血管健康评分可视化脚本 (双语适配版)
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import platform
import warnings
warnings.filterwarnings('ignore')

# --- 字体配置 ---
import matplotlib.pyplot as plt
from matplotlib import font_manager
import platform
import os

# 全局字体属性
chinese_font = None

def setup_font():
    global chinese_font
    
    # Windows系统常见中文字体路径
    font_paths = [
        'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
        'C:/Windows/Fonts/simhei.ttf', # 黑体
        'C:/Windows/Fonts/simsun.ttc', # 宋体
    ]
    
    font_path = None
    for path in font_paths:
        if os.path.exists(path):
            font_path = path
            break
            
    if font_path:
        # 加载字体
        chinese_font = font_manager.FontProperties(fname=font_path)
        # 设置为全局默认字体
        plt.rcParams['font.family'] = chinese_font.get_name()
        # 这一步很关键：注册字体
        font_manager.fontManager.addfont(font_path)
        plt.rcParams['axes.unicode_minus'] = False
        print(f"✓ 已加载中文字体: {font_path}")
    else:
        print("⚠ 未找到标准中文字体文件，将尝试使用系统默认字体族")
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False

setup_font()
sns.set_style("whitegrid")
# 恢复字体设置 (因为seaborn style可能会覆盖)
if chinese_font:
   plt.rcParams['font.family'] = chinese_font.get_name()

def create_correlation_heatmap(df):
    """1. 相关性热力图"""
    lifestyle_cols = ['Daily Steps', 'Physical Activity Level (minutes/day)', 
                     'Sleep Duration (hours)', 'Quality of Sleep (scale: 1-10)', 
                     'Stress Level (scale: 1-10)']
    cardio_cols = ['Systolic', 'Diastolic', 'Heart Rate (bpm)', 'Cardio_Score']
    
    # 中文标签映射
    col_map = {
        'Daily Steps': '日常步数',
        'Physical Activity Level (minutes/day)': '活动时间',
        'Sleep Duration (hours)': '睡眠时长',
        'Quality of Sleep (scale: 1-10)': '睡眠质量',
        'Stress Level (scale: 1-10)': '压力水平',
        'Systolic': '收缩压',
        'Diastolic': '舒张压',
        'Heart Rate (bpm)': '心率',
        'Cardio_Score': '心血管分数'
    }
    
    corr_matrix = pd.DataFrame(index=[col_map.get(c, c) for c in lifestyle_cols], 
                             columns=[col_map.get(c, c) for c in cardio_cols])
    
    for i, l_col in enumerate(lifestyle_cols):
        for j, c_col in enumerate(cardio_cols):
            corr_matrix.iloc[i, j] = df[l_col].corr(df[c_col])
    
    corr_matrix = corr_matrix.astype(float)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0, vmin=-1, vmax=1)
    plt.title('相关性分析: 生活方式 vs 心血管健康', fontsize=14, fontweight='bold')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('cardio_correlation_heatmap.png', dpi=300)
    print("✓ Generated: cardio_correlation_heatmap.png")
    plt.close()

def create_score_boxplots(df):
    """2. 箱线图 (仅年龄段)"""
    plt.figure(figsize=(10, 6))
    
    # 按年龄段
    df['Age_Group'] = pd.cut(df['Age'], bins=[0, 30, 40, 50, 60, 100], 
                            labels=['30岁以下', '30-40岁', '40-50岁', '50-60岁', '60岁以上'])
    
    sns.boxplot(data=df, x='Age_Group', y='Cardio_Score', palette='Pastel1')
    plt.title('不同年龄段的健康分数分布', fontsize=14, fontweight='bold')
    plt.ylabel('心血管健康分数')
    plt.xlabel('年龄段')
    
    plt.tight_layout()
    plt.savefig('cardio_score_boxplots.png', dpi=300)
    print("✓ Generated: cardio_score_boxplots.png")
    plt.close()

def create_risk_distribution(df):
    """3. 风险等级分布图 (优化布局)"""
    risk_counts = df['Risk_Level'].value_counts()
    risk_order = ['低风险', '中低风险', '中等风险', '中高风险', '高风险']
    
    present_risks = [r for r in risk_order if r in risk_counts]
    counts = [risk_counts[r] for r in present_risks]
    
    # 颜色映射
    color_map = {
        '低风险': '#2ecc71', '中低风险': '#3498db', '中等风险': '#f1c40f', 
        '中高风险': '#e67e22', '高风险': '#e74c3c'
    }
    use_colors = [color_map[r] for r in present_risks]
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # 只在饼图上显示百分比,防止标签重叠
    wedges, texts, autotexts = ax.pie(counts, autopct='%1.1f%%', startangle=90, 
                                     colors=use_colors, pctdistance=0.85,
                                     textprops={'fontsize': 10, 'color': 'white', 'weight': 'bold'})
    
    # 中间画个圆做成甜甜圈图,更美观
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    
    ax.axis('equal')  
    
    # 添加图例在右侧
    legend_labels = [f"{r} ({risk_counts[r]}人)" for r in present_risks]
    ax.legend(wedges, legend_labels,
              title="风险等级",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
              
    plt.title('心血管健康风险等级分布', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('cardio_risk_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: cardio_risk_distribution.png")
    plt.close()

def create_scatter_analysis(df):
    """4. 散点图: 血压 vs 运动量"""
    plt.figure(figsize=(10, 8))
    
    risk_color_map = {
        '低风险': 'green', '中低风险': 'blue', '中等风险': 'gold', 
        '中高风险': 'orange', '高风险': 'red'
    }
    
    sns.scatterplot(data=df, x='Daily Steps', y='Systolic', 
                    hue='Risk_Level', palette=risk_color_map, 
                    size='Age', sizes=(20, 200), alpha=0.7)
    
    plt.title('收缩压 vs 日常步数 (按风险等级着色)', fontsize=14, fontweight='bold')
    plt.xlabel('日常步数 (步/天)')
    plt.ylabel('收缩压 (mmHg)')
    plt.axhline(y=120, color='r', linestyle='--', alpha=0.3, label='理想血压上限 (120)')
    plt.axvline(x=7000, color='g', linestyle='--', alpha=0.3, label='建议运动量 (7000)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='风险等级')
    
    plt.tight_layout()
    plt.savefig('cardio_scatter_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: cardio_scatter_analysis.png")
    plt.close()

def main():
    print("Loading results...")
    try:
        df = pd.read_csv('cardio_health_score_results.csv')
    except FileNotFoundError:
        print("Error: cardio_health_score_results.csv not found. Please run calculator first.")
        return

    print("Generating visualizations...")
    create_correlation_heatmap(df)
    create_score_boxplots(df)
    create_risk_distribution(df)
    create_scatter_analysis(df)
    print("All charts generated!")

if __name__ == '__main__':
    main()
