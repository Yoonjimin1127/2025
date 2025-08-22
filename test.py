# streamlit_food_nutrition.py
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# 1. 데이터 불러오기
# -----------------------
# 예시용 간단한 데이터 (실제로는 USDA/KFDA 데이터 사용 가능)
data = pd.DataFrame({
    '음식': ['사과', '바나나', '계란', '닭가슴살', '브로콜리'],
    '칼로리': [52, 89, 155, 165, 55],
    '탄수화물': [14, 23, 1, 0, 11],
    '단백질': [0.3, 1.1, 13, 31, 3.7],
    '지방': [0.2, 0.3, 11, 3.6, 0.6],
    '비타민C': [4.6, 8.7, 0, 0, 89.2]
})

# 하루 권장 섭취량 (간단 예시)
daily_req = {'칼로리': 2000, '탄수화물': 300, '단백질': 50, '지방': 70, '비타민C': 100}

# -----------------------
# 2. 사용자 입력
# -----------------------
st.title("🍎 간단 식품 영양 분석 웹")

selected_foods = st.multiselect(
    "분석할 음식을 선택하세요",
    options=data['음식'].tolist(),
    default=['사과']
)

if selected_foods:
    df_selected = data[data['음식'].isin(selected_foods)]

    st.subheader("선택한 음식의 영양소 비교")

    # -----------------------
    # 3. 바차트로 영양소 비교
    # -----------------------
    nutrients = ['칼로리', '탄수화물', '단백질', '지방', '비타민C']
    df_melted = df_selected.melt(id_vars='음식', value_vars=nutrients, var_name='영양소', value_name='함량')

    fig_bar = px.bar(
        df_melted,
        x='영양소',
        y='함량',
        color='음식',
        barmode='group',
        title='영양소 비교'
    )
    st.plotly_chart(fig_bar)

    # -----------------------
    # 4. 권장량 대비 섭취 체크
    # -----------------------
    st.subheader("하루 권장 섭취량 대비 분석")

    total_nutrients = df_selected[nutrients].sum()
    ratio = (total_nutrients / pd.Series(daily_req)) * 100
    ratio_df = ratio.reset_index()
    ratio_df.columns = ['영양소', '섭취비율(%)']

    fig_ratio = px.bar(
        ratio_df,
        x='영양소',
        y='섭취비율(%)',
        color='섭취비율(%)',
        title='하루 권장량 대비 비율',
        text='섭취비율(%)'
    )
    st.plotly_chart(fig_ratio)

    # 부족/과다 안내
    st.write("⚠️ 부족하거나 과다한 영양소:")
    for nutrient, val in ratio.items():
        if val < 80:
            st.write(f"- {nutrient}: 부족 ({val:.1f}%)")
        elif val > 120:
            st.write(f"- {nutrient}: 과다 ({val:.1f}%)")
        else:
            st.write(f"- {nutrient}: 적정 ({val:.1f}%)")
