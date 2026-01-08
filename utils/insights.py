"""
自动洞察生成工具
基于数据分析结果生成文本解读
"""

import pandas as pd
import streamlit as st


def generate_sleep_quality_insight(df):
    """生成睡眠质量洞察"""
    avg_quality = df['Quality of Sleep (scale: 1-10)'].mean()
    
    if avg_quality >= 8:
        level = "优秀"
        icon = "🌟"
    elif avg_quality >= 7:
        level = "良好"
        icon = "✅"
    elif avg_quality >= 6:
        level = "中等"
        icon = "⚠️"
    else:
        level = "较差"
        icon = "❌"
    
    return f"{icon} 整体睡眠质量为**{level}** (平均分: {avg_quality:.2f}/10)"


def generate_disorder_insight(df):
    """生成睡眠障碍洞察"""
    disorder_counts = df['Sleep Disorder'].value_counts()
    total = len(df)
    
    insights = []
    
    if 'Sleep Apnea' in disorder_counts:
        apnea_rate = disorder_counts['Sleep Apnea'] / total * 100
        insights.append(f"- 睡眠呼吸暂停: **{apnea_rate:.1f}%** ({disorder_counts['Sleep Apnea']}人)")
    
    if 'Insomnia' in disorder_counts:
        insomnia_rate = disorder_counts['Insomnia'] / total * 100
        insights.append(f"- 失眠症: **{insomnia_rate:.1f}%** ({disorder_counts['Insomnia']}人)")
    
    no_disorder_rate = disorder_counts.get('No Disorder', 0) / total * 100
    insights.append(f"- 健康人群: **{no_disorder_rate:.1f}%** ({disorder_counts.get('No Disorder', 0)}人)")
    
    return "\n".join(insights)


def generate_lifestyle_insight(df):
    """生成生活方式洞察"""
    # 运动与睡眠质量的相关性
    correlation = df['Physical Activity Level (minutes/day)'].corr(df['Quality of Sleep (scale: 1-10)'])
    
    if correlation > 0.3:
        activity_insight = f"🏃 运动与睡眠质量呈**正相关** (相关系数: {correlation:.2f})，增加运动有助于改善睡眠"
    elif correlation < -0.3:
        activity_insight = f"运动与睡眠质量呈负相关 (相关系数: {correlation:.2f})"
    else:
        activity_insight = f"运动与睡眠质量相关性较弱 (相关系数: {correlation:.2f})"
    
    # 压力分析
    avg_stress = df['Stress Level (scale: 1-10)'].mean()
    high_stress_rate = (df['Stress Level (scale: 1-10)'] >= 7).sum() / len(df) * 100
    
    stress_insight = f"😰 平均压力水平为 **{avg_stress:.2f}/10**，{high_stress_rate:.1f}% 的人群处于高压力状态"
    
    return f"{activity_insight}\n\n{stress_insight}"


def generate_risk_insight(df):
    """生成健康风险洞察"""
    # BMI风险
    obese_count = (df['BMI Category'] == 'Obese').sum()
    obese_with_apnea = df[(df['BMI Category'] == 'Obese') & (df['Sleep Disorder'] == 'Sleep Apnea')].shape[0]
    
    if obese_count > 0:
        apnea_in_obese_rate = obese_with_apnea / obese_count * 100
        bmi_insight = f"🚨 肥胖人群中 **{apnea_in_obese_rate:.1f}%** 患有睡眠呼吸暂停"
    else:
        bmi_insight = "数据中无肥胖人群"
    
    # 高血压风险
    high_bp_count = (df['Systolic_BP'] >= 140).sum()
    high_bp_rate = high_bp_count / len(df) * 100
    
    bp_insight = f"💔 **{high_bp_rate:.1f}%** 的人群收缩压≥140mmHg (高血压风险)"
    
    return f"{bmi_insight}\n\n{bp_insight}"


def generate_gender_insight(df):
    """生成性别差异洞察"""
    gender_quality = df.groupby('Gender')['Quality of Sleep (scale: 1-10)'].mean()
    gender_stress = df.groupby('Gender')['Stress Level (scale: 1-10)'].mean()
    
    insights = []
    
    for gender in gender_quality.index:
        quality = gender_quality[gender]
        stress = gender_stress[gender]
        insights.append(f"**{gender}**: 睡眠质量 {quality:.2f}/10, 压力水平 {stress:.2f}/10")
    
    return "\n\n".join(insights)


def get_top_occupation_by_stress(df, top_n=3):
    """获取压力最大的职业"""
    occupation_stress = df.groupby('Occupation')['Stress Level (scale: 1-10)'].mean().sort_values(ascending=False)
    
    top_occupations = []
    for i, (occupation, stress) in enumerate(occupation_stress.head(top_n).items(), 1):
        top_occupations.append(f"{i}. **{occupation}**: {stress:.2f}/10")
    
    return "\n".join(top_occupations)
