"""
筛查器验证脚本
验证 SleepDisorderScreener 在数据集上的表现
"""
import pandas as pd
from sleep_disorder_screener import batch_screen
from sklearn.metrics import classification_report, confusion_matrix

def validate():
    print("正在加载数据...")
    try:
        df = pd.read_csv('sleep_health_lifestyle_dataset_cleaned.csv')
    except:
        df = pd.read_csv('sleep_health_lifestyle_dataset.csv')
        
    # 填充NaN
    df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')
    
    print("正在批量运行筛查...")
    results = batch_screen(df)
    
    # 定义简单的二分类验证
    # 1. 验证呼吸暂停 (Apnea) 捕捉率
    # 只要 Apnea_Level 是 High 或 Medium 就算 "Screened_Positive"
    results['Screened_Apnea'] = results['Apnea_Score'] >= 60
    results['Actual_Apnea'] = results['Actual_Disorder'] == 'Sleep Apnea'
    
    print("\n=== 睡眠呼吸暂停 (Sleep Apnea) 筛查验证 ===")
    tp_apnea = len(results[results['Screened_Apnea'] & results['Actual_Apnea']])
    total_apnea = len(results[results['Actual_Apnea']])
    fp_apnea = len(results[results['Screened_Apnea'] & (~results['Actual_Apnea'])])
    
    print(f"实际患病人数: {total_apnea}")
    print(f"筛查出高/中风险人数: {results['Screened_Apnea'].sum()}")
    print(f"成功捕捉 (True Positive): {tp_apnea}")
    print(f"召回率 (Recall): {tp_apnea/total_apnea:.2%}")
    print(f"误报数 (False Positive): {fp_apnea}")
    
    # 2. 验证失眠 (Insomnia) 捕捉率
    results['Screened_Insomnia'] = results['Insomnia_Score'] >= 60
    results['Actual_Insomnia'] = results['Actual_Disorder'] == 'Insomnia'
    
    print("\n=== 失眠 (Insomnia) 筛查验证 ===")
    tp_insomnia = len(results[results['Screened_Insomnia'] & results['Actual_Insomnia']])
    total_insomnia = len(results[results['Actual_Insomnia']])
    fp_insomnia = len(results[results['Screened_Insomnia'] & (~results['Actual_Insomnia'])])
    
    print(f"实际患病人数: {total_insomnia}")
    print(f"筛查出高/中风险人数: {results['Screened_Insomnia'].sum()}")
    print(f"成功捕捉 (True Positive): {tp_insomnia}")
    print(f"召回率 (Recall): {tp_insomnia/total_insomnia:.2%}")
    print(f"误报数 (False Positive): {fp_insomnia}")
    
    # 导出高风险名单
    high_risk = results[
        (results['Apnea_Level'] == '高风险 (High Risk)') | 
        (results['Insomnia_Level'] == '高风险 (High Risk)')
    ]
    
    print(f"\n共发现 {len(high_risk)} 名高风险个体")
    high_risk.to_csv('high_risk_individuals.csv', index=False)
    print("高风险名单已保存至 'high_risk_individuals.csv'")

if __name__ == '__main__':
    validate()
