"""
生活方式分析页面
分析运动、职业压力与睡眠的关系
"""

import streamlit as st
from utils.data_loader import load_and_preprocess_data, filter_data
from utils.insights import get_top_occupation_by_stress

# 页面配置
st.set_page_config(page_title="生活方式分析", page_icon="🏃", layout="wide")

# 加载数据
@st.cache_data
def load_data():
    return load_and_preprocess_data('sleep_health_lifestyle_dataset.csv')

df, df_encoded = load_data()

# 页面标题
st.title("🏃 生活方式分析")
st.markdown("探索运动、职业压力与睡眠质量之间的关系")
st.markdown("---")

# 侧边栏筛选
st.sidebar.header("数据筛选")
occupation_filter = st.sidebar.multiselect(
    "选择职业类型",
    options=sorted(df['Occupation'].unique()),
    default=[]
)

if occupation_filter:
    df_display = df[df['Occupation'].isin(occupation_filter)]
else:
    df_display = df

st.sidebar.markdown(f"**当前样本数**: {len(df_display)} 条")

# 核心洞察
st.markdown("## 💡 核心洞察")

col1, col2 = st.columns(2)

with col1:
    st.info(f"""
    ### 运动与睡眠
    
    平均运动时长: **{df_display['Physical Activity Level (minutes/day)'].mean():.0f}** 分钟/天
    
    相关性系数: **{df_display['Physical Activity Level (minutes/day)'].corr(df_display['Quality of Sleep (scale: 1-10)']):.3f}**
    
    运动量越高，睡眠质量通常越好 ✅
    """)

with col2:
    st.warning(f"""
    ### 压力最大职业 TOP 3
    
    {get_top_occupation_by_stress(df_display, top_n=3)}
    
    职业压力是影响睡眠的重要因素 ⚠️
    """)

st.markdown("---")

# 图表展示
st.markdown("## 📊 数据可视化")

# 第一行：运动与睡眠 + 职业压力
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("### 🏃‍♂️ 运动与睡眠质量回归分析")
    st.image('outputs/02_activity_sleep_regression.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **X轴**: 每日运动时长（分钟）
        - **Y轴**: 睡眠质量评分（1-10分）
        - **蓝色线**: 回归趋势线
        - **解读**: 散点图显示运动量与睡眠质量的正相关关系，运动时长越长，睡眠质量倾向越高
        """)

with col_chart2:
    st.markdown("### 📦 职业压力分布箱线图")
    st.image('outputs/03_occupation_stress_boxplot.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **X轴**: 不同职业类型
        - **Y轴**: 压力水平（1-10分）
        - **颜色**: 按性别分组
        - **解读**: 图中可以看到不同职业的压力分布差异
        """)

st.markdown("---")

# 第二行：运动分段 + 职业健康指标
col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.markdown("### 📈 运动量分段分析")
    st.image('outputs/08_activity_segments_line.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - 将运动量分为不同区间段
        - 对比各区间段的睡眠质量、压力水平等指标
        - 解读：有助于找到最佳运动量区间
        """)

with col_chart4:
    st.markdown("### 🎯 职业健康指标综合对比")
    st.image('outputs/12_occupation_horizontal_bars.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - 横向条形图展示不同职业的多维度健康指标
        - 包括睡眠质量、运动水平、压力状况
        - 便于快速识别各职业的健康状况
        """)

st.markdown("---")

# 第三行：压力趋势 + 步数分布
col_chart5, col_chart6 = st.columns(2)

with col_chart5:
    st.markdown("### 😰 压力与睡眠质量趋势")
    st.image('outputs/18_stress_sleep_quality_line.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - 展示不同压力水平下的睡眠质量变化
        - 通常呈现负相关：压力越大，睡眠质量越差
        - 有助于识别压力管理的重要性
        """)

with col_chart6:
    st.markdown("### 👣 每日步数职业分布")
    st.image('outputs/19_steps_occupation_facet.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - 分面图展示不同职业的每日步数分布
        - 可以看出职业性质对日常活动量的影响
        """)

st.markdown("---")

# 数据下载功能
st.markdown("## 📥 数据导出")

col_download1, col_download2 = st.columns(2)

with col_download1:
    # 生活方式相关数据
    lifestyle_data = df_display[['Occupation', 'Physical Activity Level (minutes/day)', 
                                  'Stress Level (scale: 1-10)', 'Quality of Sleep (scale: 1-10)',
                                  'Daily Steps']].copy()
    
    csv = lifestyle_data.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📊 下载生活方式数据 (CSV)",
        data=csv,
        file_name="lifestyle_analysis.csv",
        mime="text/csv"
    )

with col_download2:
    st.info("💡 **提示**: 下载的数据可以用于进一步分析或制作自定义报告")

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>💪 改善生活方式，从了解数据开始</p>
</div>
""", unsafe_allow_html=True)
