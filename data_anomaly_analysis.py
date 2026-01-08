import pandas as pd
import numpy as np

# 读取数据
df = pd.read_csv('sleep_health_lifestyle_dataset.csv')

print("=" * 80)
print("睡眠健康数据集 - 逻辑异常检测报告")
print("=" * 80)
print(f"\n数据集总行数: {len(df)}")

# 1. 年龄与职业不匹配
print("\n" + "=" * 80)
print("【异常1】年龄与职业不匹配")
print("=" * 80)

# 年龄<25且职业为Retired（退休）
young_retired = df[(df['Age'] < 25) & (df['Occupation'] == 'Retired')]
print(f"\n1.1 年龄<25岁但职业为Retired的记录: {len(young_retired)}条")
if len(young_retired) > 0:
    print(young_retired[['Person ID', 'Age', 'Occupation', 'Gender']].to_string(index=False))

# 年龄<30且职业为Retired
young_retired_30 = df[(df['Age'] < 30) & (df['Occupation'] == 'Retired')]
print(f"\n1.2 年龄<30岁但职业为Retired的记录: {len(young_retired_30)}条")
if len(young_retired_30) > 0:
    print(young_retired_30[['Person ID', 'Age', 'Occupation', 'Gender']].to_string(index=False))

# 年龄>=70且职业为Student
old_student = df[(df['Age'] >= 70) & (df['Occupation'] == 'Student')]
print(f"\n1.3 年龄>=70岁但职业为Student的记录: {len(old_student)}条")
if len(old_student) > 0:
    print(old_student[['Person ID', 'Age', 'Occupation', 'Gender']].to_string(index=False))

# 2. 极端年龄
print("\n" + "=" * 80)
print("【异常2】极端年龄值")
print("=" * 80)

very_old = df[df['Age'] > 80]
print(f"\n2.1 年龄>80岁的记录: {len(very_old)}条")
if len(very_old) > 0:
    print(very_old[['Person ID', 'Age', 'Gender', 'Occupation']].to_string(index=False))

# 3. 极端睡眠时长
print("\n" + "=" * 80)
print("【异常3】极端睡眠时长")
print("=" * 80)

extreme_sleep_long = df[df['Sleep Duration (hours)'] >= 12]
print(f"\n3.1 睡眠时长>=12小时的记录: {len(extreme_sleep_long)}条")
if len(extreme_sleep_long) > 0:
    print(extreme_sleep_long[['Person ID', 'Age', 'Sleep Duration (hours)', 'Sleep Disorder']].to_string(index=False))

extreme_sleep_short = df[df['Sleep Duration (hours)'] <= 4.2]
print(f"\n3.2 睡眠时长<=4.2小时的记录: {len(extreme_sleep_short)}条")
if len(extreme_sleep_short) > 0:
    print(extreme_sleep_short[['Person ID', 'Age', 'Sleep Duration (hours)', 'Sleep Disorder']].head(10).to_string(index=False))
    if len(extreme_sleep_short) > 10:
        print(f"... 还有 {len(extreme_sleep_short) - 10} 条记录")

# 4. 矛盾的睡眠质量与睡眠障碍
print("\n" + "=" * 80)
print("【异常4】睡眠质量与睡眠障碍矛盾")
print("=" * 80)

# 高质量睡眠但有睡眠障碍
high_quality_with_disorder = df[(df['Quality of Sleep (scale: 1-10)'] >= 8) & 
                                 (df['Sleep Disorder'].isin(['Sleep Apnea', 'Insomnia']))]
print(f"\n4.1 睡眠质量>=8分但有睡眠障碍的记录: {len(high_quality_with_disorder)}条")
if len(high_quality_with_disorder) > 0:
    print(high_quality_with_disorder[['Person ID', 'Quality of Sleep (scale: 1-10)', 
                                       'Sleep Duration (hours)', 'Sleep Disorder']].to_string(index=False))

# 极低睡眠质量但无睡眠障碍
low_quality_no_disorder = df[(df['Quality of Sleep (scale: 1-10)'] <= 2) & 
                              (df['Sleep Disorder'] == 'None')]
print(f"\n4.2 睡眠质量<=2分但无睡眠障碍的记录: {len(low_quality_no_disorder)}条")
if len(low_quality_no_disorder) > 0:
    print(low_quality_no_disorder[['Person ID', 'Quality of Sleep (scale: 1-10)', 
                                    'Sleep Duration (hours)', 'Sleep Disorder']].to_string(index=False))

# 5. 极端运动量与BMI的矛盾
print("\n" + "=" * 80)
print("【异常5】运动量与BMI的矛盾")
print("=" * 80)

# 极高运动量但肥胖
high_activity_obese = df[(df['Physical Activity Level (minutes/day)'] >= 100) & 
                          (df['BMI Category'] == 'Obese')]
print(f"\n5.1 日运动量>=100分钟但BMI为肥胖的记录: {len(high_activity_obese)}条")
if len(high_activity_obese) > 0:
    print(high_activity_obese[['Person ID', 'Physical Activity Level (minutes/day)', 
                                'BMI Category', 'Age']].head(10).to_string(index=False))
    if len(high_activity_obese) > 10:
        print(f"... 还有 {len(high_activity_obese) - 10} 条记录")

# 极低运动量但体重不足
low_activity_underweight = df[(df['Physical Activity Level (minutes/day)'] <= 15) & 
                               (df['BMI Category'] == 'Underweight')]
print(f"\n5.2 日运动量<=15分钟且BMI为体重不足的记录: {len(low_activity_underweight)}条")
if len(low_activity_underweight) > 0:
    print(low_activity_underweight[['Person ID', 'Physical Activity Level (minutes/day)', 
                                     'BMI Category', 'Age']].to_string(index=False))

# 6. 高压力但低压力表现
print("\n" + "=" * 80)
print("【异常6】压力水平与睡眠质量的矛盾")
print("=" * 80)

# 极高压力(>=9)但高质量睡眠(>=8)
high_stress_good_sleep = df[(df['Stress Level (scale: 1-10)'] >= 9) & 
                             (df['Quality of Sleep (scale: 1-10)'] >= 8)]
print(f"\n6.1 压力>=9分但睡眠质量>=8分的记录: {len(high_stress_good_sleep)}条")
if len(high_stress_good_sleep) > 0:
    print(high_stress_good_sleep[['Person ID', 'Stress Level (scale: 1-10)', 
                                   'Quality of Sleep (scale: 1-10)', 'Sleep Disorder']].to_string(index=False))

# 低压力(<=2)但低质量睡眠(<=4)
low_stress_bad_sleep = df[(df['Stress Level (scale: 1-10)'] <= 2) & 
                           (df['Quality of Sleep (scale: 1-10)'] <= 4)]
print(f"\n6.2 压力<=2分但睡眠质量<=4分的记录: {len(low_stress_bad_sleep)}条")
if len(low_stress_bad_sleep) > 0:
    print(low_stress_bad_sleep[['Person ID', 'Stress Level (scale: 1-10)', 
                                 'Quality of Sleep (scale: 1-10)', 'Sleep Disorder']].to_string(index=False))

# 7. 血压异常
print("\n" + "=" * 80)
print("【异常7】血压异常值")
print("=" * 80)

# 解析血压
df[['Systolic', 'Diastolic']] = df['Blood Pressure (systolic/diastolic)'].str.split('/', expand=True).astype(int)

# 极高血压
very_high_bp = df[(df['Systolic'] >= 140) | (df['Diastolic'] >= 95)]
print(f"\n7.1 收缩压>=140 或 舒张压>=95的记录: {len(very_high_bp)}条")
if len(very_high_bp) > 0:
    print(very_high_bp[['Person ID', 'Age', 'Blood Pressure (systolic/diastolic)', 
                         'BMI Category']].head(15).to_string(index=False))
    if len(very_high_bp) > 15:
        print(f"... 还有 {len(very_high_bp) - 15} 条记录")

# 8. 心率异常
print("\n" + "=" * 80)
print("【异常8】心率异常值")
print("=" * 80)

extreme_hr_high = df[df['Heart Rate (bpm)'] >= 100]
print(f"\n8.1 心率>=100 bpm的记录: {len(extreme_hr_high)}条")
if len(extreme_hr_high) > 0:
    print(extreme_hr_high[['Person ID', 'Age', 'Heart Rate (bpm)', 
                            'Physical Activity Level (minutes/day)']].head(10).to_string(index=False))

extreme_hr_low = df[df['Heart Rate (bpm)'] <= 50]
print(f"\n8.2 心率<=50 bpm的记录: {len(extreme_hr_low)}条")
if len(extreme_hr_low) > 0:
    print(extreme_hr_low[['Person ID', 'Age', 'Heart Rate (bpm)', 
                           'Physical Activity Level (minutes/day)']].head(10).to_string(index=False))

# 9. 每日步数异常
print("\n" + "=" * 80)
print("【异常9】每日步数异常")
print("=" * 80)

# 极高步数但低运动量
high_steps_low_activity = df[(df['Daily Steps'] >= 18000) & 
                              (df['Physical Activity Level (minutes/day)'] <= 30)]
print(f"\n9.1 日步数>=18000但运动时长<=30分钟的记录: {len(high_steps_low_activity)}条")
if len(high_steps_low_activity) > 0:
    print(high_steps_low_activity[['Person ID', 'Daily Steps', 
                                    'Physical Activity Level (minutes/day)', 'BMI Category']].head(10).to_string(index=False))

# 极低步数但高运动量
low_steps_high_activity = df[(df['Daily Steps'] <= 3000) & 
                              (df['Physical Activity Level (minutes/day)'] >= 90)]
print(f"\n9.2 日步数<=3000但运动时长>=90分钟的记录: {len(low_steps_high_activity)}条")
if len(low_steps_high_activity) > 0:
    print(low_steps_high_activity[['Person ID', 'Daily Steps', 
                                   'Physical Activity Level (minutes/day)', 'BMI Category']].to_string(index=False))

# 10. 汇总统计
print("\n" + "=" * 80)
print("【汇总】需要重点关注的异常记录")
print("=" * 80)

# 收集所有异常的Person ID
anomaly_ids = set()
anomaly_ids.update(young_retired_30['Person ID'].tolist())
anomaly_ids.update(old_student['Person ID'].tolist())
anomaly_ids.update(very_old['Person ID'].tolist())
anomaly_ids.update(extreme_sleep_long['Person ID'].tolist())
anomaly_ids.update(high_quality_with_disorder['Person ID'].tolist())
anomaly_ids.update(high_activity_obese['Person ID'].tolist())
anomaly_ids.update(high_stress_good_sleep['Person ID'].tolist())

print(f"\n存在至少一种异常的记录总数: {len(anomaly_ids)}条")
print(f"占总数据的比例: {len(anomaly_ids)/len(df)*100:.2f}%")

print("\n" + "=" * 80)
print("分析完成")
print("=" * 80)
