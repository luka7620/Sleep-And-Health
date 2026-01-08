"""
健康风险评估页面
分析BMI、血压、心率等健康风险指标
"""

import streamlit as st
from utils.data_loader import load_and_preprocess_data
from utils.insights import generate_risk_insight

# 页面配置
st.set_page_config(page_title="健康风险评估", page_icon="💔", layout="wide")

# 加载数据
@st.cache_data
def load_data():
    return load_and_preprocess_data('sleep_health_lifestyle_dataset.csv')

df, df_encoded = load_data()

# 页面标题
st.title("💔 健康风险评估")
st.markdown("深入分析BMI、血压、心率等健康风险因素与睡眠的关系")
st.markdown("---")

# 风险警报
st.markdown("## 🚨 风险警报")

col_alert1, col_alert2, col_alert3 = st.columns(3)

with col_alert1:
    obese_count = (df['BMI Category'] == 'Obese').sum()
    obese_rate = obese_count / len(df) * 100
    st.metric("肥胖人群", f"{obese_count} 人", f"{obese_rate:.1f}%")

with col_alert2:
    high_bp_count = (df['Systolic_BP'] >= 140).sum()
    high_bp_rate = high_bp_count / len(df) * 100
    st.metric("高血压风险", f"{high_bp_count} 人", f"{high_bp_rate:.1f}%", delta_color="inverse")

with col_alert3:
    high_hr_count = (df['Heart Rate (bpm)'] >= 100).sum()
    high_hr_rate = high_hr_count / len(df) * 100
    st.metric("心率过快", f"{high_hr_count} 人", f"{high_hr_rate:.1f}%", delta_color="inverse")

st.markdown("---")

# 核心洞察
st.markdown("## 💡 核心洞察")
st.error(generate_risk_insight(df))

st.markdown("---")

# 图表展示
st.markdown("## 📊 数据可视化")

# 第一行：BMI相关分析
st.markdown("### 🏋️ BMI 与睡眠障碍")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("#### BMI类别与睡眠障碍分布")
    st.image('outputs/04_bmi_disorder_countplot.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **X轴**: BMI类别（消瘦、正常、超重、肥胖）
        - **颜色**: 按睡眠障碍类型分组
        - **解读**: 肥胖人群中睡眠呼吸暂停（Sleep Apnea）发病率显著升高
        - **建议**: 控制体重可有效降低睡眠障碍风险
        """)

with col_chart2:
    st.markdown("#### BMI类别与睡眠时长分布")
    st.image('outputs/10_bmi_sleep_violin.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **小提琴图**: 展示各BMI类别下睡眠时长的概率密度分布
        - **颜色**: 按性别分组
        - **解读**: 可以看到不同BMI类别人群的睡眠时长分布特征
        - **宽度**: 表示该睡眠时长的人数多少
        """)

st.markdown("---")

# 第二行：心率与压力
st.markdown("### ❤️ 心率与压力分析")

col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.markdown("#### 心率与压力散点图")
    st.image('outputs/13_heartrate_stress_scatter.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **X轴**: 心率（bpm）
        - **Y轴**: 压力水平（1-10分）
        - **解读**: 探索心率与压力水平的关系
        - **观察**: 心率较快的人群往往伴随较高的压力水平
        """)

with col_chart4:
    st.markdown("#### 心率压力核密度估计")
    st.image('outputs/20_heartrate_stress_kde.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **KDE图**: 核密度估计，平滑展示数据分布
        - **解读**: 显示心率和压力的联合概率分布
        - **应用**: 识别高风险人群聚集区域
        """)

st.markdown("---")

# 第三行：综合健康分析
st.markdown("### 🔍 综合健康风险")

col_chart5, col_chart6 = st.columns(2)

with col_chart5:
    st.markdown("#### BMI、心率、压力综合分析")
    st.image('outputs/16_bmi_heart_stress_dual.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **双图模式**: 同时展示多个健康指标的关系
        - **左图**: BMI与心率的热力图
        - **右图**: 压力水平与睡眠质量对比
        - **解读**: 提供多维度的健康风险视角
        """)

with col_chart6:
    st.markdown("#### 高血压风险矩阵")
    st.image('outputs/21_hypertension_risk_matrix.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **矩阵图**: 收缩压与舒张压的联合分布
        - **风险区域**: 右上角为高风险区域（收缩压≥140, 舒张压≥90）
        - **临床意义**: 直观识别高血压患者
        - **预防**: 及早干预可降低心血管疾病风险
        """)

st.markdown("---")

# 风险评估建议
st.markdown("## 📋 健康建议")

col_advice1, col_advice2, col_advice3 = st.columns(3)

with col_advice1:
    st.info("""
    ### 🏋️ BMI管理
    
    - 保持健康体重
    - 均衡饮食
    - 定期运动
    - 避免过度肥胖
    """)

with col_advice2:
    st.success("""
    ### 💊 血压控制
    
    - 减少盐分摄入
    - 规律作息
    - 压力管理
    - 定期监测
    """)

with col_advice3:
    st.warning("""
    ### ❤️ 心率调节
    
    - 有氧运动
    - 深呼吸练习
    - 避免过度饮咖啡
    - 保证充足睡眠
    """)

st.markdown("---")

# 数据下载
st.markdown("## 📥 数据导出")

health_data = df[['Gender', 'Age', 'BMI Category', 'Systolic_BP', 'Diastolic_BP', 
                   'Heart Rate (bpm)', 'Sleep Disorder', 'Quality of Sleep (scale: 1-10)']].copy()

csv = health_data.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📊 下载健康风险数据 (CSV)",
    data=csv,
    file_name="health_risk_assessment.csv",
    mime="text/csv"
)

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>⚕️ 预防胜于治疗，定期健康检查很重要</p>
</div>
""", unsafe_allow_html=True)
