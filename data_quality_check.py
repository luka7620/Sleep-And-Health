"""
数据质量诊断脚本
检查可能导致反直觉结果的问题
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

print("="*60)
print("睡眠健康数据质量诊断")
print("="*60 + "\n")

# 加载数据
df = pd.read_csv('sleep_health_lifestyle_dataset.csv')
print(f"数据集大小: {len(df)} 条记录\n")

# === 问题1: 检查数据分布和异常值 ===
print("="*60)
print("1. 数据分布检查")
print("="*60 + "\n")

# 检查睡眠质量分布
print("睡眠质量分布:")
print(df['Quality of Sleep (scale: 1-10)'].value_counts().sort_index())
print(f"\n平均值: {df['Quality of Sleep (scale: 1-10)'].mean():.2f}")
print(f"标准差: {df['Quality of Sleep (scale: 1-10)'].std():.2f}")
print(f"最小值: {df['Quality of Sleep (scale: 1-10)'].min()}")
print(f"最大值: {df['Quality of Sleep (scale: 1-10)'].max()}\n")

# 检查压力水平分布
print("压力水平分布:")
print(df['Stress Level (scale: 1-10)'].value_counts().sort_index())
print(f"\n平均值: {df['Stress Level (scale: 1-10)'].mean():.2f}")
print(f"标准差: {df['Stress Level (scale: 1-10)'].std():.2f}\n")

# === 问题2: 压力与睡眠质量的相关性 ===
print("="*60)
print("2. 压力与睡眠质量关系诊断")
print("="*60 + "\n")

stress_corr = df['Stress Level (scale: 1-10)'].corr(df['Quality of Sleep (scale: 1-10)'])
print(f"直接相关系数: {stress_corr:.4f}\n")

# 分组查看
stress_sleep = df.groupby('Stress Level (scale: 1-10)')['Quality of Sleep (scale: 1-10)'].agg(['mean', 'count'])
print("按压力水平分组的平均睡眠质量:")
print(stress_sleep)
print()

# === 问题3: 运动时长的特征重要性 ===
print("="*60)
print("3. 运动时长数据检查")
print("="*60 + "\n")

print("运动时长统计:")
print(df['Physical Activity Level (minutes/day)'].describe())
print(f"\n与睡眠质量的相关性: {df['Physical Activity Level (minutes/day)'].corr(df['Quality of Sleep (scale: 1-10)']):.4f}\n")

# === 问题4: 编码后的分类变量 ===
print("="*60)
print("4. 分类变量编码检查")
print("="*60 + "\n")

# 检查性别编码
print("性别分布:")
print(df['Gender'].value_counts())
print()

# 检查BMI类别编码
print("BMI类别分布:")
print(df['BMI Category'].value_counts())
print()

# 检查睡眠障碍
df['Sleep Disorder'] = df['Sleep Disorder'].fillna('No Disorder')
print("睡眠障碍分布:")
print(df['Sleep Disorder'].value_counts())
print()

# === 问题5: 编码后相关性 ===
print("="*60)
print("5. 编码影响诊断")
print("="*60 + "\n")

df_encoded = df.copy()
categorical_columns = ['Gender', 'Occupation', 'BMI Category', 'Sleep Disorder']

print("编码映射:")
for col in categorical_columns:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df_encoded[col])
    print(f"\n{col}:")
    mapping = dict(zip(le.classes_, le.transform(le.classes_)))
    for k, v in mapping.items():
        print(f"  {k} -> {v}")

# === 问题6: 具体案例分析 ===
print("\n" + "="*60)
print("6. 反常案例分析")
print("="*60 + "\n")

print("高压力但睡眠好的案例:")
high_stress_good_sleep = df[(df['Stress Level (scale: 1-10)'] >= 9) & 
                             (df['Quality of Sleep (scale: 1-10)'] >= 8)]
print(f"数量: {len(high_stress_good_sleep)} 条")
if len(high_stress_good_sleep) > 0:
    print(high_stress_good_sleep[['Age', 'Occupation', 'Stress Level (scale: 1-10)', 
                                   'Quality of Sleep (scale: 1-10)', 'Sleep Duration (hours)',
                                   'Physical Activity Level (minutes/day)']].head(10))
print()

print("低压力但睡眠差的案例:")
low_stress_bad_sleep = df[(df['Stress Level (scale: 1-10)'] <= 3) & 
                          (df['Quality of Sleep (scale: 1-10)'] <= 4)]
print(f"数量: {len(low_stress_bad_sleep)} 条")
if len(low_stress_bad_sleep) > 0:
    print(low_stress_bad_sleep[['Age', 'Occupation', 'Stress Level (scale: 1-10)', 
                                 'Quality of Sleep (scale: 1-10)', 'Sleep Duration (hours)',
                                 'Physical Activity Level (minutes/day)']].head(10))
print()

# === 结论 ===
print("="*60)
print("诊断结论")
print("="*60 + "\n")

print("潜在问题:")
print("1. 数据集较小 (401条) - 可能导致统计不稳定")
print("2. 压力与睡眠质量相关性极低 - 可能是数据生成问题")
print("3. 存在反常案例 - 高压力却睡眠好")
print("4. 分类变量编码为序数 - 可能误导相关性分析")
print("5. 这可能是一个合成数据集，不是真实数据\n")
