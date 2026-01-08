# 三、算法设计与实现

## 1. 数据预处理 (Data Preprocessing)

数据预处理是保证分析结果准确性的基础。本项目针对 `sleep_health_lifestyle_dataset.csv` 原始数据集，设计了一套包含数据备份、质量标记、异常检测和分层输出的清洗流程（详见 `data_cleaning.py`）。

### 1.1 异常检测规则
采用了基于领域知识的逻辑规则来识别潜在的数据异常：

*   **年龄与职业逻辑校验**：
    *   **规则 1.2**：若年龄 < 30 岁且职业为 "Retired"（退休），标记为异常（`AGE_OCCUPATION_1.2`）。
    *   **规则 1.3**：若年龄 ≥ 70 岁且职业为 "Student"（学生），标记为异常（`AGE_OCCUPATION_1.3`）。
*   **心理压力与睡眠质量一致性校验**：
    *   **规则 6.1**：若压力水平 ≥ 9（满分10）但睡眠质量评分 ≥ 8，视为严重矛盾，标记为异常（`STRESS_SLEEP_6.1`）。
    *   **规则 6.2**：若压力水平 ≤ 2 但睡眠质量评分 ≤ 4，标记为异常（`STRESS_SLEEP_6.2`）。
*   **运动数据逻辑校验**：
    *   **规则 9.1**：若日步数 ≥ 18,000 步但高强度运动时长 ≤ 30 分钟，数据存疑，标记为异常（`STEPS_ACTIVITY_9.1`）。

### 1.2 核心代码实现
```python
# 异常检测逻辑实现 (data_cleaning.py)

# 1. 年龄与职业逻辑校验
condition_1_2 = (df['Age'] < 30) & (df['Occupation'] == 'Retired')
condition_1_3 = (df['Age'] >= 70) & (df['Occupation'] == 'Student')

# 2. 心理压力与睡眠质量一致性校验
condition_6_1 = (df['Stress Level (scale: 1-10)'] >= 9) & \
                (df['Quality of Sleep (scale: 1-10)'] >= 8) & \
                (df['Data_Quality_Flag'] == 'Normal')
                
condition_6_2 = (df['Stress Level (scale: 1-10)'] <= 2) & \
                (df['Quality of Sleep (scale: 1-10)'] <= 4) & \
                (df['Data_Quality_Flag'] == 'Normal')

# 3. 运动数据逻辑校验
condition_9_1 = (df['Daily Steps'] >= 18000) & \
                (df['Physical Activity Level (minutes/day)'] <= 30) & \
                (df['Data_Quality_Flag'] == 'Normal')
```

### 1.2 清洗输出
经过清洗流程后，系统生成了三分数据集以满足不同分析需求：
1.  `sleep_health_lifestyle_dataset_cleaned.csv`: 仅包含标记为 `Normal` 的高质量数据，用于核心算法建模。
2.  `sleep_health_lifestyle_dataset_anomalies.csv`: 仅包含异常数据，用于错误分析。
3.  `sleep_health_lifestyle_dataset_full_annotated.csv`: 包含所有原始数据及新增的质量标记列。

---

## 2. 生活方式分析 (Lifestyle Analysis)

为了量化不同生活方式对健康的影响，设计了**加权健康分数计算器**（`health_score_calculator.py`），该算法基于职业特性对各个健康因子进行动态加权。

### 2.1 核心评分因子
算法考察了六大维度的健康指标，并设定了基础权重：
*   **BMI分类 (20%)**: 基于 Normal, Overweight, Obese 等分类评分。
*   **睡眠时长 (20%)**: 7-9小时为最优区间 (100分)。
*   **活动步数 (15%)**: >10,000步为满分。
*   **活动时间 (15%)**: 60-90分钟为最佳区间。
*   **压力水平 (15%)**: 3-5分视为适度压力 (100分)。
*   **睡眠质量 (15%)**: 主观评分 8-10分视为高质量。

### 2.2 职业自适应权重调整
算法引入了职业调整系数，以反映不同职业群体的健康需求差异：
*   **Office Worker (久坐族)**: 增加**步数** (+5%) 和**活动时间** (+5%) 的权重，强调运动的重要性；增加**压力** (+5%) 权重。
*   **Manual Labor (体力劳动者)**: 降低运动类权重 (-3%)，增加**BMI** (+5%) 和**睡眠时长** (+5%) 权重，强调恢复和体重管理。
*   **Student (学生)**: 增加**睡眠质量** (+5%) 和**压力** (+5%) 权重，反映学业压力下的睡眠需求。
*   **Retired (退休人员)**: 降低压力权重 (-5%)，增加**步数** (+3%) 和**BMI** (+3%) 权重，关注基础代谢健康。

最终得出的 `Health_Score` (0-100) 将人群划分为优秀、良好、中等、较差、差五个等级。

### 2.3 核心代码实现
```python
# 加权健康分数计算逻辑 (health_score_calculator.py)

class HealthScoreCalculator:
    def __init__(self):
        # 职业权重调整字典
        self.occupation_adjustments = {
            'Office Worker': {
                'steps': +0.05, 'activity': +0.05, 'stress': +0.05,
                'bmi': 0.00, 'sleep_duration': +0.02, 'sleep_quality': +0.03
            },
            'Manual Labor': {
                'steps': -0.03, 'activity': -0.03, 'bmi': +0.05,
                'sleep_duration': +0.05, 'sleep_quality': +0.04
            }
            # ... 其他职业配置
        }

    def calculate_health_score(self, row):
        # ... (各分项评分计算)
        
        # 获取职业自适应权重
        weights = self.get_occupation_weights(row['Occupation'])
        
        # 动态加权求和
        total_score = (
            score_steps * weights['steps'] +
            score_activity * weights['activity'] +
            score_bmi * weights['bmi'] +
            score_stress * weights['stress'] +
            score_sleep_dur * weights['sleep_duration'] +
            score_sleep_qual * weights['sleep_quality']
        )
        return total_score
```

---

## 3. 睡眠 (Sleep)

**综合睡眠健康指数 (CSHI)** (`comprehensive_sleep_index.py`) 是一个多维度的综合评价指标，旨在全面反映个体的睡眠健康状况。

### 3.1 评价维度设计
CSHI 模型整合了三个核心维度：
1.  **睡眠核心维度 (权重 50%)**:
    *   直接反映睡眠表现。
    *   由**睡眠时长评分** (50%) 和 **睡眠质量评分** (50%) 构成。
2.  **心血管健康维度 (权重 25%)**:
    *   引入生理指标作为睡眠质量的客观印证。
    *   直接引用下文所述的 `Cardio_Score`。
3.  **生活方式维度 (权重 25%)**:
    *   反映睡眠卫生的外部环境。
    *   直接引用上文计算的 `Health_Score`。

### 3.2 评分计算
$$ CSHI = (Dim_{Sleep} \times 0.5) + (Dim_{Cardio} \times 0.25) + (Dim_{Lifestyle} \times 0.25) $$

### 3.3 核心代码实现
```python
# 综合睡眠健康指数计算 (comprehensive_sleep_index.py)

def calculate_cshi(self, df):
    results = []
    
    for idx, row in df.iterrows():
        # 1. 睡眠核心维度 (50%)
        # 时长评分 + 质量评分 各占一半
        dim_sleep = self.calculate_sleep_dimension(row)
        
        # 2. 健康基石维度 (引用 Cardio Score 和 Lifestyle Score)
        dim_cardio = row['Cardio_Score']
        dim_lifestyle = row['Health_Score']
        
        # 3. 加权汇总
        # 强化睡眠权重 (50%), 并独立心血管 (25%) 和生活方式 (25%)
        cshi = (dim_sleep * 0.50 + 
                dim_cardio * 0.25 + 
                dim_lifestyle * 0.25)
        
        # 风险分级
        if cshi < 60: risk_label = "差"
        elif cshi < 75: risk_label = "一般"
        elif cshi < 85: risk_label = "良"
        else: risk_label = "优"
        
        results.append({'Person ID': row['Person ID'], 'CSHI_Score': cshi, 'CSHI_Level': risk_label})
        
    return pd.DataFrame(results)
```

评分结果用于将睡眠健康风险分级：
*   **差**: < 60 分
*   **一般**: 60 - 75 分
*   **良**: 75 - 85 分
*   **优**: ≥ 85 分

---

## 4. 心血管健康 (Cardiovascular Health)

**心血管健康分数 (Cardio Score)** (`cardio_score_calculator.py`) 是一个基于生理指标和行为数据的复合风险评估模型。

### 4.1 算法模型架构
该模型由四部分组成，总分 100 分：

1.  **血压评分 (Blood Pressure Score, 权重 35%)**:
    *   基于收缩压/舒张压通过医学标准分级（理想、正常、正常高值、1-3级高血压）。
    *   **动态调整**：根据**年龄**（中老年人放宽标准）和**性别**（女性低血压容忍度）进行加分修正。
2.  **心率评分 (Heart Rate Score, 权重 25%)**:
    *   评估静息心率是否处于理想区间（如 60-80 bpm）。
    *   **动态区间**：理想区间根据年龄（随年龄增长上调）、职业（体力劳动者上调）和性别进行个性化调整。
3.  **生活方式评分 (Lifestyle Score, 权重 25%)**:
    *   综合评估运动、睡眠、压力和BMI对心血管的长期影响。
4.  **相关性协同评分 (Correlation Score, 权重 15%)**:
    *   评估健康因子的协同效应（如“高运动量+好睡眠”产生额外加分）。
    *   对存在**睡眠障碍**（失眠/呼吸暂停）的个体进行降分惩罚。

### 4.2 风险评级
根据最终得分将心血管风险划分为 5 个等级，从“高风险”（1星）到“低风险”（5星）。

### 4.3 核心代码实现
```python
# 心血管健康分数计算 (cardio_score_calculator.py)

def process_dataset(self, df):
    for idx, row in df.iterrows():
        # 1. 血压评分 (35%) - 含年龄/性别调整
        score_bp = self.calculate_bp_score(sys, dia, row['Age'], row['Gender'])
        
        # 2. 心率评分 (25%) - 含职业/年龄调整
        score_hr = self.calculate_hr_score(row['Heart Rate (bpm)'], row['Age'], row['Occupation'], ...)
        
        # 3. 生活方式评分 (25%)
        score_life = self.calculate_lifestyle_score(...)
        
        # 4. 相关性协同评分 (15%) - 睡眠障碍惩罚
        score_corr = self.calculate_correlation_score(...)
        
        # 综合分数
        final_score = (score_bp * 0.35 + 
                       score_hr * 0.25 + 
                       score_life * 0.25 + 
                       score_corr * 0.15)
                       
        risk_label, risk_stars = self.get_risk_level(final_score)
```

---

## 5. 睡眠障碍分析 (Sleep Disorder Analysis)

针对睡眠障碍（如失眠 Insomnia、睡眠呼吸暂停 Sleep Apnea），利用 `sleep_disorder_profile.py` 实现了多维度的特征画像分析。

### 5.1 分析方法
*   **BMI 分布特征**：计算不同睡眠障碍人群中各 BMI 类别（正常、超重、肥胖）的占比，揭示肥胖与呼吸暂停的强相关性。
*   **压力水平关联**：通过箱线图对比失眠症患者与健康人群的压力分布差异。
*   **血压特征分布**：利用散点图可视化收缩压与舒张压的分布，分析睡眠障碍对血压调节的潜在影响。

### 5.2 统计摘要
系统自动生成分组统计摘要，计算每类人群（正常、失眠、呼吸暂停）的：
*   平均 BMI 分类
*   平均压力指数
*   平均睡眠时长
*   平均血压与心率
*   日常活动水平

通过上述对比，量化睡眠障碍对整体生理机能的负面影响，为早期筛查提供数据支持。

### 5.3 核心代码实现
```python
# 睡眠障碍特征画像分析 (sleep_disorder_profile.py)

def create_bmi_disorder_plot(df):
    """可视化 BMI 与 睡眠障碍 的分布关系"""
    # 计算交叉表并归一化
    cross_tab = pd.crosstab(df['Sleep Disorder'], df['BMI Category'], normalize='index') * 100
    
    # 绘制堆叠条形图
    ax = cross_tab.plot(kind='barh', stacked=True, colormap='Set3')
    
    # 标注数值
    for c in ax.containers:
        ax.bar_label(c, fmt='%.1f%%', label_type='center')

def create_bp_scatter_plot(df):
    """可视化 血压特征 与 睡眠障碍 的关系"""
    sns.scatterplot(data=df, x='Systolic', y='Diastolic', hue='Sleep Disorder', 
                    style='Sleep Disorder', s=100, alpha=0.8)
    
    # 添加高血压警戒线
    plt.axvline(x=140, color='r', linestyle='--', alpha=0.3)
    plt.axhline(y=90, color='r', linestyle='--', alpha=0.3)
```
