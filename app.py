"""
睡眠健康数据分析仪表板 - 主页
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from utils.data_loader import load_and_preprocess_data, get_summary_stats, filter_data
from utils.insights import (
    generate_sleep_quality_insight,
    generate_disorder_insight,
    generate_lifestyle_insight
)

# 页面配置
st.set_page_config(
    page_title="睡眠健康分析仪表板",
    page_icon="😴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
        color: #3498db;
    }
    .main-title {
        text-align: center;
        color: #2c3e50;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# 加载数据
@st.cache_data
def load_data():
    return load_and_preprocess_data('sleep_health_lifestyle_dataset.csv')

df, df_encoded = load_data()

# 标题
st.markdown('<p class="main-title">😴 睡眠健康数据分析仪表板</p>', unsafe_allow_html=True)

# ========== 侧边栏 ==========
st.sidebar.header("📊 数据仪表板")
st.sidebar.markdown("---")

# 数据集信息
st.sidebar.subheader("数据集信息")
st.sidebar.info(f"""
- **样本数量**: {len(df)} 条记录
- **特征数量**: {df.shape[1]} 个字段
- **数据来源**: 睡眠健康与生活方式数据集
""")

st.sidebar.markdown("---")

# 全局筛选器
st.sidebar.subheader("🔍 数据筛选")

gender_filter = st.sidebar.selectbox(
    "性别筛选",
    ['全部'] + list(df['Gender'].unique())
)

occupation_filter = st.sidebar.selectbox(
    "职业筛选",
    ['全部'] + sorted(df['Occupation'].unique())
)

age_range = st.sidebar.slider(
    "年龄范围",
    int(df['Age'].min()),
    int(df['Age'].max()),
    (int(df['Age'].min()), int(df['Age'].max()))
)

# 应用筛选
df_filtered = filter_data(
    df,
    gender=gender_filter if gender_filter != '全部' else None,
    occupation=occupation_filter if occupation_filter != '全部' else None,
    age_range=age_range
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**筛选后样本数**: {len(df_filtered)} 条")

# ========== 主内容区域 ==========

# 关键指标卡片
st.markdown("## 📈 关键指标")
stats = get_summary_stats(df_filtered)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="平均睡眠质量",
        value=f"{stats['avg_sleep_quality']:.2f}/10",
        delta=f"{stats['avg_sleep_quality'] - 7:.2f} vs 良好标准(7分)"
    )

with col2:
    st.metric(
        label="睡眠障碍比例",
        value=f"{stats['disorder_rate']:.1f}%",
        delta=f"{stats['disorder_rate'] - 50:.1f}%" if stats['disorder_rate'] > 50 else None,
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="平均运动时长",
        value=f"{stats['avg_activity']:.0f} 分钟/天",
        delta=f"{stats['avg_activity'] - 60:.0f} vs 建议(60分钟)"
    )

with col4:
    st.metric(
        label="平均压力水平",
        value=f"{stats['avg_stress']:.2f}/10",
        delta=f"{stats['avg_stress'] - 5:.2f} vs 中等水平(5分)",
        delta_color="inverse"
    )

st.markdown("---")

# 数据洞察
st.markdown("## 💡 数据洞察")

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.markdown("### 睡眠质量评估")
    st.info(generate_sleep_quality_insight(df_filtered))
    
    st.markdown("### 睡眠障碍分布")
    st.warning(generate_disorder_insight(df_filtered))

with col_insight2:
    st.markdown("### 生活方式分析")
    st.success(generate_lifestyle_insight(df_filtered))

st.markdown("---")

# 核心图表展示
st.markdown("## 📊 核心分析图表")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("### 🗺️ 特征相关性热力图")
    st.image('outputs/01_correlation_heatmap.png', use_container_width=True)
    st.caption("展示各健康指标之间的相关性关系，颜色越深表示相关性越强")

with col_chart2:
    st.markdown("### 🎯 特征重要性分析")
    st.image('outputs/05_feature_importance.png', use_container_width=True)
    st.caption("基于随机森林模型分析各因素对睡眠质量的影响权重")

st.markdown("---")

# 快速导航
st.markdown("## 🧭 页面导航")

nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

with nav_col1:
    st.info("**🏃 生活方式分析**\n\n分析运动、职业压力与睡眠的关系")

with nav_col2:
    st.warning("**💔 健康风险评估**\n\nBMI、血压、心率等健康风险")

with nav_col3:
    st.success("**🌟 综合睡眠指标**\n\n综合评分、维度分析与详细数据")

with nav_col4:
    st.error("**🔬 深度探索**\n\n睡眠障碍深度分析与数据清洗报告")

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>睡眠健康数据分析仪表板 | 数据驱动的健康洞察</p>
    <p>使用左侧导航栏探索更多专题分析 👈</p>
</div>
""", unsafe_allow_html=True)
