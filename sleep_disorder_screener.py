"""
睡眠障碍风险智能筛查器
基于数据集特征分析开发的规则引擎
"""
import pandas as pd

class SleepDisorderScreener:
    def __init__(self):
        self.risk_thresholds = {
            'Low': 30,
            'Medium': 60,
            'High': 80
        }

    def assess_apnea_risk(self, person_data):
        """
        评估睡眠呼吸暂停(Sleep Apnea)风险
        * 调整参数以适应数据集特征 (平均年龄较轻, 血压差异不明显)
        """
        score = 0
        risk_factors = []
        
        # 1. BMI (核心因子 - 提高权重)
        bmi_cat = person_data.get('BMI Category', 'Normal')
        if bmi_cat == 'Obese':
            score += 60  # 直接进入中等风险
            risk_factors.append("肥胖 (Obese)")
        elif bmi_cat == 'Overweight':
            score += 40
            risk_factors.append("超重 (Overweight)")
            
        # 2. 血压 (辅助因子)
        sys = person_data.get('Systolic', 120)
        dia = person_data.get('Diastolic', 80)
        
        if sys >= 140 or dia >= 90:
            score += 30
            risk_factors.append(f"高血压 ({sys}/{dia})")
        elif sys >= 130 or dia >= 85:
            score += 20
            risk_factors.append(f"血压偏高 ({sys}/{dia})")
            
        # 3. 压力水平 
        stress = person_data.get('Stress Level', 5)
        if stress >= 6:
            score += 15
            risk_factors.append(f"高压力 (Level {stress})")
            
        # 4. 年龄修正 (下调阈值)
        age = person_data.get('Age', 30)
        if age >= 35: # 数据集平均发病年龄37岁
            score += 20
            risk_factors.append("年龄 > 35")
            
        return min(100, score), risk_factors

    def assess_insomnia_risk(self, person_data):
        """
        评估失眠(Insomnia)风险
        """
        score = 0
        risk_factors = []
        
        # 1. 压力水平 (主要诱因 - 放宽门槛)
        stress = person_data.get('Stress Level', 5)
        if stress >= 7:
            score += 45
            risk_factors.append(f"极高压力 (Level {stress})")
        elif stress >= 5: # 适度压力也可能导致敏感人群失眠
            score += 20
            risk_factors.append(f"压力 (Level {stress})")
            
        # 2. 睡眠时长
        sleep_dur = person_data.get('Sleep Duration', 8)
        if sleep_dur < 6:
            score += 35
            risk_factors.append(f"睡眠严重不足 ({sleep_dur}h)")
        elif sleep_dur < 7:
            score += 20
            risk_factors.append(f"睡眠偏少 ({sleep_dur}h)")
            
        # 3. BMI (双向关注)
        bmi_cat = person_data.get('BMI Category', 'Normal')
        if bmi_cat == 'Underweight':
            score += 30
            risk_factors.append("体重过轻 (Underweight)")
        elif bmi_cat == 'Obese':
            score += 15
            risk_factors.append("肥胖")
            
        # 4. 运动量 (异常高)
        steps = person_data.get('Daily Steps', 5000)
        if steps > 10000:
            score += 10
            
        return min(100, score), risk_factors

    def get_risk_level(self, score):
        if score >= self.risk_thresholds['High']:
            return "高风险 (High Risk)"
        elif score >= self.risk_thresholds['Medium']:
            return "中风险 (Medium Risk)"
        elif score >= self.risk_thresholds['Low']:
            return "低风险 (Low Risk)"
        else:
            return "极低风险 (Minimal Risk)"

    def screen(self, person_data):
        """对单人进行综合筛查"""
        apnea_score, apnea_factors = self.assess_apnea_risk(person_data)
        insomnia_score, insomnia_factors = self.assess_insomnia_risk(person_data)
        
        return {
            'Apnea_Score': apnea_score,
            'Apnea_Level': self.get_risk_level(apnea_score),
            'Apnea_Factors': apnea_factors,
            'Insomnia_Score': insomnia_score,
            'Insomnia_Level': self.get_risk_level(insomnia_score),
            'Insomnia_Factors': insomnia_factors
        }

def batch_screen(df):
    """批量筛查数据集"""
    screener = SleepDisorderScreener()
    results = []
    
    for idx, row in df.iterrows():
        # 准备数据以匹配接口
        sys, dia = str(row['Blood Pressure (systolic/diastolic)']).split('/')
        data = {
            'Age': row['Age'],
            'BMI Category': row['BMI Category'],
            'Systolic': int(sys),
            'Diastolic': int(dia),
            'Stress Level': row['Stress Level (scale: 1-10)'],
            'Sleep Duration': row['Sleep Duration (hours)'],
            'Daily Steps': row['Daily Steps']
        }
        
        res = screener.screen(data)
        
        # 记录结果
        result_row = {
            'Person ID': row['Person ID'],
            'Actual_Disorder': row['Sleep Disorder'],
            **res
        }
        results.append(result_row)
        
    return pd.DataFrame(results)

if __name__ == '__main__':
    # 简单的测试
    test_person = {
        'Age': 50, 'BMI Category': 'Obese', 
        'Systolic': 142, 'Diastolic': 95, 
        'Stress Level': 6, 'Sleep Duration': 6.5,
        'Daily Steps': 6000
    }
    screener = SleepDisorderScreener()
    print("测试样本筛查结果:", screener.screen(test_person))
