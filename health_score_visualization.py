"""
健康分数可视化分析 (双语版本)
生成健康分数的各类统计图表 - 使用英文标签避免字体问题
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# 设置样式
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 10


def create_score_distribution_chart(df):
    """创建健康分数分布图"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. 健康分数直方图
    ax1 = axes[0, 0]
    ax1.hist(df['Health_Score'], bins=20, color='steelblue', edgecolor='black', alpha=0.7)
    ax1.axvline(df['Health_Score'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Health_Score"].mean():.1f}')
    ax1.axvline(df['Health_Score'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df["Health_Score"].median():.1f}')
    ax1.set_xlabel('Health Score', fontsize=12)
    ax1.set_ylabel('Count', fontsize=12)
    ax1.set_title('Health Score Distribution', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. 健康等级饼图
    ax2 = axes[0, 1]
    # 将中文等级映射为英文
    level_map = {'优秀': 'Excellent', '良好': 'Good', '中等': 'Fair', '较差': 'Poor', '差': 'Bad'}
    level_counts = df['Health_Level'].map(level_map).value_counts()
    colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#95a5a6']
    level_order = ['Excellent', 'Good', 'Fair', 'Poor', 'Bad']
    level_counts = level_counts.reindex(level_order, fill_value=0)
    
    wedges, texts, autotexts = ax2.pie(level_counts.values, labels=level_counts.index, autopct='%1.1f%%',
                                         colors=colors, startangle=90, textprops={'fontsize': 11})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax2.set_title('Health Level Distribution', fontsize=14, fontweight='bold')
    
    # 3. 各职业平均健康分数
    ax3 = axes[1, 0]
    occupation_scores = df.groupby('Occupation')['Health_Score'].mean().sort_values(ascending=True)
    bars = ax3.barh(occupation_scores.index, occupation_scores.values, color='coral', edgecolor='black')
    ax3.set_xlabel('Average Health Score', fontsize=12)
    ax3.set_ylabel('Occupation', fontsize=12)
    ax3.set_title('Average Health Score by Occupation', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='x')
    
    # 在柱状图上添加数值标签
    for i, (idx, val) in enumerate(occupation_scores.items()):
        ax3.text(val + 0.5, i, f'{val:.1f}', va='center', fontsize=10)
    
    # 4. 健康分数箱线图(按职业)
    ax4 = axes[1, 1]
    occupation_order = df.groupby('Occupation')['Health_Score'].median().sort_values(ascending=False).index
    sns.boxplot(data=df, y='Occupation', x='Health_Score', order=occupation_order, palette='Set2', ax=ax4)
    ax4.set_xlabel('Health Score', fontsize=12)
    ax4.set_ylabel('Occupation', fontsize=12)
    ax4.set_title('Health Score Distribution by Occupation (Box Plot)', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('health_score_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: health_score_distribution.png")
    plt.close()


def create_component_analysis_chart(df):
    """创建各指标贡献度分析图"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    score_columns = [
        ('Score_Steps', 'Daily Steps Score'),
        ('Score_Activity', 'Activity Time Score'),
        ('Score_BMI', 'BMI Score'),
        ('Score_Stress', 'Stress Level Score'),
        ('Score_Sleep_Duration', 'Sleep Duration Score'),
        ('Score_Sleep_Quality', 'Sleep Quality Score')
    ]
    
    for idx, (col, title) in enumerate(score_columns):
        ax = axes[idx // 3, idx % 3]
        
        # 按职业分组的箱线图
        occupation_order = df.groupby('Occupation')[col].median().sort_values(ascending=False).index
        sns.boxplot(data=df, y='Occupation', x=col, order=occupation_order, palette='Set3', ax=ax)
        ax.set_xlabel('Score', fontsize=11)
        ax.set_ylabel('Occupation', fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        ax.set_xlim(0, 105)
    
    plt.tight_layout()
    plt.savefig('health_score_components.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: health_score_components.png")
    plt.close()


def create_weight_heatmap(df):
    """创建职业权重热力图"""
    # 提取每个职业的平均权重
    occupations = df['Occupation'].unique()
    weight_columns = ['Weight_Steps', 'Weight_Activity', 'Weight_BMI', 
                     'Weight_Stress', 'Weight_Sleep_Duration', 'Weight_Sleep_Quality']
    
    weight_data = []
    for occupation in occupations:
        occupation_df = df[df['Occupation'] == occupation]
        weights = occupation_df[weight_columns].mean().values
        weight_data.append(weights)
    
    weight_matrix = np.array(weight_data)
    
    # 创建热力图
    fig, ax = plt.subplots(figsize=(12, 6))
    
    labels = ['Steps', 'Activity', 'BMI', 'Stress', 'Sleep Duration', 'Sleep Quality']
    
    im = ax.imshow(weight_matrix, cmap='YlOrRd', aspect='auto')
    
    # 设置刻度
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(occupations)))
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_yticklabels(occupations, fontsize=11)
    
    # 旋转x轴标签
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # 添加数值标签
    for i in range(len(occupations)):
        for j in range(len(labels)):
            text = ax.text(j, i, f'{weight_matrix[i, j]:.3f}',
                          ha="center", va="center", color="black", fontsize=10)
    
    ax.set_title('Health Score Weights by Occupation', fontsize=14, fontweight='bold', pad=20)
    
    # 添加颜色条
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Weight Value', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('health_score_weights_heatmap.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: health_score_weights_heatmap.png")
    plt.close()


def create_correlation_with_score(df):
    """创建原始指标与健康分数的相关性分析"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 选择原始指标
    features = [
        'Daily Steps',
        'Physical Activity Level (minutes/day)',
        'Stress Level (scale: 1-10)',
        'Sleep Duration (hours)',
        'Quality of Sleep (scale: 1-10)'
    ]
    
    feature_labels = [
        'Daily Steps',
        'Activity Time',
        'Stress Level',
        'Sleep Duration',
        'Sleep Quality'
    ]
    
    # 计算相关系数
    correlations = []
    for feature in features:
        corr = df[feature].corr(df['Health_Score'])
        correlations.append(corr)
    
    # 创建柱状图
    colors = ['green' if c > 0 else 'red' for c in correlations]
    bars = ax.barh(feature_labels, correlations, color=colors, edgecolor='black', alpha=0.7)
    
    ax.set_xlabel('Correlation with Health Score', fontsize=12)
    ax.set_title('Correlation Analysis: Features vs Health Score', fontsize=14, fontweight='bold')
    ax.axvline(0, color='black', linewidth=0.8)
    ax.grid(True, alpha=0.3, axis='x')
    
    # 添加数值标签
    for i, (label, val) in enumerate(zip(feature_labels, correlations)):
        x_pos = val + 0.02 if val > 0 else val - 0.02
        ha = 'left' if val > 0 else 'right'
        ax.text(x_pos, i, f'{val:.3f}', va='center', ha=ha, fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('health_score_correlation.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: health_score_correlation.png")
    plt.close()


def main():
    """主函数"""
    print("=" * 80)
    print("Health Score Visualization (Bilingual Version)")
    print("=" * 80)
    
    # 读取带分数的数据
    print("\n[1] Loading data...")
    df = pd.read_csv('sleep_health_lifestyle_dataset_with_scores.csv')
    print(f"✓ Data loaded: {len(df)} records")
    
    # 生成各类图表
    print("\n[2] Generating charts...")
    
    create_score_distribution_chart(df)
    create_component_analysis_chart(df)
    create_weight_heatmap(df)
    create_correlation_with_score(df)
    
    print("\n" + "=" * 80)
    print("Visualization Complete!")
    print("=" * 80)
    print("\nGenerated Charts:")
    print("  1. health_score_distribution.png - Health Score Distribution Analysis")
    print("  2. health_score_components.png - Component Score Analysis")
    print("  3. health_score_weights_heatmap.png - Occupation Weight Heatmap")
    print("  4. health_score_correlation.png - Correlation Analysis")
    print("=" * 80)


if __name__ == '__main__':
    main()
