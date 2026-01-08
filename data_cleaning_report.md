# 睡眠健康数据集清洗报告

**清洗时间**: 2026-01-08 19:21:11

---

## 数据清洗统计

| 数据集类型 | 记录数 | 占比 | 文件名 |
|-----------|--------|------|--------|
| 原始数据集 | 400 | 100.00% | sleep_health_lifestyle_dataset.csv |
| 清洗后数据集 | 341 | 85.25% | sleep_health_lifestyle_dataset_cleaned.csv |
| 异常数据集 | 59 | 14.75% | sleep_health_lifestyle_dataset_anomalies.csv |
| 完整标注数据集 | 400 | 100.00% | sleep_health_lifestyle_dataset_full_annotated.csv |

---

## 异常类型统计

| 异常类型 | 描述 | 数量 | 占总异常比例 |
|---------|------|------|-------------|
| AGE_OCCUPATION_1.2 | 年龄<30岁但职业为Retired | 24 | 40.68% |
| AGE_OCCUPATION_1.3 | 年龄>=70岁但职业为Student | 3 | 5.08% |
| STRESS_SLEEP_6.1 | 压力>=9分但睡眠质量>=8分 | 17 | 28.81% |
| STRESS_SLEEP_6.2 | 压力<=2分但睡眠质量<=4分 | 12 | 20.34% |
| STEPS_ACTIVITY_9.1 | 日步数>=18000但运动时长<=30分钟 | 3 | 5.08% |

---

## 异常记录详情

### AGE_OCCUPATION_1.2

| Person ID | Age | Occupation | Gender |
|---|---|---|---|
| 30 | 27 | Retired | Female |
| 99 | 21 | Retired | Female |
| 106 | 29 | Retired | Female |
| 114 | 21 | Retired | Female |
| 120 | 18 | Retired | Male |
| 149 | 27 | Retired | Male |
| 185 | 27 | Retired | Male |
| 233 | 28 | Retired | Female |
| 239 | 26 | Retired | Male |
| 245 | 18 | Retired | Male |
| 261 | 18 | Retired | Male |
| 279 | 22 | Retired | Male |
| 286 | 19 | Retired | Male |
| 293 | 20 | Retired | Male |
| 304 | 28 | Retired | Female |
| 308 | 22 | Retired | Female |
| 331 | 18 | Retired | Male |
| 334 | 18 | Retired | Male |
| 347 | 26 | Retired | Male |
| 356 | 27 | Retired | Male |
| 375 | 18 | Retired | Male |
| 380 | 18 | Retired | Male |
| 385 | 27 | Retired | Male |
| 390 | 23 | Retired | Male |

### AGE_OCCUPATION_1.3

| Person ID | Age | Occupation | Gender |
|---|---|---|---|
| 58 | 90 | Student | Male |
| 69 | 74 | Student | Female |
| 327 | 86 | Student | Male |

### STRESS_SLEEP_6.1

| Person ID | Stress Level (scale: 1-10) | Quality of Sleep (scale: 1-10) | Sleep Disorder |
|---|---|---|---|
| 4 | 10 | 10.0 | nan |
| 16 | 10 | 9.1 | nan |
| 81 | 9 | 8.0 | nan |
| 85 | 9 | 8.2 | nan |
| 97 | 9 | 10.0 | Insomnia |
| 105 | 10 | 9.3 | nan |
| 117 | 10 | 8.4 | nan |
| 142 | 9 | 10.0 | Insomnia |
| 146 | 9 | 10.0 | nan |
| 210 | 9 | 10.0 | nan |
| 272 | 10 | 10.0 | Insomnia |
| 345 | 9 | 8.4 | Sleep Apnea |
| 352 | 10 | 9.4 | nan |
| 373 | 10 | 10.0 | nan |
| 388 | 9 | 9.0 | nan |
| 391 | 10 | 8.7 | nan |
| 399 | 9 | 9.1 | Sleep Apnea |

### STRESS_SLEEP_6.2

| Person ID | Stress Level (scale: 1-10) | Quality of Sleep (scale: 1-10) | Sleep Disorder |
|---|---|---|---|
| 17 | 1 | 3.5 | nan |
| 18 | 2 | 3.1 | nan |
| 127 | 2 | 3.8 | nan |
| 157 | 1 | 2.6 | Sleep Apnea |
| 160 | 2 | 3.8 | Insomnia |
| 224 | 1 | 4.0 | nan |
| 230 | 1 | 2.9 | nan |
| 269 | 2 | 3.8 | nan |
| 270 | 1 | 1.7 | Insomnia |
| 332 | 2 | 2.4 | nan |
| 336 | 2 | 1.0 | nan |
| 353 | 2 | 3.3 | nan |

### STEPS_ACTIVITY_9.1

| Person ID | Daily Steps | Physical Activity Level (minutes/day) | BMI Category |
|---|---|---|---|
| 34 | 18034 | 30 | Obese |
| 194 | 18351 | 28 | Normal |
| 333 | 18526 | 30 | Normal |

---

## 清洗标准说明

清洗依据以下逻辑异常标准：

1. **年龄与职业不匹配**：年龄过小却已退休，或年龄过大仍是学生
2. **压力与睡眠质量矛盾**：极高压力却有极高睡眠质量，或极低压力却睡眠质量很差
3. **步数与运动时长矛盾**：步数很高但运动时间很短

---

## 文件说明

### 推荐使用的数据集
- **sleep_health_lifestyle_dataset_cleaned.csv**：推荐用于后续数据分析，仅包含正常记录

### 参考数据集
- **sleep_health_lifestyle_dataset_anomalies.csv**：异常记录，供研究参考
- **sleep_health_lifestyle_dataset_full_annotated.csv**：包含质量标记的完整数据

### 备份数据集
- **sleep_health_lifestyle_dataset_backup.csv**：原始数据的完整备份

---

## 数据质量评估

- **清洗前数据量**: 400条
- **清洗后数据量**: 341条
- **数据保留率**: 85.25%
- **异常剔除率**: 14.75%

**结论**: 清洗后的数据集保留了绝大部分数据，同时剔除了明显的逻辑异常，适合进行后续的数据分析和建模工作。