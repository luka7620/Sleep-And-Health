# 加权健康分数算法说明文档

## 📋 算法概述

本算法基于**职业分类**的个性化健康评分系统,综合评估6个核心健康维度:
- 活动步数
- 活动时间
- BMI分类
- 压力水平
- 睡眠时长
- 睡眠质量

**输出**: 0-100分的健康分数 + 健康等级(优秀/良好/中等/较差/差)

---

## 🎯 核心指标与权重

### 基础权重分配

| 指标 | 基础权重 | 说明 |
|------|---------|------|
| 活动步数 | 15% | 日常活动量 |
| 活动时间 | 15% | 运动时长 |
| BMI分类 | 20% | 体重管理 |
| 压力水平 | 15% | 心理健康 |
| 睡眠时长 | 20% | 睡眠充足度 |
| 睡眠质量 | 15% | 睡眠效果 |

### 职业权重调整

不同职业对各指标的权重进行微调:

**Office Worker (久坐型)**
- 活动步数 +5% ⬆️ (需要更多活动)
- 活动时间 +5% ⬆️
- 压力水平 +5% ⬆️ (工作压力大)

**Manual Labor (体力型)**
- 活动步数 -3% (已有足够活动)
- 活动时间 -3%
- BMI +5% ⬆️ (体重管理重要)
- 睡眠时长 +5% ⬆️ (需要充足恢复)

**Student (学习型)**
- 压力水平 +5% ⬆️ (学习压力)
- 睡眠质量 +5% ⬆️ (睡眠质量很重要)

**Retired (退休型)**
- 压力水平 -5% (压力较小)
- BMI +3% ⬆️
- 适度运动即可

---

## 📊 评分标准

### 1. 活动步数评分

| 步数范围 | 得分 | 评价 |
|---------|------|------|
| ≥10000步 | 100分 | 优秀 |
| 7000-9999步 | 80-99分 | 良好 |
| 5000-6999步 | 60-79分 | 一般 |
| 3000-4999步 | 40-59分 | 不足 |
| <3000步 | 20-39分 | 较差 |

### 2. 活动时间评分

| 时长范围 | 得分 | 评价 |
|---------|------|------|
| 60-90分钟 | 100分 | 理想 |
| 30-59分钟 | 80-99分 | 良好 |
| 15-29分钟 | 60-79分 | 一般 |
| <15分钟 | 40分 | 不足 |
| >90分钟 | 70-100分 | 根据职业调整 |

### 3. BMI分类评分

| BMI分类 | 得分 |
|---------|------|
| Normal | 100分 |
| Overweight | 70分 |
| Underweight | 70分 |
| Obese | 40分 |

### 4. 压力水平评分

| 压力等级 | 得分 | 评价 |
|---------|------|------|
| 3-5分 | 100分 | 适度压力 |
| 6-7分 | 70分 | 中等压力 |
| 1-2分 | 60分 | 压力过低 |
| 8分 | 40分 | 高压力 |
| 9分 | 35分 | 很高压力 |
| 10分 | 30分 | 极高压力 |

### 5. 睡眠时长评分

| 睡眠时长 | 得分 | 评价 |
|---------|------|------|
| 7-9小时 | 100分 | 理想 |
| 6-7小时 | 80分 | 良好 |
| 9-10小时 | 85分 | 稍长 |
| 5-6小时 | 60分 | 不足 |
| <5小时 | 30分 | 严重不足 |
| >10小时 | 50分 | 过度睡眠 |

### 6. 睡眠质量评分

| 质量分数 | 得分 | 评价 |
|---------|------|------|
| 8-10分 | 100分 | 高质量 |
| 6-7分 | 70-85分 | 良好 |
| 4-5分 | 50-65分 | 一般 |
| 1-3分 | 20-45分 | 较差 |

---

## 🧮 计算公式

```python
# 步骤1: 计算各指标单项得分 (0-100分)
score_steps = calculate_steps_score(daily_steps)
score_activity = calculate_activity_score(activity_minutes)
score_bmi = calculate_bmi_score(bmi_category)
score_stress = calculate_stress_score(stress_level)
score_sleep_duration = calculate_sleep_duration_score(sleep_hours)
score_sleep_quality = calculate_sleep_quality_score(quality_score)

# 步骤2: 根据职业获取调整后的权重
weights = get_occupation_weights(occupation)

# 步骤3: 加权求和
health_score = (
    score_steps * weights['steps'] +
    score_activity * weights['activity'] +
    score_bmi * weights['bmi'] +
    score_stress * weights['stress'] +
    score_sleep_duration * weights['sleep_duration'] +
    score_sleep_quality * weights['sleep_quality']
)

# 步骤4: 四舍五入到小数点后1位
final_score = round(health_score, 1)
```

---

## 🏆 健康等级划分

| 分数区间 | 等级 | 星级 | 评价 |
|---------|------|------|------|
| 85-100分 | 优秀 | ⭐⭐⭐⭐⭐ | 健康状况极佳 |
| 70-84分 | 良好 | ⭐⭐⭐⭐ | 健康状况良好 |
| 55-69分 | 中等 | ⭐⭐⭐ | 需要改善 |
| 40-54分 | 较差 | ⭐⭐ | 存在健康风险 |
| <40分 | 差 | ⭐ | 需要重点关注 |

---

## 📁 使用方法

### 1. 计算健康分数

```bash
python health_score_calculator.py
```

**输入**: `sleep_health_lifestyle_dataset_cleaned.csv`  
**输出**: `sleep_health_lifestyle_dataset_with_scores.csv`

输出文件包含:
- 原始数据的所有字段
- `Health_Score`: 健康总分
- `Health_Level`: 健康等级
- `Score_*`: 各指标单项得分
- `Weight_*`: 各指标实际权重

### 2. 生成可视化图表

```bash
python health_score_visualization.py
```

**生成图表**:
1. `health_score_distribution.png` - 健康分数分布分析
2. `health_score_components.png` - 各指标得分分析
3. `health_score_weights_heatmap.png` - 职业权重热力图
4. `health_score_correlation.png` - 相关性分析

---

## 💡 算法特点

✅ **个性化**: 根据职业特征调整权重  
✅ **科学性**: 基于WHO和医学标准  
✅ **全面性**: 覆盖运动、BMI、压力、睡眠4大维度  
✅ **可解释**: 每个指标都有明确的评分逻辑  
✅ **实用性**: 可直接应用于实际数据集

---

## 📈 应用场景

1. **个人健康评估**: 综合评估个人健康状况
2. **职业健康管理**: 针对不同职业提供定制化建议
3. **健康趋势分析**: 追踪健康分数变化趋势
4. **风险预警**: 识别健康风险人群
5. **健康干预**: 为改善措施提供数据支持

---

## 🔧 技术实现

- **语言**: Python 3.x
- **核心库**: pandas, numpy
- **可视化**: matplotlib, seaborn
- **数据源**: 清洗后的睡眠健康数据集

---

## 📝 注意事项

1. 算法基于统计数据和医学标准,仅供参考
2. 不同职业的权重调整基于一般性假设,可根据实际需求调整
3. 建议结合专业医疗建议使用
4. 分数仅反映当前状态,需持续监测

---

**版本**: 1.0  
**创建日期**: 2026-01-08  
**作者**: Health Score Calculator System
