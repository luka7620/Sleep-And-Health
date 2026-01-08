"""
综合睡眠指标页面
展示综合睡眠健康指数 (CSHI) 及其维度分析
"""

import streamlit as st
import pandas as pd
import os

# 页面配置
st.set_page_config(page_title="综合睡眠指标", page_icon="🌟", layout="wide")

# 加载数据
@st.cache_data
def load_cshi_data():
    if os.path.exists('comprehensive_sleep_health_index.csv'):
        return pd.read_csv('comprehensive_sleep_health_index.csv')
    else:
        st.error("未找到综合睡眠健康指数数据文件 (comprehensive_sleep_health_index.csv)")
        return None

df = load_cshi_data()

# 页面标题
st.title("🌟 综合睡眠指标")
st.markdown("基于多维度的综合睡眠健康指数 (CSHI) 分析")
st.markdown("---")

if df is not None:
    # 关键指标
    st.markdown("## 📊 核心指标概览")
    
    col_score1, col_score2, col_score3, col_score4 = st.columns(4)
    
    avg_score = df['CSHI_Score'].mean()
    
    with col_score1:
        st.metric("平均 CSHI 分数", f"{avg_score:.1f}/100")
        
    with col_score2:
        excellent_count = (df['CSHI_Level'] == '优').sum()
        st.metric("优秀等级人数", f"{excellent_count} 人", f"{excellent_count/len(df)*100:.1f}%")

    with col_score3:
        poor_count = (df['CSHI_Level'] == '差').sum()
        st.metric("差等级人数", f"{poor_count} 人", f"{poor_count/len(df)*100:.1f}%", delta_color="inverse")
        
    with col_score4:
        st.metric("评估维度数量", "3 个", "睡眠、心血管、生活方式")

    st.markdown("---")

    # 图表展示
    st.markdown("## 📈 综合指数分析")
    
    col_chart1, col_chart2 = st.columns(2)
    
    # 导入绘制函数
    from cshi_visualization import create_cshi_distribution, create_dimension_radar, create_cshi_comparison_grid
    
    with col_chart1:
        st.markdown("### 📊 CSHI 分数分布")
        fig_dist = create_cshi_distribution(df)
        st.pyplot(fig_dist)
        
        with st.expander("📖 图表说明"):
            st.markdown("""
            - **直方图**: 展示CSHI分数的分布情况
            - **颜色**: 代表不同的评级等级（优、良、一般、差）
            - **解读**: 分数越高代表综合睡眠健康状况越好
            """)

    with col_chart2:
        st.markdown("### 🎯 各等级维度表现雷达图")
        fig_radar = create_dimension_radar(df)
        st.pyplot(fig_radar)

        with st.expander("📖 图表说明"):
            st.markdown("""
            - **雷达图**: 展示不同等级人群在三个维度上的平均得分
            - **维度**: 睡眠维度、心血管维度、生活方式维度
            - **解读**: 优秀人群的图形面积最大，各维度均衡发展
            """)
            
    st.markdown("---")
    
    st.markdown("### 👥 多维度详细对比")
    fig_grid = create_cshi_comparison_grid(df)
    st.pyplot(fig_grid)
        
    with st.expander("📖 图表说明"):
        st.markdown("""
        - **性别对比**: 不同性别的CSHI分数分布差异
        - **年龄对比**: 不同年龄段的CSHI分数变化
        - **职业对比**: 不同职业的平均睡眠健康得分排名
        """)

    st.markdown("---")

    # 原始数据浏览
    st.markdown("## 📋 详细评分数据")
    
    # 筛选器
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        selected_level = st.multiselect(
            "选择评级等级",
            options=df['CSHI_Level'].unique(),
            default=df['CSHI_Level'].unique()
        )
        
    with col_filter2:
        score_range = st.slider(
            "分数范围",
            int(df['CSHI_Score'].min()),
            int(df['CSHI_Score'].max()),
            (int(df['CSHI_Score'].min()), int(df['CSHI_Score'].max()))
        )
        
    # 应用筛选
    df_filtered = df[
        (df['CSHI_Level'].isin(selected_level)) &
        (df['CSHI_Score'] >= score_range[0]) & 
        (df['CSHI_Score'] <= score_range[1])
    ]
    
    st.dataframe(df_filtered, use_container_width=True)
    
    # 下载
    csv = df_filtered.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 下载评分数据 (CSV)",
        data=csv,
        file_name="cshi_scores.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d;'>
        <p>🌟 综合指标提供更全面的健康视角</p>
    </div>
    """, unsafe_allow_html=True)
