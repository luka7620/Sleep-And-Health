"""
睡眠健康数据分析
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import os
import warnings

warnings.filterwarnings('ignore')

# 设置图表样式
sns.set(style="whitegrid")

# 配置中文字体
import matplotlib.font_manager as fm
available_fonts = [f.name for f in fm.fontManager.ttflist]
chinese_fonts = ['Microsoft YaHei', 'SimHei', 'SimSun', 'STXihei', 'STSong', 'KaiTi', 'FangSong']

for font in chinese_fonts:
    if font in available_fonts:
        plt.rcParams['font.sans-serif'] = [font]
        print(f"使用字体: {font}\n")
        break

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (14, 10)

# 创建输出目录
OUTPUT_DIR = 'outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("="*60)
print("睡眠健康数据分析")
print("="*60 + "\n")

# 加载数据
print("加载数据...")
df = pd.read_csv('sleep_health_lifestyle_dataset.csv')
print(f"数据集: {len(df)} 条记录, {len(df.columns)} 个字段\n")

# 数据预处理
print("数据预处理...")
df = df.drop('Person ID', axis=1)
df['Sleep Disorder'] = df['Sleep Disorder'].fillna('No Disorder')

# 1. 拆分血压数据
df[['Systolic_BP', 'Diastolic_BP']] = df['Blood Pressure (systolic/diastolic)'].str.split('/', expand=True)
df['Systolic_BP'] = df['Systolic_BP'].astype(int)
df['Diastolic_BP'] = df['Diastolic_BP'].astype(int)
df = df.drop('Blood Pressure (systolic/diastolic)', axis=1)

# 2. 特征工程：年龄分段
age_bins = [20, 25, 30, 35, 40, 45, 50, 55, 60]
df['Age_Group'] = pd.cut(df['Age'], bins=age_bins, right=False).astype(str)
df['Age_Bracket'] = pd.cut(df['Age'], bins=[20, 30, 40, 50, 60], labels=['20-29岁', '30-39岁', '40-49岁', '50-59岁'], right=False).astype(str)

# 3. 特征工程：睡眠分类
def categorize_sleep(hours):
    if hours < 6: return '睡眠不足 (<6h)'
    elif hours <= 8: return '正常睡眠 (6-8h)'
    else: return '睡眠充足 (>8h)'
df['Sleep_Category'] = df['Sleep Duration (hours)'].apply(categorize_sleep)

# 4. 特征工程：运动等级
df['Activity_Group'] = pd.cut(df['Physical Activity Level (minutes/day)'], bins=[0, 30, 60, 90, 120], include_lowest=True).astype(str)
df['Activity_Level'] = pd.cut(df['Physical Activity Level (minutes/day)'], bins=[0, 40, 80, 120], labels=['低运动 (0-40)', '中运动 (40-80)', '高运动 (80+)'], include_lowest=True).astype(str)

# 5. 特征工程：BMI 数值映射 (用于气泡大小分布)
bmi_map = {'Underweight': 1, 'Normal': 2, 'Normal Weight': 2, 'Overweight': 3, 'Obese': 4}
df['BMI_numeric'] = df['BMI Category'].map(bmi_map).fillna(2).astype(int)

# 6. 数值编码 (用于相关性和特征重要性)
df_encoded = df.copy()
categorical_columns = ['Gender', 'Occupation', 'BMI Category', 'Sleep Disorder']
for col in categorical_columns:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df_encoded[col])

print("预处理完成\n")

# 生成图表
print("生成可视化图表...\n")

# 1. 相关性热力图
plt.figure(figsize=(16, 12))
correlation_matrix = df_encoded.corr(numeric_only=True)
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title('睡眠健康数据相关性矩阵', fontsize=18, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/01_correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. 运动与睡眠质量
plt.figure(figsize=(12, 8))
sns.regplot(data=df, 
            x='Physical Activity Level (minutes/day)', 
            y='Quality of Sleep (scale: 1-10)',
            scatter_kws={'alpha': 0.6, 's': 80, 'color': 'steelblue'},
            line_kws={'color': 'red', 'linewidth': 2})
plt.title('运动量与睡眠质量的关系', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('每日运动时长 (分钟)', fontsize=13)
plt.ylabel('睡眠质量 (1-10分)', fontsize=13)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/02_activity_sleep_regression.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. 职业压力分析
occupation_stress_median = df.groupby('Occupation')['Stress Level (scale: 1-10)'].median().sort_values(ascending=False)
occupation_order = occupation_stress_median.index.tolist()

plt.figure(figsize=(14, 8))
sns.boxplot(data=df, 
            x='Occupation', 
            y='Stress Level (scale: 1-10)',
            hue='Gender',
            order=occupation_order,
            palette='Set2')
plt.title('不同职业的压力水平分布（按压力中位数降序排列）', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('职业', fontsize=13)
plt.ylabel('压力水平 (1-10分)', fontsize=13)
plt.legend(title='性别', loc='upper right')
plt.xticks(rotation=15)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/03_occupation_stress_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. BMI 与睡眠障碍
bmi_order = ['Underweight', 'Normal', 'Overweight', 'Obese']

plt.figure(figsize=(12, 8))
sns.countplot(data=df, 
              x='BMI Category', 
              hue='Sleep Disorder',
              order=bmi_order,
              palette='viridis')
plt.title('BMI 类别与睡眠障碍的关系', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('BMI 类别', fontsize=13)
plt.ylabel('人数', fontsize=13)
plt.legend(title='睡眠障碍类型', loc='upper right')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/04_bmi_disorder_countplot.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. 年龄趋势分析（折线图 - 按性别分组）
age_gender_quality = df.groupby(['Age_Group', 'Gender'])['Quality of Sleep (scale: 1-10)'].mean().reset_index()

plt.figure(figsize=(14, 8))
for gender in df['Gender'].unique():
    data = age_gender_quality[age_gender_quality['Gender'] == gender]
    plt.plot(range(len(data)), data['Quality of Sleep (scale: 1-10)'], 
             marker='o', linewidth=2.5, markersize=8, label=f'{gender}', alpha=0.8)

plt.title('不同年龄段的睡眠质量变化趋势（按性别分组）', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('年龄段', fontsize=13)
plt.ylabel('平均睡眠质量 (1-10分)', fontsize=13)
age_labels = [str(interval) for interval in age_gender_quality['Age_Group'].unique()]
plt.xticks(range(len(age_labels)), age_labels, rotation=45)
plt.legend(title='性别', fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/06_age_sleep_quality_line.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. 睡眠障碍类型对比（折线图）
disorder_stats = df.groupby('Sleep Disorder').agg({
    'Sleep Duration (hours)': 'mean',
    'Quality of Sleep (scale: 1-10)': 'mean',
    'Stress Level (scale: 1-10)': 'mean'
}).reset_index()

plt.figure(figsize=(12, 8))
x_pos = range(len(disorder_stats))
plt.plot(x_pos, disorder_stats['Sleep Duration (hours)'], 
         marker='o', linewidth=2.5, markersize=10, label='睡眠时长 (小时)', color='#3498db')
plt.plot(x_pos, disorder_stats['Quality of Sleep (scale: 1-10)'], 
         marker='s', linewidth=2.5, markersize=10, label='睡眠质量 (1-10分)', color='#e74c3c')
plt.plot(x_pos, disorder_stats['Stress Level (scale: 1-10)'], 
         marker='^', linewidth=2.5, markersize=10, label='压力水平 (1-10分)', color='#f39c12')

plt.title('不同睡眠障碍类型的多指标对比', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('睡眠障碍类型', fontsize=13)
plt.ylabel('数值', fontsize=13)
plt.xticks(x_pos, disorder_stats['Sleep Disorder'], rotation=15)
plt.legend(fontsize=11, loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/07_disorder_comparison_line.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. 运动量分段分析（折线图）
activity_stats = df.groupby('Activity_Group').agg({
    'Quality of Sleep (scale: 1-10)': 'mean',
    'Heart Rate (bpm)': 'mean',
    'Stress Level (scale: 1-10)': 'mean'
}).reset_index()

plt.figure(figsize=(12, 8))
x_pos = range(len(activity_stats))
plt.plot(x_pos, activity_stats['Quality of Sleep (scale: 1-10)'], 
         marker='o', linewidth=2.5, markersize=10, label='睡眠质量', color='#2ecc71')
plt.plot(x_pos, activity_stats['Heart Rate (bpm)']/10, 
         marker='s', linewidth=2.5, markersize=10, label='心率 (÷10)', color='#e67e22')
plt.plot(x_pos, activity_stats['Stress Level (scale: 1-10)'], 
         marker='^', linewidth=2.5, markersize=10, label='压力水平', color='#9b59b6')

plt.title('不同运动量区间的健康指标变化', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('运动量区间 (分钟/天)', fontsize=13)
plt.ylabel('指标值', fontsize=13)
activity_labels = [str(interval) for interval in activity_stats['Activity_Group']]
plt.xticks(x_pos, activity_labels, rotation=15)
plt.legend(fontsize=11, loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/08_activity_segments_line.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. 职业多维度雷达图
occupation_radar = df.groupby('Occupation').agg({
    'Physical Activity Level (minutes/day)': lambda x: (x.mean() - x.min()) / (x.max() - x.min()) * 10,
    'Quality of Sleep (scale: 1-10)': 'mean',
    'Stress Level (scale: 1-10)': lambda x: 10 - x.mean(),  # 反转，越低越好
    'Sleep Duration (hours)': lambda x: (x.mean() - 4) / 5 * 10,  # 标准化到0-10
    'Heart Rate (bpm)': lambda x: (100 - x.mean()) / 30 * 10  # 反转并标准化
}).head(5)  # 只取前5个职业

categories = ['运动量', '睡眠质量', '压力适应', '睡眠时长', '心率健康']
fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(projection='polar'))

angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']

for idx, (occupation, row) in enumerate(occupation_radar.iterrows()):
    values = row.tolist()
    values += values[:1]
    ax.plot(angles, values, 'o-', linewidth=2, label=occupation, color=colors[idx])
    ax.fill(angles, values, alpha=0.15, color=colors[idx])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11)
ax.set_ylim(0, 10)
ax.set_title('职业健康指标雷达图 (数值越高越好)', fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/09_occupation_radar.png', dpi=300, bbox_inches='tight')
plt.close()

# 9. BMI与睡眠时长分布（小提琴图）
bmi_order = ['Normal', 'Overweight', 'Obese']
bmi_data = df[df['BMI Category'].isin(bmi_order)]

plt.figure(figsize=(14, 8))
sns.violinplot(data=bmi_data, 
               x='BMI Category', 
               y='Sleep Duration (hours)',
               hue='Gender',
               order=bmi_order,
               palette='muted',
               split=True,
               inner='quartile')
plt.title('不同BMI类别的睡眠时长分布（小提琴图）', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('BMI 类别', fontsize=13)
plt.ylabel('睡眠时长 (小时)', fontsize=13)
plt.legend(title='性别', loc='upper right')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/10_bmi_sleep_violin.png', dpi=300, bbox_inches='tight')
plt.close()

# 10. 睡眠障碍分布（面积图）
disorder_gender_count = df.groupby(['Sleep Disorder', 'Gender']).size().unstack(fill_value=0)

plt.figure(figsize=(12, 8))
disorder_gender_count.T.plot(kind='area', stacked=True, alpha=0.7, 
                             color=['#FF6B6B', '#4ECDC4', '#45B7D1'], 
                             ax=plt.gca())
plt.title('不同性别的睡眠障碍分布（堆叠面积图）', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('性别', fontsize=13)
plt.ylabel('人数', fontsize=13)
plt.legend(title='睡眠障碍类型', loc='upper left', fontsize=10)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/11_disorder_area.png', dpi=300, bbox_inches='tight')
plt.close()

# 11. 职业综合指标对比（水平条形图）
occupation_metrics = df.groupby('Occupation').agg({
    'Quality of Sleep (scale: 1-10)': 'mean',
    'Physical Activity Level (minutes/day)': 'mean',
    'Stress Level (scale: 1-10)': 'mean'
}).sort_values('Quality of Sleep (scale: 1-10)', ascending=True)

fig, axes = plt.subplots(1, 3, figsize=(18, 8))

# 睡眠质量
axes[0].barh(occupation_metrics.index, occupation_metrics['Quality of Sleep (scale: 1-10)'], 
             color='#3498db', alpha=0.8)
axes[0].set_xlabel('平均睡眠质量 (1-10分)', fontsize=11)
axes[0].set_title('各职业睡眠质量', fontsize=13, fontweight='bold')
axes[0].grid(True, alpha=0.3, axis='x')

# 运动量
axes[1].barh(occupation_metrics.index, occupation_metrics['Physical Activity Level (minutes/day)'], 
             color='#2ecc71', alpha=0.8)
axes[1].set_xlabel('平均运动量 (分钟/天)', fontsize=11)
axes[1].set_title('各职业运动量', fontsize=13, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='x')
axes[1].set_yticklabels([])

# 压力水平
axes[2].barh(occupation_metrics.index, occupation_metrics['Stress Level (scale: 1-10)'], 
             color='#e74c3c', alpha=0.8)
axes[2].set_xlabel('平均压力水平 (1-10分)', fontsize=11)
axes[2].set_title('各职业压力水平', fontsize=13, fontweight='bold')
axes[2].grid(True, alpha=0.3, axis='x')
axes[2].set_yticklabels([])

plt.suptitle('职业健康指标综合对比', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/12_occupation_horizontal_bars.png', dpi=300, bbox_inches='tight')
plt.close()

# 12. 心率与压力关系（散点+趋势线）
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, 
                x='Heart Rate (bpm)', 
                y='Stress Level (scale: 1-10)',
                hue='Sleep Disorder',
                size='Age',
                sizes=(50, 300),
                alpha=0.6,
                palette='Set2')

# 添加趋势线
z = np.polyfit(df['Heart Rate (bpm)'], df['Stress Level (scale: 1-10)'], 1)
p = np.poly1d(z)
plt.plot(df['Heart Rate (bpm)'].sort_values(), 
         p(df['Heart Rate (bpm)'].sort_values()), 
         "r--", linewidth=2, alpha=0.8, label='趋势线')

plt.title('心率与压力水平的关系（按睡眠障碍分类）', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('心率 (bpm)', fontsize=13)
plt.ylabel('压力水平 (1-10分)', fontsize=13)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/13_heartrate_stress_scatter.png', dpi=300, bbox_inches='tight')
plt.close()

# ========== 高级分析图表 (14-17) ==========

# 14. 职业压力锅分析：职业 × 性别 × 压力与睡眠（双图模式）
occ_stress_pivot = df.pivot_table(index='Gender', columns='Occupation', values='Stress Level (scale: 1-10)', aggfunc='mean')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# 左图：压力热力图
sns.heatmap(occ_stress_pivot, annot=True, fmt='.1f', cmap='YlOrRd', linewidths=1, ax=ax1, cbar_kws={'label': '平均压力水平'})
ax1.set_title('各职业性别压力分布热力图', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('职业', fontsize=12)
ax1.set_ylabel('性别', fontsize=12)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')

# 右图：睡眠质量趋势折线
sns.lineplot(data=df, x='Occupation', y='Quality of Sleep (scale: 1-10)', hue='Gender', marker='s', linewidth=2.5, markersize=8, ax=ax2)
ax2.set_title('各职业性别睡眠质量对比', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('职业', fontsize=12)
ax2.set_ylabel('平均睡眠质量', fontsize=12)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
ax2.grid(True, alpha=0.3)

plt.suptitle('职业压力锅分析：职业、性别对压力与睡眠的影响', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/14_occupation_gender_dual.png', dpi=300, bbox_inches='tight')
plt.close()

# 15. 健康防御战分析：运动量 × 性别 × 血压与睡眠（双图模式）
act_bp_pivot = df.pivot_table(index='Gender', columns='Activity_Level', values='Systolic_BP', aggfunc='mean')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# 左图：血压热力图 (收缩压)
sns.heatmap(act_bp_pivot, annot=True, fmt='.1f', cmap='YlGnBu_r', linewidths=1, ax=ax1, cbar_kws={'label': '平均收缩压 (mmHg)'})
ax1.set_title('运动量与性别的血压分布热力图', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('运动量等级', fontsize=12)
ax1.set_ylabel('性别', fontsize=12)

# 右图：睡眠质量提升趋势
sns.lineplot(data=df, x='Activity_Level', y='Quality of Sleep (scale: 1-10)', hue='Gender', marker='o', linewidth=2.5, markersize=10, ax=ax2)
ax2.set_title('运动对睡眠质量的提升趋势', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('运动量等级', fontsize=12)
ax2.set_ylabel('平均睡眠质量', fontsize=12)
ax2.grid(True, alpha=0.3)

plt.suptitle('健康防御战：运动对不同性别血压与睡眠的保护作用', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/15_exercise_gender_defense_dual.png', dpi=300, bbox_inches='tight')
plt.close()

# 16. 隐形杀手分析：BMI × 性别 × 心率与健康（双图模式）
bmi_heart_pivot = df[df['BMI Category'].isin(['Normal', 'Overweight', 'Obese'])].pivot_table(index='Gender', columns='BMI Category', values='Heart Rate (bpm)', aggfunc='mean')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# 左图：心率热力图
sns.heatmap(bmi_heart_pivot, annot=True, fmt='.1f', cmap='OrRd', linewidths=1, ax=ax1, cbar_kws={'label': '平均心率 (bpm)'})
ax1.set_title('BMI与性别的平均心率热力图', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('BMI 类别', fontsize=12)
ax1.set_ylabel('性别', fontsize=12)

# 右图：压力水平随BMI的变化
sns.lineplot(data=df[df['BMI Category'].isin(['Normal', 'Overweight', 'Obese'])], x='BMI Category', y='Stress Level (scale: 1-10)', hue='Gender', marker='^', linewidth=2.5, markersize=10, ax=ax2)
ax2.set_title('BMI 对不同性别压力水平的影响', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('BMI 类别', fontsize=12)
ax2.set_ylabel('平均压力水平', fontsize=12)
ax2.grid(True, alpha=0.3)

plt.suptitle('隐形杀手：BMI对不同性别心脏与压力的双重打击', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/16_bmi_heart_stress_dual.png', dpi=300, bbox_inches='tight')
plt.close()

# 17. 年龄的代价分析：年龄 × 睡眠质量 × 性别（热力图 + 折线图组合）
age_sleep_pivot = df.pivot_table(index='Gender', columns='Age_Bracket', values='Quality of Sleep (scale: 1-10)', aggfunc='mean')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

# 左图：热力图
sns.heatmap(age_sleep_pivot, annot=True, fmt='.2f', cmap='YlOrRd_r', center=df['Quality of Sleep (scale: 1-10)'].mean(), linewidths=2, cbar_kws={'label': '平均睡眠质量 (1-10分)'}, ax=ax1)
ax1.set_title('年龄的代价：性别×年龄段睡眠质量热力图', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('年龄段', fontsize=12)
ax1.set_ylabel('性别', fontsize=12)

# 右图：折线图
sns.lineplot(data=df, x='Age_Bracket', y='Quality of Sleep (scale: 1-10)', hue='Gender', marker='o', linewidth=2.5, markersize=10, ax=ax2)
ax2.set_title('睡眠质量的年龄衰退曲线', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('年龄段', fontsize=12)
ax2.set_ylabel('平均睡眠质量 (1-10分)', fontsize=12)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(5, 8) 

plt.suptitle('年龄与性别对睡眠质量的影响', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/17_age_gender_sleep_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# 18. 压力锅的代价：不同压力水平下的睡眠质量趋势（折线图 - 分性别）
plt.figure(figsize=(12, 8))
sns.lineplot(data=df, x='Stress Level (scale: 1-10)', y='Quality of Sleep (scale: 1-10)', hue='Gender', marker='p', linewidth=3, markersize=10)
plt.title('压力锅的代价：压力水平对不同性别睡眠质量的影响', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('压力水平 (1-10分)', fontsize=13)
plt.ylabel('平均睡眠质量 (1-10分)', fontsize=13)
plt.xticks(range(3, 9))  # 数据集压力通常在3-8之间
plt.legend(title='性别', fontsize=11)
plt.grid(True, alpha=0.3, linestyle='--')
plt.annotate('压力增加，睡眠质量显著下降', xy=(6, 6), xytext=(4, 5), arrowprops=dict(facecolor='black', shrink=0.05, width=1), fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/18_stress_sleep_quality_line.png', dpi=300, bbox_inches='tight')
plt.close()

# 19. 万步走的真相：每日步数 × 睡眠质量 × 典型职业（分面散点图）
typical_occupations = df['Occupation'].unique().tolist()
typical_df = df[df['Occupation'].isin(typical_occupations)]

if not typical_df.empty:
    g = sns.FacetGrid(typical_df, col="Occupation", hue="Gender", col_wrap=2, height=4, aspect=1.2, palette='Set1')
    g.map(sns.regplot, "Daily Steps", "Quality of Sleep (scale: 1-10)", scatter_kws={'alpha':0.4, 's':60}, line_kws={'linewidth':2})
    g.add_legend(title='性别')
    g.fig.suptitle('万步走的真相：步数对不同职业睡眠质量的边际贡献差异', fontsize=16, fontweight='bold', y=1.05)
    g.set_axis_labels("每日步数", "睡眠质量")
    plt.savefig(f'{OUTPUT_DIR}/19_steps_occupation_facet.png', dpi=300, bbox_inches='tight')
    plt.close()
else:
    print("  ! 图表 19 跳过: 数据为空")

# 20. 心律压力解耦：心率 × 压力水平 × 睡眠障碍状况（联合密度分布图）
plt.figure(figsize=(12, 10))
# 使用 Sleep Disorder 作为分类，以包含正常人对照组
sns.kdeplot(data=df, x='Heart Rate (bpm)', y='Stress Level (scale: 1-10)', 
            hue='Sleep Disorder', fill=True, alpha=0.42, palette='husl', levels=5)
plt.title('心律压力解耦：无睡眠障碍人群是否更具“心理韧性”？', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('心率 (bpm)', fontsize=13)
plt.ylabel('压力水平 (1-10分)', fontsize=13)
plt.grid(True, alpha=0.2, linestyle='--')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/20_heartrate_stress_kde.png', dpi=300, bbox_inches='tight')
plt.close()

# 21. 高血压警示录：收缩压 × 舒张压 × BMI × 年龄（四分位气泡矩阵）
plt.figure(figsize=(14, 10))
# 设置分类颜色和气泡大小
sns.scatterplot(data=df, x='Systolic_BP', y='Diastolic_BP', size='BMI_numeric', hue='Age_Bracket', sizes=(100, 600), alpha=0.7, palette='magma', edgecolor='gray', linewidth=1)
plt.axvline(x=140, color='red', linestyle='--', alpha=0.6, label='收缩压警戒线 (140)')
plt.axhline(y=90, color='red', linestyle='--', alpha=0.6, label='舒张压警戒线 (90)')
plt.title('高血压警示录：血压、体重与年龄的多维风险矩阵', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('收缩压 (mmHg)', fontsize=13)
plt.ylabel('舒张压 (mmHg)', fontsize=13)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='年龄段 / 气泡大小=BMI')
plt.grid(True, alpha=0.2)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/21_hypertension_risk_matrix.png', dpi=300, bbox_inches='tight')
plt.close()

# 22. 🎯 人群画像雷达图：一眼看穿三类人
# 准备雷达图数据：按睡眠障碍类型聚合并标准化
radar_cols = ['Stress Level (scale: 1-10)', 'Heart Rate (bpm)', 'Daily Steps', 'Sleep Duration (hours)', 'Quality of Sleep (scale: 1-10)']
raw_radar_data = df.groupby('Sleep Disorder')[radar_cols].mean()

# 定义各维度的合理取值范围进行归一化，避免过度拉伸
ranges = {
    'Stress Level (scale: 1-10)': (1, 9),
    'Heart Rate (bpm)': (50, 90),
    'Daily Steps': (3000, 10000),
    'Sleep Duration (hours)': (4, 9),
    'Quality of Sleep (scale: 1-10)': (1, 10)
}

radar_norm = raw_radar_data.copy()
for col, (min_v, max_v) in ranges.items():
    radar_norm[col] = (raw_radar_data[col] - min_v) / (max_v - min_v) * 10
    radar_norm[col] = radar_norm[col].clip(0, 10)

categories = ['压力水平', '心率', '每日步数', '睡眠时长', '睡眠质量']
angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
colors = {'No Disorder': '#3498db', 'Insomnia': '#e67e22', 'Sleep Apnea': '#2ecc71'}

for disorder in radar_norm.index:
    values = radar_norm.loc[disorder].tolist()
    values += values[:1]
    ax.plot(angles, values, 'o-', linewidth=2, label=disorder, color=colors.get(disorder, '#999'))
    ax.fill(angles, values, alpha=0.1, color=colors.get(disorder, '#999'))

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=12)
ax.set_title('人群画像雷达图：三类人群多维特征“指纹”对比(统一量程)', fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
ax.set_ylim(0, 10) # 统一坐标轴范围
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/22_disorder_radar_profile.png', dpi=300, bbox_inches='tight')
plt.close()

# 23. 🚻 性别差异交互图：不同性别对压力的睡眠敏感度
plt.figure(figsize=(12, 8))
sns.pointplot(data=df, x='Stress Level (scale: 1-10)', y='Quality of Sleep (scale: 1-10)', 
              hue='Gender', markers=['o', 's'], linestyles=['-', '--'], capsize=.1, palette='vlag')
plt.title('性别差异交互图：女性对压力的睡眠敏感度是否更高？', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('压力水平 (1-10分)', fontsize=13)
plt.ylabel('平均睡眠质量 (1-10分)', fontsize=13)
plt.grid(True, alpha=0.2)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/23_gender_stress_interaction.png', dpi=300, bbox_inches='tight')
plt.close()

# 24. ⏳ 全生命周期轨迹图：岁月的痕迹与中年健康危机
# 按年龄平滑处理趋势
age_trends = df.groupby('Age').agg({
    'Systolic_BP': 'mean',
    'Quality of Sleep (scale: 1-10)': 'mean'
}).rolling(window=3, center=True).mean()

fig, ax1 = plt.subplots(figsize=(14, 8))

# 绘制收缩压趋势
color1 = '#e74c3c'
ax1.set_xlabel('年龄 (岁)', fontsize=13)
ax1.set_ylabel('收缩压 (mmHg)', color=color1, fontsize=13)
ax1.plot(age_trends.index, age_trends['Systolic_BP'], color=color1, linewidth=3, label='收缩压趋势')
ax1.tick_params(axis='y', labelcolor=color1)

# 绘制睡眠质量趋势
ax2 = ax1.twinx()
color2 = '#27ae60'
ax2.set_ylabel('睡眠质量 (1-10分)', color=color2, fontsize=13)
ax2.plot(age_trends.index, age_trends['Quality of Sleep (scale: 1-10)'], color=color2, 
         linestyle='--', linewidth=3, label='睡眠质量趋势')
ax2.tick_params(axis='y', labelcolor=color2)

plt.title('全生命周期轨迹图：年龄增长对血压与睡眠质量的双重演变', fontsize=16, fontweight='bold', pad=20)
ax1.grid(True, alpha=0.3)
# 合并图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

# 标注 40-50 岁区间为“中年转折点”
plt.axvspan(40, 50, color='gray', alpha=0.1)
plt.annotate('中年健康转折点', xy=(45, 7.5), xytext=(35, 8.5),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1), fontsize=12)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/24_age_health_trajectory.png', dpi=300, bbox_inches='tight')
plt.close()

print("所有图表生成完成 (共24张)\n")

# 特征重要性分析
print("特征重要性分析...\n")

# 剔除无法用于 ML 的字符串派生列和重复列
cols_to_drop = [
    'Quality of Sleep (scale: 1-10)', 
    'Age_Group', 'Age_Bracket', 
    'Sleep_Category', 'Activity_Group', 
    'Activity_Level', 'BMI_numeric'
]
X = df_encoded.drop(columns=cols_to_drop)
y = df_encoded['Quality of Sleep (scale: 1-10)']

rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X, y)

feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("特征重要性排名:")
print(feature_importance.head(10).to_string(index=False))
print()

# 特征重要性图表
plt.figure(figsize=(12, 8))
sns.barplot(data=feature_importance.head(10), 
            x='Importance', 
            y='Feature',
            palette='rocket')
plt.title('影响睡眠质量的 Top 10 特征', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('重要性得分', fontsize=13)
plt.ylabel('特征名称', fontsize=13)
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/05_feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()

# 分析摘要
print("="*60)
print("分析结果摘要")
print("="*60 + "\n")

quality_corr = correlation_matrix['Quality of Sleep (scale: 1-10)'].drop('Quality of Sleep (scale: 1-10)').sort_values(ascending=False)
print(f"与睡眠质量相关性最高: {quality_corr.index[0]} ({quality_corr.iloc[0]:.3f})")
print(f"与睡眠质量相关性最低: {quality_corr.index[-1]} ({quality_corr.iloc[-1]:.3f})\n")

print(f"压力最大职业: {occupation_order[0]} (中位数: {occupation_stress_median.iloc[0]:.1f})")
print(f"压力最小职业: {occupation_order[-1]} (中位数: {occupation_stress_median.iloc[-1]:.1f})\n")

obese_sleep_apnea = len(df[(df['BMI Category'] == 'Obese') & (df['Sleep Disorder'] == 'Sleep Apnea')])
obese_total = len(df[df['BMI Category'] == 'Obese'])
print(f"肥胖人群睡眠呼吸暂停比例: {obese_sleep_apnea}/{obese_total} ({obese_sleep_apnea/obese_total*100:.1f}%)\n")

print(f"最重要特征: {feature_importance.iloc[0]['Feature']} ({feature_importance.iloc[0]['Importance']:.3f})")
print(f"Top 3: {', '.join(feature_importance.head(3)['Feature'].tolist())}\n")

print("数据统计:")
print(f"  平均睡眠质量: {df['Quality of Sleep (scale: 1-10)'].mean():.2f} 分")
print(f"  平均睡眠时长: {df['Sleep Duration (hours)'].mean():.2f} 小时")
print(f"  平均压力水平: {df['Stress Level (scale: 1-10)'].mean():.2f} 分")
print(f"  平均运动时长: {df['Physical Activity Level (minutes/day)'].mean():.1f} 分钟/天\n")

print("="*60)
print("分析完成，图表已保存至 outputs/ 目录")
print("="*60)
