# app.py 파일
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 예시 데이터
food_data = pd.DataFrame({
    '음식': ['계란', '시금치', '연어', '두부', '오렌지'],
    '단백질': [6, 2, 20, 8, 1],
    '비타민 C': [0, 28, 0, 0, 53],
    '철분': [1, 2, 1, 3, 0.1]
})

st.title("영양소 맞춤 메뉴 추천")

# 부족한 영양소 선택
nutrients = st.multiselect(
    "부족한 영양소를 선택하세요",
    ['단백질', '비타민 C', '철분']
)

if nutrients:
    # 선택한 영양소 기준으로 음식 추천
    recommended 
