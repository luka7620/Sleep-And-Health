"""
深度探索页面
睡眠障碍深度分析与原始数据展示
"""

import streamlit as st
import pandas as pd
from utils.data_loader import load_and_preprocess_data

# 页面配置
st.set_page_config(page_title="深度探索", page_icon="🔬", layout="wide")

# 加载数据
@st.cache_data
def load_data():
    return load_and_preprocess_data('sleep_health_lifestyle_dataset.csv')

df, df_encoded = load_data()

# 页面标题
st.title("🔬 深度探索")
st.markdown("睡眠障碍深度分析与原始数据探索")
st.markdown("---")

# 睡眠障碍统计
st.markdown("## 📊 睡眠障碍统计")

disorder_counts = df['Sleep Disorder'].value_counts()

col_disorder1, col_disorder2, col_disorder3 = st.columns(3)

with col_disorder1:
    no_disorder = disorder_counts.get('No Disorder', 0)
    no_disorder_rate = no_disorder / len(df) * 100
    st.metric("健康人群", f"{no_disorder} 人", f"{no_disorder_rate:.1f}%", delta_color="normal")

with col_disorder2:
    insomnia = disorder_counts.get('Insomnia', 0)
    insomnia_rate = insomnia / len(df) * 100
    st.metric("失眠症", f"{insomnia} 人", f"{insomnia_rate:.1f}%", delta_color="inverse")

with col_disorder3:
    apnea = disorder_counts.get('Sleep Apnea', 0)
    apnea_rate = apnea / len(df) * 100
    st.metric("睡眠呼吸暂停", f"{apnea} 人", f"{apnea_rate:.1f}%", delta_color="inverse")

st.markdown("---")

# 图表展示
st.markdown("## 📊 睡眠障碍深度分析")

# 第一行：障碍对比与分布
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("### 📈 睡眠障碍多维对比")
    st.image('outputs/07_disorder_comparison_line.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - 对比不同睡眠障碍类型在多个健康指标上的差异
        - 包括年龄、BMI、心率、血压等
        - 折线图展示各障碍类型的特征轮廓
        - 有助于识别不同障碍的致病因素
        """)

with col_chart2:
    st.markdown("### 📊 睡眠障碍分布面积图")
    st.image('outputs/11_disorder_area.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - 按性别展示睡眠障碍的分布情况
        - 面积图可以直观看出各类障碍的人数占比
        - 有助于识别性别与睡眠障碍的关系
        """)

st.markdown("---")

# 第二行：职业雷达图与障碍画像
col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.markdown("### 🎯 职业多维度雷达图")
    st.image('outputs/09_occupation_radar.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **雷达图**: 展示不同职业在多个健康维度的表现
        - **维度**: 运动量、睡眠质量、压力水平、心率等
        - **应用**: 快速识别各职业的健康优势和劣势
        - **对比**: 多个职业的雷达图叠加对比
        """)

with col_chart4:
    st.markdown("### 🧬 睡眠障碍人群画像雷达")
    st.image('outputs/22_disorder_radar_profile.png', use_container_width=True)
    
    with st.expander("📖 图表说明"):
        st.markdown("""
        - 为每种睡眠障碍类型绘制人群画像
        - 包括年龄、BMI、运动量、压力等特征
        - 便于理解不同障碍人群的典型特征
        - 为精准干预提供依据
        """)

st.markdown("---")

# 原始数据展示
st.markdown("## 📋 原始数据浏览")

# 数据筛选选项
col_filter1, col_filter2, col_filter3 = st.columns(3)

with col_filter1:
    selected_disorder = st.selectbox(
        "睡眠障碍筛选",
        ['全部'] + list(df['Sleep Disorder'].unique())
    )

with col_filter2:
    selected_gender = st.selectbox(
        "性别筛选",
        ['全部'] + list(df['Gender'].unique())
    )

with col_filter3:
    selected_bmi = st.selectbox(
        "BMI类别筛选",
        ['全部'] + list(df['BMI Category'].unique())
    )

# 应用筛选
df_filtered = df.copy()

if selected_disorder != '全部':
    df_filtered = df_filtered[df_filtered['Sleep Disorder'] == selected_disorder]

if selected_gender != '全部':
    df_filtered = df_filtered[df_filtered['Gender'] == selected_gender]

if selected_bmi != '全部':
    df_filtered = df_filtered[df_filtered['BMI Category'] == selected_bmi]

st.markdown(f"**筛选后样本数**: {len(df_filtered)} 条")

# 显示数据表
st.dataframe(
    df_filtered.head(100),
    use_container_width=True,
    height=400
)

st.caption("💡 提示: 显示前100条数据，可使用下方下载按钮获取完整数据")

st.markdown("---")

# 数据统计摘要
st.markdown("## 📊 数据统计摘要")

tab1, tab2, tab3 = st.tabs(["描述性统计", "分类变量分布", "相关性分析"])

with tab1:
    st.markdown("### 数值型变量描述性统计")
    numeric_cols = df_filtered.select_dtypes(include=['int64', 'float64']).columns
    st.dataframe(df_filtered[numeric_cols].describe().round(2), use_container_width=True)

with tab2:
    st.markdown("### 分类变量分布")
    
    col_cat1, col_cat2 = st.columns(2)
    
    with col_cat1:
        st.markdown("#### 性别分布")
        st.bar_chart(df_filtered['Gender'].value_counts())
        
        st.markdown("#### BMI类别分布")
        st.bar_chart(df_filtered['BMI Category'].value_counts())
    
    with col_cat2:
        st.markdown("#### 睡眠障碍分布")
        st.bar_chart(df_filtered['Sleep Disorder'].value_counts())
        
        st.markdown("#### 职业分布")
        st.bar_chart(df_filtered['Occupation'].value_counts())

with tab3:
    st.markdown("### Top 10 相关性对")
    
    # 计算相关性矩阵
    corr_matrix = df_encoded.corr()
    
    # 提取上三角（避免重复）
    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_pairs.append({
                '变量1': corr_matrix.columns[i],
                '变量2': corr_matrix.columns[j],
                '相关系数': corr_matrix.iloc[i, j]
            })
    
    # 转换为DataFrame并排序
    corr_df = pd.DataFrame(corr_pairs)
    corr_df = corr_df.reindex(corr_df['相关系数'].abs().sort_values(ascending=False).index)
    
    st.dataframe(corr_df.head(10).round(3), use_container_width=True)

st.markdown("---")

# 数据下载功能
st.markdown("## 📥 数据导出")

col_download1, col_download2, col_download3 = st.columns(3)

with col_download1:
    # CSV下载
    csv = df_filtered.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📊 下载筛选数据 (CSV)",
        data=csv,
        file_name="sleep_health_filtered.csv",
        mime="text/csv"
    )

with col_download2:
    # Excel下载（需要转换）
    import io
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_filtered.to_excel(writer, index=False, sheet_name='睡眠健康数据')
    
    st.download_button(
        label="📊 下载筛选数据 (Excel)",
        data=buffer.getvalue(),
        file_name="sleep_health_filtered.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col_download3:
    # 统计摘要下载
    stats_summary = df_filtered.describe().round(2)
    csv_stats = stats_summary.to_csv().encode('utf-8-sig')
    st.download_button(
        label="📊 下载统计摘要 (CSV)",
        data=csv_stats,
        file_name="statistics_summary.csv",
        mime="text/csv"
    )

st.markdown("---")

# 探索建议
st.markdown("## 💡 探索建议")

col_suggest1, col_suggest2 = st.columns(2)

with col_suggest1:
    st.info("""
    ### 🔍 数据探索方向
    
    1. **异常值检测**: 筛选极端数值，识别特殊案例
    2. **群体细分**: 按多个维度组合筛选，发现小众群体特征
    3. **趋势分析**: 观察年龄、BMI等连续变量的变化趋势
    4. **因果推断**: 探索变量间的因果关系（需要严谨的统计方法）
    """)

with col_suggest2:
    st.success("""
    ### 📚 进一步研究
    
    1. **机器学习建模**: 构建睡眠质量预测模型
    2. **聚类分析**: 对人群进行无监督聚类
    3. **时间序列**: 如有时间数据，分析睡眠变化轨迹
    4. **干预实验**: 设计实验验证改善睡眠的方法
    """)

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>🔬 数据探索无止境，保持好奇心</p>
</div>
""", unsafe_allow_html=True)
