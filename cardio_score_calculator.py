import pandas as pd
import numpy as np

class CardioScoreCalculator:
    def __init__(self):
        pass

    def parse_blood_pressure(self, bp_str):
        """解析血压字符串 '124/70' -> (124, 70)"""
        try:
            sys, dia = map(int, bp_str.split('/'))
            return sys, dia
        except:
            return None, None

    def calculate_bp_score(self, systolic, diastolic, age, gender):
        """
        计算血压分数 (医学分级 + 年龄/性别调整)
        """
        if pd.isna(systolic) or pd.isna(diastolic):
            return 50.0

        # 1. 基础评分
        score = 0
        
        # 判断收缩压/舒张压等级 (取最差情况)
        # 理想
        if systolic < 120 and diastolic < 80:
            score = 100
        # 正常
        elif systolic < 130 and diastolic < 85:
            score = 90
        # 正常高值
        elif systolic < 140 and diastolic < 90:
            score = 75
        # 1级高血压
        elif systolic < 160 and diastolic < 100:
            score = 55
        # 2级高血压
        elif systolic < 180 and diastolic < 110:
            score = 35
        # 3级高血压 (>=180 or >=110)
        else:
            score = 20
        
        # 低血压检查
        if systolic < 90 and diastolic < 60:
            score = 65

        # 2. 年龄调整
        age_bonus = 0
        if 41 <= age <= 60:
            # 中年人正常高值容忍度
            if 75 <= score <= 90:
                age_bonus = 5
        elif age > 60:
            # 老年人正常高值容忍度
            if 75 <= score <= 90:
                age_bonus = 10
        
        # 3. 性别调整
        gender_bonus = 0
        if gender == 'Female':
            # 女性低血压容忍
            if systolic < 90:
                gender_bonus = 5
        elif gender == 'Male':
            # 男性高血压风险更高, 稍微严厉一点? 
            # 暂时保持标准
            pass

        final_score = min(100, score + age_bonus + gender_bonus)
        return final_score

    def calculate_hr_score(self, hr, age, occupation, gender):
        """
        计算心率分数 (静息心率 + 年龄/职业调整)
        """
        if pd.isna(hr):
            return 50.0

        # 1. 确定理想心率范围 (年龄调整)
        if age <= 30:
            ideal_low, ideal_high = 60, 80
        elif age <= 50:
            ideal_low, ideal_high = 65, 85
        elif age <= 70:
            ideal_low, ideal_high = 70, 90
        else: # > 70
            ideal_low, ideal_high = 75, 95

        # 2. 职业/性别调整理想范围
        # 女性心率通常略高
        if gender == 'Female':
            ideal_low += 5
            ideal_high += 5
        
        # 体力劳动者/退休人员心率可能不同
        if occupation == 'Manual Labor':
            ideal_high += 5
        elif occupation == 'Retired':
            ideal_high += 3

        # 3. 评分
        if ideal_low <= hr <= ideal_high:
            return 100.0
        
        # 偏离程度评分
        # 使用基础表格作为参考, 但结合动态范围
        # 优秀范围: [ideal_low, ideal_high] -> 100
        
        # 良好 (轻微偏离 +/- 5-10 bpm)
        if (ideal_low - 10) <= hr < ideal_low or ideal_high < hr <= (ideal_high + 10):
            return 85.0
        
        # 一般 (偏离 10-20 bpm)
        if (ideal_low - 20) <= hr < (ideal_low - 10) or (ideal_high + 10) < hr <= (ideal_high + 20):
            return 70.0
        
        # 偏高/偏低 (偏离 > 20)
        return 40.0

    def calculate_lifestyle_score(self, steps, activity_min, sleep_dur, sleep_qual, stress, bmi_cat):
        """
        生活方式匹配度评分
        """
        # A. 运动充足度 (25%)
        # 步数达标(7000-10000)
        score_steps = 0
        if steps >= 10000: score_steps = 100
        elif steps >= 7000: score_steps = 85
        elif steps >= 5000: score_steps = 60
        else: score_steps = 40
        
        # 活动时间达标(30-60分钟)
        score_activity = 0
        if 60 <= activity_min <= 90: score_activity = 100
        elif 30 <= activity_min < 60: score_activity = 90
        elif activity_min >= 15: score_activity = 70
        else: score_activity = 40
        
        score_motion = (score_steps + score_activity) / 2

        # B. 睡眠质量 (30%)
        # 时长
        score_dur = 0
        if 7 <= sleep_dur <= 9: score_dur = 100
        elif 6 <= sleep_dur < 7 or 9 < sleep_dur <= 10: score_dur = 80
        else: score_dur = 50
        
        # 质量
        score_qual = 0
        if sleep_qual >= 8: score_qual = 100
        elif sleep_qual >= 6: score_qual = 80
        elif sleep_qual >= 4: score_qual = 60
        else: score_qual = 40
        
        score_sleep = score_dur * 0.5 + score_qual * 0.5

        # C. 压力管理 (25%)
        score_stress = 0
        if 3 <= stress <= 5: score_stress = 100
        elif stress <= 2: score_stress = 90 # 低压力也算好
        elif 6 <= stress <= 7: score_stress = 70
        else: score_stress = 40

        # D. BMI健康度 (20%)
        score_bmi = 0
        if bmi_cat == 'Normal' or bmi_cat == 'Normal Weight':
            score_bmi = 100
        elif bmi_cat == 'Overweight':
            score_bmi = 70
        elif bmi_cat == 'Underweight': # 虽然不是最优,但比肥胖好
            score_bmi = 70
        else: # Obese
            score_bmi = 40

        # 加权总分
        total = (score_motion * 0.25 + 
                 score_sleep * 0.30 + 
                 score_stress * 0.25 + 
                 score_bmi * 0.20)
        
        return total

    def calculate_correlation_score(self, steps, sleep_qual, stress, sleep_disorder):
        """
        生活方式-心血管相关性评分 (协同效应)
        """
        # A. 运动保护效应 (30%)
        # 假设运动有助于心血管
        motion_effect = 0
        if steps >= 7000: motion_effect = 100
        elif steps >= 5000: motion_effect = 70
        else: motion_effect = 40

        # B. 睡眠质量影响 (30%)
        sleep_effect = 0
        if sleep_qual >= 7: sleep_effect = 100
        elif sleep_qual >= 5: sleep_effect = 70
        else: sleep_effect = 40

        # C. 压力管理效应 (25%)
        stress_effect = 0
        if stress <= 5: stress_effect = 100
        elif stress <= 7: stress_effect = 70
        else: stress_effect = 40

        # D. 睡眠障碍风险调整 (15%)
        disorder_score = 100
        if pd.notna(sleep_disorder) and sleep_disorder != 'None':
            if 'Insomnia' in sleep_disorder:
                disorder_score = 60 # 风险增加
            elif 'Apnea' in sleep_disorder:
                disorder_score = 50 # 风险较高

        total = (motion_effect * 0.30 +
                 sleep_effect * 0.30 +
                 stress_effect * 0.25 +
                 disorder_score * 0.15)
        
        return total

    def get_risk_level(self, score):
        if score >= 85: return "低风险", "⭐⭐⭐⭐⭐"
        elif score >= 70: return "中低风险", "⭐⭐⭐⭐"
        elif score >= 55: return "中等风险", "⭐⭐⭐"
        elif score >= 40: return "中高风险", "⭐⭐"
        else: return "高风险", "⭐"

    def process_dataset(self, df):
        results = []
        
        for idx, row in df.iterrows():
            sys, dia = self.parse_blood_pressure(row['Blood Pressure (systolic/diastolic)'])
            
            # 1. 血压分数
            score_bp = self.calculate_bp_score(sys, dia, row['Age'], row['Gender'])
            
            # 2. 心率分数
            score_hr = self.calculate_hr_score(row['Heart Rate (bpm)'], row['Age'], row['Occupation'], row['Gender'])
            
            # 3. 生活方式分数
            score_life = self.calculate_lifestyle_score(row['Daily Steps'], 
                                                        row['Physical Activity Level (minutes/day)'],
                                                        row['Sleep Duration (hours)'],
                                                        row['Quality of Sleep (scale: 1-10)'],
                                                        row['Stress Level (scale: 1-10)'],
                                                        row['BMI Category'])
            
            # 4. 相关性分数
            score_corr = self.calculate_correlation_score(row['Daily Steps'],
                                                          row['Quality of Sleep (scale: 1-10)'],
                                                          row['Stress Level (scale: 1-10)'],
                                                          row['Sleep Disorder'])
            
            # 5. 综合分数
            # 血压35% + 心率25% + 生活25% + 相关15%
            final_score = (score_bp * 0.35 + 
                           score_hr * 0.25 + 
                           score_life * 0.25 + 
                           score_corr * 0.15)
            
            risk_label, risk_stars = self.get_risk_level(final_score)
            
            results.append({
                'Person ID': row['Person ID'],
                'Cardio_Score': round(final_score, 1),
                'Risk_Level': risk_label,
                'Risk_Stars': risk_stars,
                'Score_BP': round(score_bp, 1),
                'Score_HR': round(score_hr, 1),
                'Score_Lifestyle': round(score_life, 1),
                'Score_Correlation': round(score_corr, 1),
                # 用于分析的派生列
                'Systolic': sys,
                'Diastolic': dia
            })
            
        return pd.DataFrame(results)

def main():
    # 读取数据
    print("正在读取数据...")
    try:
        df = pd.read_csv('sleep_health_lifestyle_dataset_cleaned.csv')
    except:
        # 如果找不到cleaned, 尝试原始文件
        df = pd.read_csv('sleep_health_lifestyle_dataset.csv')
    
    calculator = CardioScoreCalculator()
    
    print("正在计算心血管健康分数...")
    result_df = calculator.process_dataset(df)
    
    # 合并原始数据以便查看
    final_df = pd.merge(df, result_df, on='Person ID')
    
    # 保存结果
    output_file = 'cardio_health_score_results.csv'
    final_df.to_csv(output_file, index=False)
    print(f"计算完成! 结果已保存至 {output_file}")
    
    # 打印统计信息
    print("\n=== 分数统计 ===")
    print(final_df[['Cardio_Score', 'Score_BP', 'Score_HR', 'Score_Lifestyle']].describe().round(1))
    
    print("\n=== 风险等级分布 ===")
    print(final_df['Risk_Level'].value_counts())

if __name__ == '__main__':
    main()
