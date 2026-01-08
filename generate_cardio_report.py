"""
心血管健康评分 - 个人报告生成器
"""
import pandas as pd
import sys

def generate_report(person_id=None):
    try:
        df = pd.read_csv('cardio_health_score_results.csv')
    except:
        print("未找到结果文件")
        return

    # 如果未指定ID, 找分最低的那个
    if person_id is None:
        person_id = df.loc[df['Cardio_Score'].idxmin(), 'Person ID']
    
    # 获取该人员数据
    person = df[df['Person ID'] == person_id].iloc[0]
    
    report = f"""# 个人心血管健康评估报告

**Person ID**: {person['Person ID']}
**日期**: 2026-01-08

---

## 📊 综合评估

**【综合心血管健康分数】**: {person['Cardio_Score']} / 100
**【风险等级】**: {person['Risk_Level']} {person['Risk_Stars']}

---

## 🩺 分项得分详情

### 1. 血压健康
**得分**: {person['Score_BP']} 分
- **测量值**: {person['Systolic']}/{person['Diastolic']} mmHg
- **评价**: {"理想" if person['Score_BP']==100 else "正常" if person['Score_BP']>=90 else "需关注"}

### 2. 心率健康
**得分**: {person['Score_HR']} 分
- **静息心率**: {person['Heart Rate (bpm)']} bpm
- **评价**: {"优秀" if person['Score_HR']==100 else "良好" if person['Score_HR']>=85 else "偏离理想范围"}

### 3. 生活方式匹配度
**得分**: {person['Score_Lifestyle']} 分
- **日常活动**: {person['Daily Steps']} 步
- **BMI分类**: {person['BMI Category']}
- **睡眠时长**: {person['Sleep Duration (hours)']} 小时
- **压力水平**: {person['Stress Level (scale: 1-10)']}/10

### 4. 生活方式协同效应
**得分**: {person['Score_Correlation']} 分
- 评估生活方式对心血管健康的综合保护作用。

---

## 💡 改善建议

{generate_advice(person)}

---
*注: 本报告基于统计模型生成, 仅供参考, 不能替代专业医疗诊断。*
"""
    
    filename = f"cardio_report_{person['Person ID']}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"报告已生成: {filename}")
    return filename

def generate_advice(person):
    advice = []
    
    # 血压建议
    if person['Score_BP'] < 80:
        advice.append("- ⚠ **关注血压**: 您的血压值偏离理想范围, 建议定期监测并在医生指导下管理。")
    
    # 运动建议
    if person['Daily Steps'] < 7000:
        advice.append("- 🏃 **增加运动**: 您的日常步数较低, 建议逐步增加到每天7000-10000步, 有助于改善心血管功能。")
    
    # 睡眠建议
    if person['Sleep Duration (hours)'] < 7:
        advice.append("- 😴 **改善睡眠**: 睡眠不足可能增加心血管负担, 建议保证每晚7-9小时高质量睡眠。")
        
    # 压力建议
    if person['Stress Level (scale: 1-10)'] > 6:
        advice.append("- 🧘 **压力管理**: 高压力水平是心血管疾病的风险因素, 建议尝试冥想、深呼吸或咨询专业人士。")
        
    if not advice:
        advice.append("- 🎉 **保持现状**: 您的生活方式非常健康, 请继续保持!")
        
    return "\n".join(advice)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        generate_report(int(sys.argv[1]))
    else:
        generate_report()
