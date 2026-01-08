"""
人群差异洞察页面
分析性别、年龄等人群特征对睡眠的影响
"""

import streamlit as st
import pandas as pd
from utils.data_loader import load_and_preprocess_data
from utils.insights import generate_gender_insight

# 页面配置
st.set_page_config(page_title="人群差异洞察", page_icon="👥", layout="wide")

# 加载数据
@st.cache_data
def load_data():
    return load_and_preprocess_data('sleep_health_lifestyle_dataset.csv')

df, df_encoded = load_data()

# 页面标题
st.title("👥 人群差异洞察")
st.markdown("探索不同性别、年龄段人群的睡眠健康特征")
st.markdown("---")

# 人群统计
st.markdown("## 📊 人群统计")

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    male_count = (df['Gender'] == 'Male').sum()
    female_count = (df['Gender'] == 'Female').sum()
    st.metric("男性样本", f"{male_count} 人", f"{male_count/(male_count+female_count)*100:.1f}%")

with col_stat2:
    st.metric("女性样本", f"{female_count} 人", f"{female_count/(male_count+female_count)*100:.1f}%")

with col_stat3:
    avg_age = df['Age'].mean()
    st.metric("平均年龄", f"{avg_age:.1f} 岁")

with col_stat4:
    age_range = df['Age'].max() - df['Age'].min()
    st.metric("年龄跨度", f"{df['Age'].min()}-{df['Age'].max()} 岁")

st.markdown("---")

# 性别差异洞察
st.markdown("## 💡 性别差异洞察")
st.info(generate_gender_insight(df))

st.markdown("---")

# 图表展示
st.markdown("## 📊 数据可视化")

# 第一行：年龄趋势分析
st.markdown("### 📈 年龄趋势分析")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("#### 年龄段睡眠质量变化趋势")
    st.image('outputs/06_age_sleep_quality_line.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **X轴**: 年龄段
        - **Y轴**: 平均睡眠质量（1-10分）
        - **颜色**: 按性别分组
        - **解读**: 可以看到不同年龄段的睡眠质量变化趋势
        - **观察**: 某些年龄段可能存在睡眠质量下降的情况
        """)

with col_chart2:
    st.markdown("#### 年龄与健康轨迹")
    st.image('outputs/24_age_health_trajectory.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - 展示年龄与多个健康指标的关系轨迹
        - 包括睡眠质量、压力水平、运动量等
        - 有助于了解不同年龄段的健康状态变化
        """)

st.markdown("---")

# 第二行：性别与职业压力
st.markdown("### 👔 性别与职业分析")

col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.markdown("#### 职业压力：性别对比")
    st.image('outputs/14_occupation_gender_dual.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **双图模式**: 左图为压力热力图，右图为睡眠质量对比
        - **维度**: 职业 × 性别
        - **解读**: 不同性别在相同职业中的压力和睡眠质量差异
        - **应用**: 识别性别特异性的职业压力模式
        """)

with col_chart4:
    st.markdown("#### 性别压力交互效应")
    st.image('outputs/23_gender_stress_interaction.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - 分析性别与压力水平的交互作用
        - 探索不同性别应对压力的差异
        - 为性别化健康干预提供依据
        """)

st.markdown("---")

# 第三行：运动与健康（性别分组）
st.markdown("### 🏃 运动与健康防御")

col_chart5, col_chart6 = st.columns(2)

with col_chart5:
    st.markdown("#### 运动量与血压（性别分组）")
    st.image('outputs/15_exercise_gender_defense_dual.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **左图**: 不同运动水平下的血压热力图
        - **右图**: 睡眠质量对比
        - **性别分组**: 男性与女性分别展示
        - **解读**: 运动对不同性别健康指标的影响差异
        - **发现**: 运动是重要的健康防御机制
        """)

with col_chart6:
    st.markdown("#### 年龄性别睡眠热力图")
    st.image('outputs/17_age_gender_sleep_heatmap.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **热力图**: 年龄 × 性别的睡眠质量分布
        - **颜色**: 深色表示睡眠质量高，浅色表示质量低
        - **解读**: 快速识别高风险年龄段和性别组合
        - **应用**: 精准定位需要关注的人群
        """)

st.markdown("---")

# 人群特征对比表
st.markdown("## 📋 人群特征对比")

col_table1, col_table2 = st.columns(2)

with col_table1:
    st.markdown("### 性别对比")
    gender_comparison = df.groupby('Gender').agg({
        'Age': 'mean',
        'Quality of Sleep (scale: 1-10)': 'mean',
        'Sleep Duration (hours)': 'mean',
        'Physical Activity Level (minutes/day)': 'mean',
        'Stress Level (scale: 1-10)': 'mean',
        'Heart Rate (bpm)': 'mean'
    }).round(2)
    
    gender_comparison.columns = ['平均年龄', '睡眠质量', '睡眠时长', '运动时长', '压力水平', '心率']
    st.dataframe(gender_comparison, use_container_width=True)

with col_table2:
    st.markdown("### 年龄段对比")
    
    # 创建年龄段
    df_temp = df.copy()
    df_temp['年龄段'] = pd.cut(df_temp['Age'], bins=[20, 30, 40, 50, 60], 
                              labels=['20-29岁', '30-39岁', '40-49岁', '50-59岁'])
    
    age_comparison = df_temp.groupby('年龄段').agg({
        'Quality of Sleep (scale: 1-10)': 'mean',
        'Sleep Duration (hours)': 'mean',
        'Physical Activity Level (minutes/day)': 'mean',
        'Stress Level (scale: 1-10)': 'mean'
    }).round(2)
    
    age_comparison.columns = ['睡眠质量', '睡眠时长', '运动时长', '压力水平']
    st.dataframe(age_comparison, use_container_width=True)

st.markdown("---")

# 关键发现
st.markdown("## 🔍 关键发现")

col_finding1, col_finding2 = st.columns(2)

with col_finding1:
    st.success("""
    ### ✅ 积极发现
    
    - 适当运动对所有人群均有益
    - 某些年龄段睡眠质量表现优秀
    - 健康意识提升带来正面效果
    """)

with col_finding2:
    st.warning("""
    ### ⚠️ 需要关注
    
    - 特定性别在某些职业压力更大
    - 年龄增长可能影响睡眠质量
    - 需要针对性别和年龄制定干预方案
    """)

st.markdown("---")

# 数据下载
st.markdown("## 📥 数据导出")

demographic_data = df[['Gender', 'Age', 'Occupation', 
                        'Quality of Sleep (scale: 1-10)', 'Sleep Duration (hours)',
                        'Physical Activity Level (minutes/day)', 'Stress Level (scale: 1-10)']].copy()

csv = demographic_data.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📊 下载人群差异数据 (CSV)",
    data=csv,
    file_name="demographic_insights.csv",
    mime="text/csv"
)

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>🧬 了解人群差异，实现精准健康管理</p>
</div>
""", unsafe_allow_html=True)
