"""
加权健康分数计算器
基于职业分类的个性化健康评分系统
"""

import pandas as pd
import numpy as np


class HealthScoreCalculator:
    """健康分数计算器"""
    
    def __init__(self):
        """初始化基础权重和评分标准"""
        # 基础权重 (总和为1.0)
        self.base_weights = {
            'steps': 0.15,           # 活动步数
            'activity': 0.15,        # 活动时间
            'bmi': 0.20,             # BMI分类
            'stress': 0.15,          # 压力水平
            'sleep_duration': 0.20,  # 睡眠时长
            'sleep_quality': 0.15    # 睡眠质量
        }
        
        # 职业权重调整 (相对于基础权重的调整)
        self.occupation_adjustments = {
            'Office Worker': {
                'steps': +0.05,           # 久坐族需要更多活动
                'activity': +0.05,
                'bmi': 0.00,
                'stress': +0.05,          # 工作压力大
                'sleep_duration': +0.02,
                'sleep_quality': +0.03
            },
            'Manual Labor': {
                'steps': -0.03,           # 已有足够活动
                'activity': -0.03,
                'bmi': +0.05,             # 体重管理重要
                'stress': +0.02,
                'sleep_duration': +0.05,  # 需要充足恢复
                'sleep_quality': +0.04
            },
            'Student': {
                'steps': +0.02,
                'activity': 0.00,
                'bmi': -0.02,
                'stress': +0.05,          # 学习压力
                'sleep_duration': +0.03,
                'sleep_quality': +0.05    # 睡眠质量很重要
            },
            'Retired': {
                'steps': +0.03,
                'activity': +0.02,
                'bmi': +0.03,
                'stress': -0.05,          # 压力较小
                'sleep_duration': +0.02,
                'sleep_quality': +0.03
            }
        }
    
    def get_occupation_weights(self, occupation):
        """
        获取特定职业的权重
        
        Args:
            occupation: 职业类型
            
        Returns:
            dict: 调整后的权重字典
        """
        if occupation not in self.occupation_adjustments:
            return self.base_weights.copy()
        
        weights = self.base_weights.copy()
        adjustments = self.occupation_adjustments[occupation]
        
        # 应用调整
        for key in weights:
            weights[key] += adjustments.get(key, 0)
        
        # 归一化权重,确保总和为1.0
        total = sum(weights.values())
        weights = {k: v/total for k, v in weights.items()}
        
        return weights
    
    def score_steps(self, daily_steps):
        """
        活动步数评分 (0-100分)
        
        Args:
            daily_steps: 每日步数
            
        Returns:
            float: 评分 (0-100)
        """
        if daily_steps >= 10000:
            return 100.0
        elif daily_steps >= 7000:
            # 7000-9999步: 80-99分线性插值
            return 80 + (daily_steps - 7000) / 3000 * 19
        elif daily_steps >= 5000:
            # 5000-6999步: 60-79分
            return 60 + (daily_steps - 5000) / 2000 * 19
        elif daily_steps >= 3000:
            # 3000-4999步: 40-59分
            return 40 + (daily_steps - 3000) / 2000 * 19
        else:
            # <3000步: 20-39分
            return max(20, 20 + daily_steps / 3000 * 19)
    
    def score_activity(self, activity_minutes, occupation=None):
        """
        活动时间评分 (0-100分)
        
        Args:
            activity_minutes: 每日活动时间(分钟)
            occupation: 职业类型(用于判断是否为体力劳动)
            
        Returns:
            float: 评分 (0-100)
        """
        if 60 <= activity_minutes <= 90:
            return 100.0
        elif 30 <= activity_minutes < 60:
            # 30-59分钟: 80-99分
            return 80 + (activity_minutes - 30) / 30 * 19
        elif 15 <= activity_minutes < 30:
            # 15-29分钟: 60-79分
            return 60 + (activity_minutes - 15) / 15 * 19
        elif activity_minutes < 15:
            return 40.0
        else:  # >90分钟
            # 体力劳动者不扣分,其他职业适度扣分
            if occupation == 'Manual Labor':
                return 100.0
            else:
                # 超过90分钟后逐渐降低分数
                excess = activity_minutes - 90
                return max(70, 100 - excess * 0.2)
    
    def score_bmi(self, bmi_category):
        """
        BMI分类评分 (0-100分)
        
        Args:
            bmi_category: BMI分类 (Normal/Overweight/Underweight/Obese)
            
        Returns:
            float: 评分 (0-100)
        """
        bmi_scores = {
            'Normal': 100.0,
            'Overweight': 70.0,
            'Underweight': 70.0,
            'Obese': 40.0
        }
        return bmi_scores.get(bmi_category, 50.0)
    
    def score_stress(self, stress_level):
        """
        压力水平评分 (0-100分)
        
        Args:
            stress_level: 压力等级 (1-10)
            
        Returns:
            float: 评分 (0-100)
        """
        if 3 <= stress_level <= 5:
            # 适度压力
            return 100.0
        elif 6 <= stress_level <= 7:
            # 中等压力
            return 70.0
        elif 1 <= stress_level <= 2:
            # 压力过低
            return 60.0
        elif stress_level == 8:
            return 40.0
        elif stress_level == 9:
            return 35.0
        else:  # stress_level == 10
            return 30.0
    
    def score_sleep_duration(self, sleep_hours):
        """
        睡眠时长评分 (0-100分)
        
        Args:
            sleep_hours: 睡眠时长(小时)
            
        Returns:
            float: 评分 (0-100)
        """
        if 7 <= sleep_hours <= 9:
            # 理想睡眠时长
            return 100.0
        elif 6 <= sleep_hours < 7:
            return 80.0
        elif 9 < sleep_hours <= 10:
            return 85.0
        elif 5 <= sleep_hours < 6:
            return 60.0
        elif sleep_hours < 5:
            return 30.0
        else:  # >10小时
            # 过度睡眠
            return 50.0
    
    def score_sleep_quality(self, quality_score):
        """
        睡眠质量评分 (0-100分)
        
        Args:
            quality_score: 睡眠质量分数 (1-10)
            
        Returns:
            float: 评分 (0-100)
        """
        if 8 <= quality_score <= 10:
            # 高质量睡眠
            return 100.0
        elif 6 <= quality_score < 8:
            # 6-7分: 70-85分
            return 70 + (quality_score - 6) / 2 * 15
        elif 4 <= quality_score < 6:
            # 4-5分: 50-65分
            return 50 + (quality_score - 4) / 2 * 15
        else:  # 1-3分
            # 1-3分: 20-45分
            return 20 + (quality_score - 1) / 2 * 25
    
    def get_health_level(self, score):
        """
        根据分数获取健康等级
        
        Args:
            score: 健康分数 (0-100)
            
        Returns:
            str: 健康等级
        """
        if score >= 85:
            return '优秀'
        elif score >= 70:
            return '良好'
        elif score >= 55:
            return '中等'
        elif score >= 40:
            return '较差'
        else:
            return '差'
    
    def calculate_health_score(self, row):
        """
        计算单条记录的健康分数
        
        Args:
            row: DataFrame的一行数据
            
        Returns:
            dict: 包含总分、等级和各项得分的字典
        """
        # 提取数据
        occupation = row['Occupation']
        daily_steps = row['Daily Steps']
        activity_minutes = row['Physical Activity Level (minutes/day)']
        bmi_category = row['BMI Category']
        stress_level = row['Stress Level (scale: 1-10)']
        sleep_hours = row['Sleep Duration (hours)']
        sleep_quality = row['Quality of Sleep (scale: 1-10)']
        
        # 计算各项得分
        score_steps = self.score_steps(daily_steps)
        score_activity = self.score_activity(activity_minutes, occupation)
        score_bmi = self.score_bmi(bmi_category)
        score_stress = self.score_stress(stress_level)
        score_sleep_dur = self.score_sleep_duration(sleep_hours)
        score_sleep_qual = self.score_sleep_quality(sleep_quality)
        
        # 获取职业权重
        weights = self.get_occupation_weights(occupation)
        
        # 加权求和
        total_score = (
            score_steps * weights['steps'] +
            score_activity * weights['activity'] +
            score_bmi * weights['bmi'] +
            score_stress * weights['stress'] +
            score_sleep_dur * weights['sleep_duration'] +
            score_sleep_qual * weights['sleep_quality']
        )
        
        # 获取健康等级
        health_level = self.get_health_level(total_score)
        
        return {
            'Health_Score': round(total_score, 1),
            'Health_Level': health_level,
            'Score_Steps': round(score_steps, 1),
            'Score_Activity': round(score_activity, 1),
            'Score_BMI': round(score_bmi, 1),
            'Score_Stress': round(score_stress, 1),
            'Score_Sleep_Duration': round(score_sleep_dur, 1),
            'Score_Sleep_Quality': round(score_sleep_qual, 1),
            'Weight_Steps': round(weights['steps'], 3),
            'Weight_Activity': round(weights['activity'], 3),
            'Weight_BMI': round(weights['bmi'], 3),
            'Weight_Stress': round(weights['stress'], 3),
            'Weight_Sleep_Duration': round(weights['sleep_duration'], 3),
            'Weight_Sleep_Quality': round(weights['sleep_quality'], 3)
        }


def main():
    """主函数:批量计算健康分数"""
    print("=" * 80)
    print("加权健康分数计算器")
    print("=" * 80)
    
    # 读取清洗后的数据
    print("\n[1] 读取数据集...")
    df = pd.read_csv('sleep_health_lifestyle_dataset_cleaned.csv')
    print(f"✓ 数据集加载完成: {len(df)} 条记录")
    
    # 初始化计算器
    calculator = HealthScoreCalculator()
    
    # 批量计算健康分数
    print("\n[2] 计算健康分数...")
    results = []
    for idx, row in df.iterrows():
        result = calculator.calculate_health_score(row)
        results.append(result)
    
    # 将结果转换为DataFrame
    results_df = pd.DataFrame(results)
    
    # 合并到原数据集
    df_with_scores = pd.concat([df, results_df], axis=1)
    
    # 保存结果
    output_file = 'sleep_health_lifestyle_dataset_with_scores.csv'
    df_with_scores.to_csv(output_file, index=False)
    print(f"✓ 健康分数计算完成,已保存到: {output_file}")
    
    # 统计分析
    print("\n[3] 健康分数统计:")
    print(f"  平均分: {results_df['Health_Score'].mean():.1f}")
    print(f"  中位数: {results_df['Health_Score'].median():.1f}")
    print(f"  最高分: {results_df['Health_Score'].max():.1f}")
    print(f"  最低分: {results_df['Health_Score'].min():.1f}")
    
    print("\n[4] 健康等级分布:")
    level_counts = results_df['Health_Level'].value_counts()
    for level in ['优秀', '良好', '中等', '较差', '差']:
        count = level_counts.get(level, 0)
        pct = count / len(results_df) * 100
        print(f"  {level}: {count}人 ({pct:.1f}%)")
    
    print("\n[5] 各职业平均健康分数:")
    occupation_scores = df_with_scores.groupby('Occupation')['Health_Score'].mean().sort_values(ascending=False)
    for occupation, score in occupation_scores.items():
        print(f"  {occupation}: {score:.1f}分")
    
    print("\n" + "=" * 80)
    print("计算完成!")
    print("=" * 80)


if __name__ == '__main__':
    main()
