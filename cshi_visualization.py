"""
综合睡眠健康指数 (CSHI) 可视化脚本
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from matplotlib import font_manager

# --- 字体配置 ---
chinese_font = None
def setup_font():
    global chinese_font
    font_paths = ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']
    font_path = None
    for path in font_paths:
        if os.path.exists(path):
            font_path = path
            break
            
    if font_path:
        chinese_font = font_manager.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = chinese_font.get_name()
        font_manager.fontManager.addfont(font_path)
        plt.rcParams['axes.unicode_minus'] = False

setup_font()
sns.set_style("whitegrid")
if chinese_font: plt.rcParams['font.family'] = chinese_font.get_name()

def create_cshi_distribution(df, save_path=None):
    """1. CSHI 分数分布直方图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df, x='CSHI_Score', hue='CSHI_Level', multiple='stack', 
                 palette={'优':'#2ecc71', '良':'#3498db', '一般':'#f1c40f', '差':'#e74c3c'},
                 binwidth=2, kde=True, ax=ax)
    
    ax.set_title('综合睡眠健康指数 (CSHI) 分布', fontsize=14, fontweight='bold')
    ax.set_xlabel('综合分数 (0-100)')
    ax.set_ylabel('人数')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"✓ 生成: {save_path}")
    return fig

def create_dimension_radar(df, save_path=None):
    """2. 综合维度雷达图 (不同CSHI等级的平均表现)"""
    # 准备数据
    levels = ['优', '良', '一般', '差']
    metrics = ['Dim_Sleep', 'Dim_Cardio', 'Dim_Lifestyle']
    titles = ['睡眠维度', '心血管维度', '生活方式维度']
    
    avg_scores = df.groupby('CSHI_Level')[metrics].mean().reindex(levels)
    
    # 绘图
    angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1] # 闭合
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    colors = ['#2ecc71', '#3498db', '#f1c40f', '#e74c3c']
    
    for idx, level in enumerate(levels):
        if level not in avg_scores.index: continue
        values = avg_scores.loc[level].tolist()
        values += values[:1]
        
        ax.plot(angles, values, linewidth=2, label=level, color=colors[idx])
        ax.fill(angles, values, alpha=0.1, color=colors[idx])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(titles, fontproperties=chinese_font, fontsize=12)
    
    # Use ax.set_title instead of plt.title for object-oriented approach consistency, 
    # though plt.title works on current axes. 
    ax.set_title('CSHI 各等级维度表现对比', fontsize=15, fontweight='bold', y=1.05)
    ax.legend(bbox_to_anchor=(1.1, 1), loc='upper left')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"✓ 生成: {save_path}")
    return fig

def create_cshi_comparison_grid(df, save_path=None):
    """3. 多维度对比图 (性别/年龄/职业)"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 1. 性别对比
    sns.boxplot(data=df, x='Gender', y='CSHI_Score', palette='Set3', ax=axes[0])
    axes[0].set_title('不同性别的 CSHI 分布', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('综合睡眠健康指数')
    
    # 2. 年龄段对比
    # 创建年龄分桶
    if 'Age_Group' not in df.columns:
        df['Age_Group'] = pd.cut(df['Age'], bins=[0, 30, 40, 50, 60, 100], 
                                labels=['30岁以下', '30-40岁', '40-50岁', '50-60岁', '60岁以上'])
    sns.boxplot(data=df, x='Age_Group', y='CSHI_Score', palette='Pastel1', ax=axes[1])
    axes[1].set_title('不同年龄段的 CSHI 分布', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('年龄段')
    axes[1].set_ylabel('')
    
    # 3. 职业对比
    # 按中位数排序
    order = df.groupby('Occupation')['CSHI_Score'].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x='Occupation', y='CSHI_Score', order=order, palette='Set2', ax=axes[2])
    axes[2].set_title('不同职业的 CSHI 分布', fontsize=12, fontweight='bold')
    axes[2].set_xlabel('职业')
    axes[2].set_ylabel('')
    axes[2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"✓ 生成: {save_path}")
    return fig

def main():
    try:
        df = pd.read_csv('comprehensive_sleep_health_index.csv')
        create_cshi_distribution(df)
        create_dimension_radar(df)
        create_cshi_comparison_grid(df)
        print("所有图表生成完成!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
