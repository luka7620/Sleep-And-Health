"""
综合睡眠健康指数 (CSHI) 计算器 v2.0
整合: 睡眠核心(40%) + 运动促眠(25%) + 健康基石(35%)
"""
import pandas as pd
import numpy as np

class SleepIndexCalculator:
    def __init__(self):
        pass

    def load_data(self):
        """加载并合并所需数据集"""
        print("正在加载基础数据...")
        try:
            # 1. 基础生活健康分 (包含Health_Score)
            df_life = pd.read_csv('sleep_health_lifestyle_dataset_with_scores.csv')
            # 2. 心血管健康分 (包含Cardio_Score)
            df_cardio = pd.read_csv('cardio_health_score_results.csv')
            
            # 合并 (基于Person ID)
            # 注意: Cardio表中已经包含了一些列, 我们只取需要的
            df_cardio_subset = df_cardio[['Person ID', 'Cardio_Score', 'Score_BP', 'Score_HR']]
            
            df_merged = pd.merge(df_life, df_cardio_subset, on='Person ID', how='inner')
            return df_merged
        except FileNotFoundError as e:
            print(f"Error: 缺少必要的数据文件 - {e}")
            return None

    def calculate_sleep_dimension(self, row):
        """1. 睡眠核心维度 (40%)"""
        # 时长评分 (0-100)
        dur = row['Sleep Duration (hours)']
        score_dur = 0
        if 7 <= dur <= 9: score_dur = 100
        elif 6 <= dur < 7 or 9 < dur <= 10: score_dur = 85
        elif 5 <= dur < 6: score_dur = 60
        else: score_dur = 40
        
        # 质量评分 (0-100)
        qual = row['Quality of Sleep (scale: 1-10)']
        score_qual = qual * 10
        
        # 维度分: 时长50% + 质量50%
        return score_dur * 0.5 + score_qual * 0.5

    def calculate_motion_dimension(self, row):
        """2. 运动促眠维度 (25%)"""
        # 步数评分
        steps = row['Daily Steps']
        score_steps = min(100, (steps / 7000) * 100)
        if steps >= 10000: score_steps = 100 # 封顶
        
        # 活动时间评分
        activity = row['Physical Activity Level (minutes/day)']
        score_activity = 0
        if 30 <= activity <= 90: score_activity = 100
        else: score_activity = min(100, (activity / 30) * 80)
        
        # 维度分: 步数50% + 时间50%
        return score_steps * 0.5 + score_activity * 0.5

    def calculate_health_dimension(self, row):
        """3. 健康基石维度 (35%)"""
        # Cardio Score (心血管)
        cardio = row['Cardio_Score']
        
        # Health Score (生活方式)
        health = row['Health_Score']
        
        # 维度分: 各占50%
        return cardio * 0.5 + health * 0.5

    def calculate_cshi(self, df):
        """计算综合指数"""
        results = []
        
        print("正在计算综合睡眠健康指数 (CSHI)...")
        print("权重配置: 睡眠(50%) + 心血管(25%) + 生活方式(25%) [已移除运动维度]")
        
        for idx, row in df.iterrows():
            # 计算各维度
            dim_sleep = self.calculate_sleep_dimension(row)
            
            # 健康基石拆解
            dim_cardio = row['Cardio_Score']
            dim_lifestyle = row['Health_Score']
            
            # 加权汇总: 除去运动, 强化睡眠权重, 并独立心血管和生活方式
            cshi = (dim_sleep * 0.50 + 
                    dim_cardio * 0.25 + 
                    dim_lifestyle * 0.25)
            
            risk_label = "优"
            if cshi < 60: risk_label = "差"
            elif cshi < 75: risk_label = "一般"
            elif cshi < 85: risk_label = "良"
            
            results.append({
                'Person ID': row['Person ID'],
                'CSHI_Score': round(cshi, 1),
                'CSHI_Level': risk_label,
                'Dim_Sleep': round(dim_sleep, 1),
                'Dim_Cardio': round(dim_cardio, 1),
                'Dim_Lifestyle': round(dim_lifestyle, 1)
            })
            
        return pd.DataFrame(results)

def main():
    calculator = SleepIndexCalculator()
    
    # 1. 加载
    df = calculator.load_data()
    if df is None: return
    
    # 2. 计算
    result_df = calculator.calculate_cshi(df)
    
    # 3. 合并全量信息
    final_df = pd.merge(df, result_df, on='Person ID')
    
    # 4. 保存
    output_file = 'comprehensive_sleep_health_index.csv'
    final_df.to_csv(output_file, index=False)
    
    print(f"\n计算完成! 结果已保存至 {output_file}")
    print("\n=== CSHI 分数统计 ===")
    print(result_df[['CSHI_Score', 'Dim_Sleep', 'Dim_Cardio', 'Dim_Lifestyle']].describe().round(1))
    
    print("\n=== CSHI 等级分布 ===")
    print(result_df['CSHI_Level'].value_counts())

if __name__ == '__main__':
    main()
