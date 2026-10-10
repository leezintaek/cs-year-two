"""
Week5 Lecture 02 실습 1: Iris 데이터셋 분류 (Decision Tree Classifier)

꽃받침/꽃잎의 길이와 너비(입력 특징 4개)로 붓꽃의 종류(클래스 3개)를 예측한다.

실행 전 설치:
    pip install pandas datasets scikit-learn matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text


# ===================================================================
# 1. 데이터셋 불러오기 (Hugging Face)
# ===================================================================
# Hugging Face에 올라와 있는 Iris 데이터셋의 train split을 내려받는다.
dataset = load_dataset("scikit-learn/iris", split="train")

# 다루기 쉽도록 pandas DataFrame(표 형태)으로 변환한다.
df = dataset.to_pandas()

# 앞의 10개 행을 출력해 데이터 구조를 확인한다.
print("===================================================================")
print(df.head(10).to_string(index=False))


# ===================================================================
# 2. 입력 X와 출력 y 분리
# ===================================================================
# 꽃받침의 길이/너비, 꽃잎의 길이/너비 (4개의 input features) -> 꽃종류 (1개의 output)
X = df[["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]]

# 레이블(정답): 3개의 class를 가지고 있음 (setosa, versicolor, virginica)
y = df["Species"]

print("===================================================================")
print(X.head(10).to_string(index=False))  # 특징 벡터 예: [5.1, 3.5, 1.4, 0.2]
print("===================================================================")
print(y.head(10).to_string(index=False))  # 레이블 예: Iris-setosa
print("===================================================================")


# ===================================================================
# 3. 훈련 데이터와 테스트 데이터 분할
# ===================================================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,     # 전체 데이터의 20%를 test set으로 사용
    random_state=42,   # 돌릴 때마다 같게 분할되도록 시드 고정
    stratify=y,        # y 기준으로 균일하게 분할 (각 클래스 비율을 train/test에서 동일하게 유지)
)

print("# Training data:", len(X_train))  # 150개 중 120개
print("# Test data:", len(X_test))       # 150개 중 30개


# ===================================================================
# 4. 모델 학습(training)과 예측(testing)
# ===================================================================
model = DecisionTreeClassifier(
    criterion="gini",  # 어떤 feature와 threshold로 나눌지 선택하는 기준 (지니 불순도)
    max_depth=3,       # tree의 최대 depth를 3으로 제한 (너무 깊으면 과대적합 위험)
    random_state=42,   # 결과 재현을 위해 시드 고정
)

# 훈련 집합(X_train, y_train)으로 결정 트리를 학습한다.
model.fit(X_train, y_train)

# 학습된 모델에 테스트 입력(X_test)을 넣어 꽃 종류를 예측한다.
y_pred = model.predict(X_test)


# ===================================================================
# 5. 성능 평가: 정확도(accuracy)와 오류율(error rate)
# ===================================================================
# accuracy  = (예측 == 정답인 샘플 수) / (테스트 샘플 수)
# errorRate = (예측 != 정답인 샘플 수) / (테스트 샘플 수) = 1 - accuracy
correct = 0
for actual, predicted in zip(y_test, y_pred):  # 정답(actual)과 예측(predicted)을 한 쌍씩 비교
    if actual == predicted:
        correct += 1                           # 맞힌 개수를 센다

accuracy = correct / len(y_test)
error_rate = (len(y_test) - correct) / len(y_test)

print("===================================================================")
print("Test Accuracy:", accuracy * 100.0)  # 백분율(%)로 출력
print("Error Rate:", error_rate * 100.0)


# ===================================================================
# 6. 학습된 결정 트리 확인
# ===================================================================
# (1) 텍스트로 결정 규칙 출력: 어떤 feature를 어떤 threshold로 나눴는지 보여준다.
decision_rules = export_text(
    model,
    feature_names=list(X.columns),  # 규칙에 feature 이름이 표시되도록 지정
)
print("===================================================================")
print(decision_rules)

# (2) 그림으로 시각화: 각 노드에 결정 규칙, 샘플 수, 불순도, 다수 클래스가 표시된다.
plt.figure(figsize=(9, 5))
plot_tree(
    model,
    feature_names=X.columns,      # 노드에 표시할 feature 이름
    class_names=model.classes_,   # 노드에 표시할 클래스 이름
    filled=True,                  # 다수 클래스에 따라 노드 색칠
    rounded=True,                 # 노드 모서리를 둥글게
)
plt.show()
