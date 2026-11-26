---
title: "Vanishing Gradient와 Normalization — Data / Batch / Layer Norm 정리"
# 대안 제목:
# - Gradient는 왜 사라질까? Vanishing Gradient와 BatchNorm · LayerNorm
# - Normalization 3종 정리: Min-max, Z-score부터 BatchNorm vs LayerNorm까지
date: 2026-11-06
tags: [Deep Learning, Vanishing Gradient, Normalization, Batch Normalization, Layer Normalization]
series: "인공지능개론 Week 9"
---

> 인공지능개론 Week 9 (Deep Learning 2) 강의를 공부하며 정리한 글입니다.
> 이 글은 **2편**입니다. Linear region과 Backpropagation 계산은 [1편](./week9_blog_1.md)에서 다뤘습니다. <!-- 블로그 URL로 교체 -->

## 목차

1. [Vanishing / Exploding Gradients](#1-vanishing--exploding-gradients)
2. [Normalization 개요](#2-normalization-개요)
3. [Data Normalization](#3-data-normalization)
4. [Batch Normalization](#4-batch-normalization)
5. [Layer Normalization](#5-layer-normalization)
6. [더 알아두면 좋은 것](#6-더-알아두면-좋은-것)
7. [정리](#7-정리)

---

## 1. Vanishing / Exploding Gradients

1편의 예시에서 Gradient 값은 이렇게 나왔습니다.

$$
\frac{\partial L}{\partial w_{2,0,0}} \approx 0.041
\qquad
\frac{\partial L}{\partial w_{1,0,0}} \approx 0.002
$$

한 층 앞으로 갔을 뿐인데 Gradient가 약 20배 작아졌습니다. 이유는 Chain rule에 있습니다.

### 1.1 원인: 곱셈이 쌓인다

앞쪽 layer의 Gradient를 구하려면, 뒤쪽 layer들의 미분값을 **모두 곱해야** 합니다.

$$
\frac{\partial L}{\partial w_1}
= \frac{\partial L}{\partial o_K}
\cdot \prod_{k} \left( \frac{\partial o_k}{\partial z_k} \cdot \frac{\partial z_k}{\partial o_{k-1}} \right)
\cdot \frac{\partial z_1}{\partial w_1}
$$

- 곱하는 항의 크기가 대부분 **1보다 작으면** 곱이 0으로 수렴합니다. 이것이 **Vanishing gradient**입니다.
- 곱하는 항의 크기가 대부분 **1보다 크면** 곱이 ∞로 발산합니다. 이것이 **Exploding gradient**입니다.

Network가 깊어질수록 곱하는 항이 많아지므로 두 문제 모두 심해집니다. 결과적으로 앞쪽 layer와 뒤쪽 layer의 Gradient 크기가 크게 벌어집니다.

> 📷 **[이미지 추가]** Layer 깊이에 따라 Gradient 크기가 줄어들거나 커지는 그래프 — 추천 출처: 슬라이드 23~24

### 1.2 Sigmoid가 특히 취약한 이유

Sigmoid의 미분은 다음과 같습니다.

$$
\sigma'(z) = \sigma(z)(1 - \sigma(z)) \le 0.25
$$

최댓값이 $z = 0$일 때 $0.25$입니다. 즉 Sigmoid layer를 하나 지날 때마다 Gradient가 **최소 1/4로** 줄어듭니다. 10층이면 $0.25^{10} \approx 10^{-6}$입니다.

> 📷 **[이미지 추가]** Sigmoid 함수와 그 미분 $\sigma'(z)$ 그래프 (최댓값 0.25 표시) — 추천 출처: 직접 그림

---

## 2. Normalization 개요

Network가 **극단적으로 크거나 작은 값을 다루지 않도록** 값의 범위를 맞춰주는 기법입니다. 강의에서는 세 가지를 다룹니다.

| 종류                | 정규화 대상       | 언제        |
|---------------------|-------------------|-------------|
| Data Normalization  | 입력 데이터       | 학습 전 1번 |
| Batch Normalization | Mini-batch 단위   | 매 update   |
| Layer Normalization | 샘플별 layer 단위 | 매 update   |

---

## 3. Data Normalization

### 3.1 왜 필요한가

입력 변수들의 범위가 크게 다른 경우가 많습니다. 예를 들어 집값 데이터에서 면적은 수백 단위이고, 방 개수는 1~5 정도입니다. 이대로 학습하면 범위가 큰 변수가 Weighted sum을 지배하고, 범위가 작은 변수의 영향은 묻혀 버립니다. 또 변수마다 Gradient 크기가 달라져 학습도 불안정해집니다.

> 📷 **[이미지 추가]** Housing data에서 변수별 값 범위가 다른 표 — 추천 출처: 슬라이드 6

입력값을 비슷한 범위로 **Re-scale**하면 이 문제가 해결됩니다. Data normalization은 **학습 전에 한 번만** 합니다.

### 3.2 Min-max Normalization

값을 **0~1 범위**로 맞춥니다.

$$
\tilde{x}_i = \frac{x_i - x_{\min}}{x_{\max} - x_{\min}}
$$

### 3.3 Z-score Normalization

값을 **평균 0, 분산 1**로 맞춥니다.

$$
\tilde{x}_i = \frac{x_i - \mu}{\sigma},
\qquad
\mu = \frac{1}{N}\sum_{i=1}^{N} x_i,
\qquad
\sigma = \sqrt{\frac{1}{N}\sum_{i=1}^{N} (x_i - \mu)^2}
$$

| Method  | 결과 범위      | Outlier 영향    |
|---------|----------------|-----------------|
| Min-max | [0, 1]         | 큼              |
| Z-score | 평균 0, 분산 1 | 상대적으로 작음 |

Min-max는 최댓값과 최솟값만으로 범위를 정합니다. 그래서 Outlier가 하나만 있어도 나머지 값들이 좁은 구간에 몰려 버립니다.

> 📷 **[이미지 추가]** 정규화 전후 데이터 분포 비교 — 추천 출처: 슬라이드 7~10

---

## 4. Batch Normalization

Data normalization은 **입력**만 정리합니다. 하지만 학습 중에는 Weight가 계속 바뀌므로, Hidden layer를 지나는 값의 분포도 계속 변합니다. 그래서 **Hidden unit의 값**을 **Weight가 업데이트될 때마다** 다시 정규화합니다. 목적은 Vanishing/Exploding gradient를 완화하는 것입니다.

### 4.1 계산 방법

크기가 $K$인 Mini-batch에서, **Hidden unit 하나**에 대해 batch 안의 $K$개 값으로 평균과 분산을 구합니다.

$$
\mu = \frac{1}{K}\sum_{i=1}^{K} a_i,
\qquad
\sigma^2 = \frac{1}{K}\sum_{i=1}^{K} (a_i - \mu)^2
$$

$$
\hat{a}_i = \frac{a_i - \mu}{\sqrt{\sigma^2 + \epsilon}}
$$

Z-score와 비슷하지만 **두 가지가 다릅니다**.

**1. $\epsilon$ (epsilon)**

$\sigma^2$이 0에 가까울 때 0으로 나누는 문제를 막기 위한 아주 작은 양수입니다.

**2. Scale-and-shift**

정규화로 모든 값을 평균 0, 분산 1로 고정하면 Network의 표현력이 제한될 수 있습니다. 그래서 학습 가능한 Parameter $\gamma$, $\beta$로 다시 조정합니다.

$$
\tilde{a}_i = \gamma \hat{a}_i + \beta
$$

- $\gamma$: Scaling parameter
- $\beta$: Shifting parameter

이 두 값은 Weight처럼 Gradient descent로 학습됩니다. 필요하면 Network가 정규화를 사실상 되돌릴 수도 있습니다.

---

## 5. Layer Normalization

계산 식은 BatchNorm과 같고, **평균과 분산을 구하는 방향만 다릅니다**.

$$
\hat{a}_i = \frac{a_i - \mu}{\sqrt{\sigma^2 + \epsilon}}
$$

- **BatchNorm**: Hidden unit 하나를 고정하고, batch 안의 **여러 샘플**에 걸쳐 통계를 냅니다.
- **LayerNorm**: 샘플 하나를 고정하고, 그 layer의 **여러 Hidden unit**에 걸쳐 통계를 냅니다.

> 📷 **[이미지 추가]** BatchNorm과 LayerNorm의 정규화 방향 비교 (샘플 × unit 격자에서 세로 방향 vs 가로 방향) — 추천 출처: 슬라이드 26

| 항목            | BatchNorm            | LayerNorm            |
|-----------------|----------------------|----------------------|
| 통계 계산 축    | 같은 unit, 여러 샘플 | 같은 샘플, 여러 unit |
| batch size 의존 | 있음                 | 없음                 |
| 추론 시         | running mean/var     | 그대로 계산          |
| 주 사용처       | CNN                  | RNN, Transformer     |

### 어떤 걸 쓸까?

- **Batch size가 충분히 클 때**는 BatchNorm이 잘 동작합니다. 샘플이 많아 평균과 분산 추정이 안정적이기 때문입니다.
- **Batch size가 작거나 샘플 하나씩 처리할 때**는 LayerNorm이 유리합니다. batch size가 작으면 BatchNorm의 통계가 불안정해지지만, LayerNorm은 샘플 하나만으로 계산하므로 batch size의 영향을 받지 않습니다.

> **Note** 여기서 중요한 것은 batch의 **개수**가 아니라 batch 하나에 든 샘플 수, 즉 **batch size**입니다.

---

## 6. 더 알아두면 좋은 것

강의 범위 밖이지만 함께 알아두면 좋은 내용입니다.

### Vanishing gradient의 다른 해결책

- **ReLU**: 양수 구간의 미분이 항상 1이라 Gradient가 덜 사라집니다. 그래서 Hidden layer에는 Sigmoid 대신 ReLU 계열을 주로 씁니다.
- **Weight initialization**: Xavier(Glorot) initialization이나 He initialization은 layer를 지나도 값의 분산이 유지되도록 초기 Weight의 크기를 정합니다.
- **Residual connection** (ResNet): $y = F(x) + x$처럼 입력을 건너뛰어 더해 줍니다. Gradient가 지나갈 지름길이 생겨 수백 층도 학습할 수 있습니다.
- **Gradient clipping**: Exploding gradient를 막기 위해 Gradient의 크기가 기준값을 넘으면 잘라냅니다.

### BatchNorm의 추론(Inference) 시 동작

테스트할 때는 샘플이 하나씩 들어올 수 있어 batch 통계를 낼 수 없습니다. 그래서 학습 중에 모아 둔 **Running mean / Running variance**(이동 평균)를 대신 씁니다. 학습할 때와 추론할 때 동작이 다르다는 점은 구현할 때 자주 실수하는 부분입니다. PyTorch의 `model.train()` / `model.eval()`이 이 차이를 처리합니다.

### Transformer가 LayerNorm을 쓰는 이유

문장은 길이가 제각각이고, RNN과 Transformer는 시퀀스 단위로 처리합니다. 이런 구조에서는 batch 방향 통계가 잘 맞지 않습니다. 샘플 단위로 계산하는 LayerNorm은 이 문제가 없어서, GPT와 BERT 같은 Transformer 모델의 표준이 되었습니다.

---

## 7. 정리

- 깊은 Network에서는 Chain rule의 곱셈이 쌓여 Gradient가 사라지거나(**Vanishing**) 폭발합니다(**Exploding**). Sigmoid는 미분 최댓값이 0.25라 특히 취약합니다.
- **Data normalization**(Min-max, Z-score)은 입력 변수의 범위를 맞추는 것이며, 학습 전에 한 번 합니다.
- **Batch normalization**은 Hidden unit 값을 Mini-batch 통계로 매번 정규화하고, $\epsilon$과 학습 가능한 $\gamma$, $\beta$를 씁니다.
- **Layer normalization**은 같은 식을 샘플 하나 안의 unit들에 적용합니다. Batch size의 영향을 받지 않아 RNN과 Transformer에 적합합니다.

## Reference

- Bishop, C. M., & Bishop, H. (2024). *Deep Learning: Foundations and Concepts*. Springer.
- [Data Normalization Techniques — dataaspirant](https://dataaspirant.com/data-normalization-techniques/)
- 인하대학교 인공지능개론(CSE2302) Week 9 강의 자료
