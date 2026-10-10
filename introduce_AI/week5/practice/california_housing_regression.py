"""
Week5 Lecture 02 실습 2: California Housing 데이터셋 회귀 (Decision Tree Regressor)

지역(블록 그룹)의 소득, 주택 연식, 방 수, 인구, 위치 등 입력 특징 8개로
주택 가격 중앙값(연속적인 값)을 예측한다.

실행 전 설치:
    pip install pandas scikit-learn
"""

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


# ===================================================================
# 1. 데이터셋 불러오기 (scikit-learn 내장)
# ===================================================================
# as_frame=True: 데이터를 pandas DataFrame 형태로 받는다.
housing = fetch_california_housing(as_frame=True)

# 입력 특징 8개와 출력(MedHouseVal)이 함께 들어 있는 전체 표의 앞 10개 행을 출력한다.
print("===================================================================")
print(housing.frame.head(10).to_string(index=False))


# ===================================================================
# 2. 입력 X와 출력 y 분리
# ===================================================================
# 입력 특징 8개: MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude
X = housing.data

# 출력(정답): MedHouseVal (주택 가격 중앙값, 단위: 10만 달러)
y = housing.target

print("===================================================================")
print(X.head(10).to_string(index=False))
print("===================================================================")
print(y.head(10).to_string(index=False))
print("===================================================================")


# ===================================================================
# 3. 훈련 데이터와 테스트 데이터 분할
# ===================================================================
# 회귀는 클래스가 없으므로 stratify를 사용하지 않는다.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,     # 전체 데이터의 20%를 test set으로 사용
    random_state=42,   # 돌릴 때마다 같게 분할되도록 시드 고정
)

print("# Training data:", len(X_train))
print("# Test data:", len(X_test))


# ===================================================================
# 4. 모델 학습(training)과 예측(testing)
# ===================================================================
model = DecisionTreeRegressor(
    criterion="squared_error",  # 어떤 feature와 threshold로 나눌지 선택하는 기준 (제곱 오차)
    max_depth=5,                # tree의 최대 depth를 5로 제한
    random_state=42,            # 결과 재현을 위해 시드 고정
)

# 훈련 집합으로 결정 트리를 학습한다.
model.fit(X_train, y_train)

# 테스트 입력으로 주택 가격을 예측한다. (결과는 클래스가 아니라 실수 값)
y_pred = model.predict(X_test)


# ===================================================================
# 5. 성능 평가: MAE와 RMSE
# ===================================================================
# MAE (Mean Absolute Error) = Σ|예측 - 정답| / m
total_error = 0
for actual, predicted in zip(y_test, y_pred):
    total_error += abs(actual - predicted)   # 오차의 절댓값을 누적
mae = total_error / len(y_test)              # 테스트 샘플 수(m)로 나눠 평균
print("MAE (Mean Absolute Error):", mae)

# RMSE (Root Mean Squared Error) = √( Σ(예측 - 정답)² / m )
# 오차를 제곱하므로 MAE보다 큰 오차에 더 큰 벌점을 준다.
total_squared_error = 0
for actual, predicted in zip(y_test, y_pred):
    total_squared_error += (actual - predicted) ** 2.0  # 오차의 제곱을 누적
rmse = (total_squared_error / len(y_test)) ** 0.5       # 평균(MSE)을 낸 뒤 제곱근(** 0.5)
print("RMSE (Root Mean Squared Error):", rmse)
