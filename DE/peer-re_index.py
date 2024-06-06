import pandas as pd
import numpy as np

# 가중치 설정
weights = {
    'avg_feedback_count': 0.25, #평균 피드백 횟수 (positive)
    'replacement_count': -0.3, #대체 표현 개수 (negative)
    'non_participating_members_count': -0.2, #미참여자 수 (negative)
    'positive_feedback_ratio': 0.15, #긍정 피드백 비율
    'negative_feedback_ratio': -0.1 #부정 피드백 비율
}

# 예시 데이터
data = {
    'avg_feedback_count': 50,
    'replacement_count': 5,
    'non_participating_members_count': 1,
    'positive_feedback_ratio': 0.7,
    'negative_feedback_ratio': 0.1
}

# 데이터 프레임 생성
df = pd.DataFrame([data])

# Min-Max 정규화 함수
def normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)

#최소값 및 최대값 설정
min_max_values = {
    'avg_feedback_count': (0, 100),
    'replacement_count': (0, 10),
    'non_participating_members_count': (0, 20),
    'positive_feedback_ratio': (0.0, 1.0),
    'negative_feedback_ratio': (0.0, 1.0)
}

# 각 항목에 대해 정규화 적용
for column, (min_value, max_value) in min_max_values.items():
    df[column] = df[column].apply(normalize, args=(min_value, max_value))

# 가중합 계산 함수
def calculate_team_health_score(df, weights):
    score = sum(weights[col] * df[col].iloc[0] for col in weights)
    return score

# 팀 건강도 점수 계산
team_health_score = calculate_team_health_score(df, weights)
print(f"피어리 지수 : {team_health_score:.2f}")
