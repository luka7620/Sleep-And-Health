import pandas as pd
import numpy as np
from datetime import datetime
import shutil

print("=" * 80)
print("睡眠健康数据集清洗程序")
print("=" * 80)
print(f"清洗时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# 1. 备份原始数据
print("\n[步骤1] 备份原始数据...")
shutil.copy('sleep_health_lifestyle_dataset.csv', 
            'sleep_health_lifestyle_dataset_backup.csv')
print("✓ 已创建备份: sleep_health_lifestyle_dataset_backup.csv")

# 2. 读取数据
print("\n[步骤2] 读取数据集...")
df = pd.read_csv('sleep_health_lifestyle_dataset.csv')
print(f"✓ 数据集总行数: {len(df)}")

# 3. 初始化质量标记列
print("\n[步骤3] 初始化数据质量标记...")
df['Data_Quality_Flag'] = 'Normal'
df['Anomaly_Type'] = ''

# 4. 检测并标注异常
print("\n[步骤4] 检测并标注异常数据...")

# 异常类型计数器
anomaly_count = {
    'AGE_OCCUPATION_1.2': 0,
    'AGE_OCCUPATION_1.3': 0,
    'STRESS_SLEEP_6.1': 0,
    'STRESS_SLEEP_6.2': 0,
    'STEPS_ACTIVITY_9.1': 0
}

# 条件1.2：年龄<30 且 职业=Retired
condition_1_2 = (df['Age'] < 30) & (df['Occupation'] == 'Retired')
df.loc[condition_1_2, 'Data_Quality_Flag'] = 'Anomaly'
df.loc[condition_1_2, 'Anomaly_Type'] = 'AGE_OCCUPATION_1.2'
anomaly_count['AGE_OCCUPATION_1.2'] = condition_1_2.sum()
print(f"  - 类型1.2 (年龄<30但已退休): {condition_1_2.sum()}条")

# 条件1.3：年龄>=70 且 职业=Student
condition_1_3 = (df['Age'] >= 70) & (df['Occupation'] == 'Student')
df.loc[condition_1_3, 'Data_Quality_Flag'] = 'Anomaly'
df.loc[condition_1_3, 'Anomaly_Type'] = 'AGE_OCCUPATION_1.3'
anomaly_count['AGE_OCCUPATION_1.3'] = condition_1_3.sum()
print(f"  - 类型1.3 (年龄>=70仍是学生): {condition_1_3.sum()}条")

# 条件6.1：压力>=9 且 睡眠质量>=8（且尚未被标记）
condition_6_1 = (df['Stress Level (scale: 1-10)'] >= 9) & \
                (df['Quality of Sleep (scale: 1-10)'] >= 8) & \
                (df['Data_Quality_Flag'] == 'Normal')
df.loc[condition_6_1, 'Data_Quality_Flag'] = 'Anomaly'
df.loc[condition_6_1, 'Anomaly_Type'] = 'STRESS_SLEEP_6.1'
anomaly_count['STRESS_SLEEP_6.1'] = condition_6_1.sum()
print(f"  - 类型6.1 (高压力但高睡眠质量): {condition_6_1.sum()}条")

# 条件6.2：压力<=2 且 睡眠质量<=4（且尚未被标记）
condition_6_2 = (df['Stress Level (scale: 1-10)'] <= 2) & \
                (df['Quality of Sleep (scale: 1-10)'] <= 4) & \
                (df['Data_Quality_Flag'] == 'Normal')
df.loc[condition_6_2, 'Data_Quality_Flag'] = 'Anomaly'
df.loc[condition_6_2, 'Anomaly_Type'] = 'STRESS_SLEEP_6.2'
anomaly_count['STRESS_SLEEP_6.2'] = condition_6_2.sum()
print(f"  - 类型6.2 (低压力但低睡眠质量): {condition_6_2.sum()}条")

# 条件9.1：日步数>=18000 且 运动时长<=30（且尚未被标记）
condition_9_1 = (df['Daily Steps'] >= 18000) & \
                (df['Physical Activity Level (minutes/day)'] <= 30) & \
                (df['Data_Quality_Flag'] == 'Normal')
df.loc[condition_9_1, 'Data_Quality_Flag'] = 'Anomaly'
df.loc[condition_9_1, 'Anomaly_Type'] = 'STEPS_ACTIVITY_9.1'
anomaly_count['STEPS_ACTIVITY_9.1'] = condition_9_1.sum()
print(f"  - 类型9.1 (高步数但低运动时长): {condition_9_1.sum()}条")

# 统计异常总数
total_anomalies = (df['Data_Quality_Flag'] == 'Anomaly').sum()
print(f"\n✓ 异常记录总数: {total_anomalies}条 ({total_anomalies/len(df)*100:.2f}%)")

# 5. 生成数据集
print("\n[步骤5] 生成清洗后的数据集...")

# 5.1 完整标注数据集（包含所有记录和质量标记）
df_full_annotated = df.copy()
df_full_annotated.to_csv('sleep_health_lifestyle_dataset_full_annotated.csv', index=False)
print(f"✓ 完整标注数据集: sleep_health_lifestyle_dataset_full_annotated.csv ({len(df_full_annotated)}条)")

# 5.2 清洗后数据集（仅包含正常记录）
df_cleaned = df[df['Data_Quality_Flag'] == 'Normal'].copy()
# 删除质量标记列（这些列只用于内部标注）
df_cleaned = df_cleaned.drop(columns=['Data_Quality_Flag', 'Anomaly_Type'])
df_cleaned.to_csv('sleep_health_lifestyle_dataset_cleaned.csv', index=False)
print(f"✓ 清洗后数据集: sleep_health_lifestyle_dataset_cleaned.csv ({len(df_cleaned)}条)")

# 5.3 异常数据集（仅包含异常记录）
df_anomalies = df[df['Data_Quality_Flag'] == 'Anomaly'].copy()
df_anomalies.to_csv('sleep_health_lifestyle_dataset_anomalies.csv', index=False)
print(f"✓ 异常数据集: sleep_health_lifestyle_dataset_anomalies.csv ({len(df_anomalies)}条)")

# 6. 生成清洗报告
print("\n[步骤6] 生成清洗报告...")

report_lines = []
report_lines.append("# 睡眠健康数据集清洗报告")
report_lines.append("")
report_lines.append(f"**清洗时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("## 数据清洗统计")
report_lines.append("")
report_lines.append("| 数据集类型 | 记录数 | 占比 | 文件名 |")
report_lines.append("|-----------|--------|------|--------|")
report_lines.append(f"| 原始数据集 | {len(df)} | 100.00% | sleep_health_lifestyle_dataset.csv |")
report_lines.append(f"| 清洗后数据集 | {len(df_cleaned)} | {len(df_cleaned)/len(df)*100:.2f}% | sleep_health_lifestyle_dataset_cleaned.csv |")
report_lines.append(f"| 异常数据集 | {len(df_anomalies)} | {len(df_anomalies)/len(df)*100:.2f}% | sleep_health_lifestyle_dataset_anomalies.csv |")
report_lines.append(f"| 完整标注数据集 | {len(df_full_annotated)} | 100.00% | sleep_health_lifestyle_dataset_full_annotated.csv |")
report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("## 异常类型统计")
report_lines.append("")
report_lines.append("| 异常类型 | 描述 | 数量 | 占总异常比例 |")
report_lines.append("|---------|------|------|-------------|")

for anomaly_type, count in anomaly_count.items():
    desc = {
        'AGE_OCCUPATION_1.2': '年龄<30岁但职业为Retired',
        'AGE_OCCUPATION_1.3': '年龄>=70岁但职业为Student',
        'STRESS_SLEEP_6.1': '压力>=9分但睡眠质量>=8分',
        'STRESS_SLEEP_6.2': '压力<=2分但睡眠质量<=4分',
        'STEPS_ACTIVITY_9.1': '日步数>=18000但运动时长<=30分钟'
    }[anomaly_type]
    
    pct = (count / total_anomalies * 100) if total_anomalies > 0 else 0
    report_lines.append(f"| {anomaly_type} | {desc} | {count} | {pct:.2f}% |")

report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("## 异常记录详情")
report_lines.append("")

# 按异常类型列出详细记录
for anomaly_type in anomaly_count.keys():
    if anomaly_count[anomaly_type] > 0:
        report_lines.append(f"### {anomaly_type}")
        report_lines.append("")
        
        # 获取该类型的异常记录
        anomaly_records = df_anomalies[df_anomalies['Anomaly_Type'] == anomaly_type]
        
        # 选择关键列展示
        if 'AGE_OCCUPATION' in anomaly_type:
            cols = ['Person ID', 'Age', 'Occupation', 'Gender']
        elif 'STRESS_SLEEP' in anomaly_type:
            cols = ['Person ID', 'Stress Level (scale: 1-10)', 
                   'Quality of Sleep (scale: 1-10)', 'Sleep Disorder']
        else:  # STEPS_ACTIVITY
            cols = ['Person ID', 'Daily Steps', 
                   'Physical Activity Level (minutes/day)', 'BMI Category']
        
        # 转换为markdown表格
        report_lines.append("| " + " | ".join(cols) + " |")
        report_lines.append("|" + "|".join(['---' for _ in cols]) + "|")
        
        for _, row in anomaly_records.iterrows():
            values = [str(row[col]) for col in cols]
            report_lines.append("| " + " | ".join(values) + " |")
        
        report_lines.append("")

report_lines.append("---")
report_lines.append("")
report_lines.append("## 清洗标准说明")
report_lines.append("")
report_lines.append("清洗依据以下逻辑异常标准：")
report_lines.append("")
report_lines.append("1. **年龄与职业不匹配**：年龄过小却已退休，或年龄过大仍是学生")
report_lines.append("2. **压力与睡眠质量矛盾**：极高压力却有极高睡眠质量，或极低压力却睡眠质量很差")
report_lines.append("3. **步数与运动时长矛盾**：步数很高但运动时间很短")
report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("## 文件说明")
report_lines.append("")
report_lines.append("### 推荐使用的数据集")
report_lines.append("- **sleep_health_lifestyle_dataset_cleaned.csv**：推荐用于后续数据分析，仅包含正常记录")
report_lines.append("")
report_lines.append("### 参考数据集")
report_lines.append("- **sleep_health_lifestyle_dataset_anomalies.csv**：异常记录，供研究参考")
report_lines.append("- **sleep_health_lifestyle_dataset_full_annotated.csv**：包含质量标记的完整数据")
report_lines.append("")
report_lines.append("### 备份数据集")
report_lines.append("- **sleep_health_lifestyle_dataset_backup.csv**：原始数据的完整备份")
report_lines.append("")
report_lines.append("---")
report_lines.append("")
report_lines.append("## 数据质量评估")
report_lines.append("")
report_lines.append(f"- **清洗前数据量**: {len(df)}条")
report_lines.append(f"- **清洗后数据量**: {len(df_cleaned)}条")
report_lines.append(f"- **数据保留率**: {len(df_cleaned)/len(df)*100:.2f}%")
report_lines.append(f"- **异常剔除率**: {len(df_anomalies)/len(df)*100:.2f}%")
report_lines.append("")
report_lines.append("**结论**: 清洗后的数据集保留了绝大部分数据，同时剔除了明显的逻辑异常，适合进行后续的数据分析和建模工作。")

# 写入报告
with open('data_cleaning_report.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print(f"✓ 清洗报告: data_cleaning_report.md")

# 7. 完成
print("\n" + "=" * 80)
print("数据清洗完成！")
print("=" * 80)
print("\n生成文件列表:")
print("  1. sleep_health_lifestyle_dataset_backup.csv (原始备份)")
print("  2. sleep_health_lifestyle_dataset_cleaned.csv (推荐使用)")
print("  3. sleep_health_lifestyle_dataset_anomalies.csv (异常记录)")
print("  4. sleep_health_lifestyle_dataset_full_annotated.csv (完整标注)")
print("  5. data_cleaning_report.md (清洗报告)")
print("\n推荐使用: sleep_health_lifestyle_dataset_cleaned.csv")
print("=" * 80)
