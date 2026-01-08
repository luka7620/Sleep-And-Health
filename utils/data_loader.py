"""
数据加载与预处理工具模块
使用缓存优化性能
"""

import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder


@st.cache_data
def load_and_preprocess_data(filepath='sleep_health_lifestyle_dataset.csv'):
    """
    加载并预处理睡眠健康数据集
    
    Args:
        filepath: CSV文件路径
        
    Returns:
        df: 预处理后的原始数据
        df_encoded: 编码后的数据(用于模型分析)
    """
    # 读取数据
    df = pd.read_csv(filepath)
    
    # 删除Person ID列
    df = df.drop('Person ID', axis=1)
    
    # 处理缺失值
    df['Sleep Disorder'] = df['Sleep Disorder'].fillna('No Disorder')
    
    # 拆分血压数据
    df[['Systolic_BP', 'Diastolic_BP']] = df['Blood Pressure (systolic/diastolic)'].str.split('/', expand=True)
    df['Systolic_BP'] = df['Systolic_BP'].astype(int)
    df['Diastolic_BP'] = df['Diastolic_BP'].astype(int)
    df = df.drop('Blood Pressure (systolic/diastolic)', axis=1)
    
    # 创建编码版本的数据副本
    df_encoded = df.copy()
    
    # 对分类变量进行编码
    categorical_cols = ['Gender', 'Occupation', 'BMI Category', 'Sleep Disorder']
    
    for col in categorical_cols:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_encoded[col])
    
    return df, df_encoded


@st.cache_data
def get_summary_stats(df):
    """
    计算关键统计指标
    
    Args:
        df: 数据框
        
    Returns:
        dict: 包含关键指标的字典
    """
    stats = {
        'total_samples': len(df),
        'avg_sleep_quality': df['Quality of Sleep (scale: 1-10)'].mean(),
        'avg_sleep_duration': df['Sleep Duration (hours)'].mean(),
        'disorder_rate': (df['Sleep Disorder'] != 'No Disorder').sum() / len(df) * 100,
        'avg_activity': df['Physical Activity Level (minutes/day)'].mean(),
        'avg_stress': df['Stress Level (scale: 1-10)'].mean(),
        'avg_heart_rate': df['Heart Rate (bpm)'].mean(),
        'avg_systolic_bp': df['Systolic_BP'].mean(),
        'avg_diastolic_bp': df['Diastolic_BP'].mean(),
    }
    
    return stats


@st.cache_data
def filter_data(df, gender=None, occupation=None, age_range=None):
    """
    根据条件筛选数据
    
    Args:
        df: 原始数据框
        gender: 性别筛选 (None表示全部)
        occupation: 职业筛选 (None表示全部)
        age_range: 年龄范围元组 (min, max)
        
    Returns:
        filtered_df: 筛选后的数据框
    """
    filtered_df = df.copy()
    
    if gender and gender != '全部':
        filtered_df = filtered_df[filtered_df['Gender'] == gender]
    
    if occupation and occupation != '全部':
        filtered_df = filtered_df[filtered_df['Occupation'] == occupation]
    
    if age_range:
        filtered_df = filtered_df[
            (filtered_df['Age'] >= age_range[0]) & 
            (filtered_df['Age'] <= age_range[1])
        ]
    
    return filtered_df
