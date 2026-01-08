"""
睡眠障碍机器学习预测模型训练脚本
使用 Random Forest Classifier 进行分类预测
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib import font_manager
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

# --- 字体配置 ---
chinese_font = None
def setup_font():
    global chinese_font
    font_paths = ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']
    font_path = None
    for path in font_paths:
        if os.path.exists(path):
            font_path = path
            break
            
    if font_path:
        chinese_font = font_manager.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = chinese_font.get_name()
        font_manager.fontManager.addfont(font_path)
        plt.rcParams['axes.unicode_minus'] = False

setup_font()
sns.set_style("whitegrid")
if chinese_font: plt.rcParams['font.family'] = chinese_font.get_name()

def load_and_preprocess_data():
    """加载并预处理数据"""
    print("[1] 加载数据...")
    try:
        df = pd.read_csv('sleep_health_lifestyle_dataset_cleaned.csv')
    except:
        df = pd.read_csv('sleep_health_lifestyle_dataset.csv')
        
    print(f"    原始数据量: {len(df)}")
    
    # 1. 处理目标变量
    df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')
    
    # 2. 移除无关列
    if 'Person ID' in df.columns:
        df = df.drop('Person ID', axis=1)
        
    # 3. 血压处理 (拆分)
    if 'Blood Pressure (systolic/diastolic)' in df.columns:
        df[['Systolic', 'Diastolic']] = df['Blood Pressure (systolic/diastolic)'].str.split('/', expand=True).astype(int)
        df = df.drop('Blood Pressure (systolic/diastolic)', axis=1)
        
    # 4. 特征编码 (One-Hot for categorical)
    # 识别分类列
    cat_cols = ['Gender', 'Occupation', 'BMI Category']
    print(f"    进行One-Hot编码: {cat_cols}")
    
    # 获取特征矩阵 X 和目标向量 y
    X = df.drop('Sleep Disorder', axis=1)
    y = df['Sleep Disorder']
    
    # One-Hot 编码
    X = pd.get_dummies(X, columns=cat_cols, drop_first=False)
    
    # 目标变量编码 (Label Encoding)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    print(f"    特征数量: {X.shape[1]}")
    print(f"    目标类别: {le.classes_}")
    
    return X, y_encoded, le, df

def train_and_evaluate(X, y, le):
    """训练并评估模型"""
    print("\n[2] 划分训练集与测试集 (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("\n[3] 训练随机森林模型...")
    # 打印训练集分布
    unique, counts = np.unique(y_train, return_counts=True)
    print(f"    训练集分布: {dict(zip(le.inverse_transform(unique), counts))}")
    
    # 使用强力自定义权重
    # 既然 'balanced' 不够, 我们手动给少数类超高权重
    custom_weights = {0: 10, 1: 1, 2: 20} # 假设 0:Insomnia, 1:None, 2:Apnea (需根据le.classes_确认顺序)
    # 为了保险, 我们使用 'balanced_subsample' 这也是一个很强的选项
    
    rf = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced_subsample', max_depth=10)
    rf.fit(X_train, y_train)
    
    print("\n[4] 模型评估:")
    y_pred = rf.predict(X_test)
    
    # 准确率
    acc = accuracy_score(y_test, y_pred)
    print(f"    准确率 (Accuracy): {acc:.2%}")
    
    # 详细报告
    target_names = [str(c) for c in le.classes_]
    report = classification_report(y_test, y_pred, target_names=target_names)
    print("\n    分类报告:")
    print(report)
    
    # 保存报告到文件
    with open('model_performance.txt', 'w', encoding='utf-8') as f:
        f.write(f"Accuracy: {acc:.2%}\n\n")
        f.write("Classification Report:\n")
        f.write(report)
        
    return rf, X_test, y_test, y_pred, target_names, X.columns

def plot_confusion_matrix(y_test, y_pred, target_names):
    """绘制混淆矩阵"""
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=target_names, yticklabels=target_names)
    plt.title('模型混淆矩阵', fontsize=14, fontweight='bold')
    plt.xlabel('预测类别')
    plt.ylabel('真实类别')
    plt.tight_layout()
    plt.savefig('model_confusion_matrix.png', dpi=300)
    print("✓ 生成: model_confusion_matrix.png")

def plot_feature_importance(model, feature_names):
    """绘制特征重要性"""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    # 取前15个重要特征
    top_n = 15
    top_indices = indices[:top_n]
    
    plt.figure(figsize=(10, 8))
    sns.barplot(x=importances[top_indices], y=[feature_names[i] for i in top_indices], palette='viridis')
    plt.title('随机森林模型特征重要性 TOP15', fontsize=14, fontweight='bold')
    plt.xlabel('重要性得分')
    plt.tight_layout()
    plt.savefig('model_feature_importance.png', dpi=300)
    print("✓ 生成: model_feature_importance.png")

def main():
    # 1. 数据准备
    X, y, le, raw_df = load_and_preprocess_data()
    
    # 2. 训练评估
    model, X_test, y_test, y_pred, target_names, feature_names = train_and_evaluate(X, y, le)
    
    # 3. 可视化
    plot_confusion_matrix(y_test, y_pred, target_names)
    plot_feature_importance(model, feature_names)
    
    print("\n所有任务完成!")

if __name__ == '__main__':
    main()
