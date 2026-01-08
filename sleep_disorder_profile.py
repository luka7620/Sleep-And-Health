"""
睡眠障碍特征分析画像脚本
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
    font_paths = [
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/simhei.ttf',
        'C:/Windows/Fonts/simsun.ttc',
    ]
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
        print(f"✓ 已加载中文字体: {font_path}")
    else:
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
        plt.rcParams['axes.unicode_minus'] = False

setup_font()
sns.set_style("whitegrid")
# 恢复字体
if chinese_font:
   plt.rcParams['font.family'] = chinese_font.get_name()

def load_data():
    try:
        df = pd.read_csv('sleep_health_lifestyle_dataset_cleaned.csv')
    except:
        df = pd.read_csv('sleep_health_lifestyle_dataset.csv')
    
    # 填充缺失值为 'None'
    df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')
    
    # 解析血压
    df[['Systolic', 'Diastolic']] = df['Blood Pressure (systolic/diastolic)'].str.split('/', expand=True).astype(int)
    
    return df

def create_bmi_disorder_plot(df):
    """1. BMI分类 vs 睡眠障碍分布"""
    plt.figure(figsize=(10, 6))
    
    # 计算百分比
    cross_tab = pd.crosstab(df['Sleep Disorder'], df['BMI Category'], normalize='index') * 100
    
    ax = cross_tab.plot(kind='barh', stacked=True, colormap='Set3', figsize=(10, 6))
    plt.title('不同睡眠障碍人群的 BMI 分布特征', fontsize=14, fontweight='bold')
    plt.xlabel('百分比 (%)')
    plt.ylabel('睡眠障碍类型')
    plt.legend(title='BMI 分类', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 添加数值标签
    for c in ax.containers:
        ax.bar_label(c, fmt='%.1f%%', label_type='center')
    
    plt.tight_layout()
    plt.savefig('sleep_disorder_bmi.png', dpi=300)
    print("✓ 生成图表: sleep_disorder_bmi.png")
    plt.close()

def create_stress_disorder_plot(df):
    """2. 压力水平 vs 睡眠障碍"""
    plt.figure(figsize=(8, 6))
    
    sns.boxplot(data=df, x='Sleep Disorder', y='Stress Level (scale: 1-10)', palette='Pastel1')
    plt.title('不同睡眠障碍人群的压力水平对比', fontsize=14, fontweight='bold')
    plt.ylabel('压力水平 (1-10)')
    plt.xlabel('睡眠障碍类型')
    
    plt.tight_layout()
    plt.savefig('sleep_disorder_stress.png', dpi=300)
    print("✓ 生成图表: sleep_disorder_stress.png")
    plt.close()

def create_bp_scatter_plot(df):
    """3. 血压特征散点图"""
    plt.figure(figsize=(10, 8))
    
    sns.scatterplot(data=df, x='Systolic', y='Diastolic', hue='Sleep Disorder', 
                    style='Sleep Disorder', s=100, alpha=0.8, palette='bright')
    
    plt.title('血压分布特征 (按睡眠障碍分类)', fontsize=14, fontweight='bold')
    plt.xlabel('收缩压 (mmHg)')
    plt.ylabel('舒张压 (mmHg)')
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # 画一些参考线
    plt.axvline(x=140, color='r', linestyle='--', alpha=0.3, label='高血压警戒线(140/90)')
    plt.axhline(y=90, color='r', linestyle='--', alpha=0.3)
    
    plt.legend(title='睡眠障碍')
    plt.tight_layout()
    plt.savefig('sleep_disorder_bp.png', dpi=300)
    print("✓ 生成图表: sleep_disorder_bp.png")
    plt.close()

def print_profile_summary(df):
    """输出特征分析摘要"""
    print("\n=== 睡眠障碍人群特征分析摘要 ===")
    
    groups = df.groupby('Sleep Disorder')
    
    for name, group in groups:
        print(f"\n【{name}】 (n={len(group)})")
        print(f"  - 平均BMI分类: {group['BMI Category'].mode()[0]}")
        print(f"  - 平均压力水平: {group['Stress Level (scale: 1-10)'].mean():.1f}")
        print(f"  - 平均睡眠时长: {group['Sleep Duration (hours)'].mean():.1f} 小时")
        print(f"  - 平均血压: {group['Systolic'].mean():.0f}/{group['Diastolic'].mean():.0f} mmHg")
        print(f"  - 平均心率: {group['Heart Rate (bpm)'].mean():.0f} bpm")
        print(f"  - 平均日常步数: {group['Daily Steps'].mean():.0f} 步")

def main():
    print("正在加载数据...")
    df = load_data()
    
    print("正在生成分析图表...")
    create_bmi_disorder_plot(df)
    create_stress_disorder_plot(df)
    create_bp_scatter_plot(df)
    
    print_profile_summary(df)
    print("\n分析完成!")

if __name__ == '__main__':
    main()
