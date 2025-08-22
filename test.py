# -*- coding: utf-8 -*-
"""
Nutrition Insight — 식품 영양 분석 대시보드
-------------------------------------------------
- 음식 검색/선택 → 영양소 시각화(바/레이다)
- 다중 음식 비교(z-score 정규화)
- RDA(권장섭취량) 대비 진단
- 영양소 유사도 기반 대체 음식 추천
- 영양소 간 상관 히트맵
- CSV 업로드/데모 데이터 지원, 결과 내보내기

실행:
    streamlit run nutrition_app.py
필요 패키지:
    pip install streamlit plotly scikit-learn pandas numpy
"""

import io
import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------------------------
# 기본 설정
# -------------------------------------------------
st.set_page_config(
    page_title="Nutrition Insight",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 Nutrition Insight — 식품 영양 분석 대시보드")
st.caption("공개 데이터 또는 데모 데이터로 영양소 비교·진단·추천을 수행합니다.")

# -------------------------------------------------
# 유틸: 데모 데이터 생성
# -------------------------------------------------
NUTR_COLS = [
    "calories_kcal","carb_g","protein_g","fat_g","fiber_g","sugars_g",
    "vitA_µg","vitC_mg","vitD_µg","vitE_mg","vitK_µg","vitB1_mg","vitB2_mg","vitB6_mg","folate_µg",
    "calcium_mg","iron_mg","zinc_mg","magnesium_mg","potassium_mg","sodium_mg"
]

CATEG = ["Fruit", "Vegetable", "Grain", "Dairy", "Meat", "Seafood", "Nuts/Seeds"]

rng = np.random.default_rng(42)

def make_demo_foods(n=60):
    foods = []
    base_names = [
        "apple","banana","broccoli","spinach","carrot","tomato","rice","oats","bread",
        "milk","yogurt","cheese","chicken","beef","pork","salmon","tuna","shrimp",
        "almond","walnut","pumpkin seed","sweet potato","avocado","egg","tofu","kimchi",
        "soy milk","mackerel","noodles","lettuce","cabbage","onion","garlic","pear","peach",
        "strawberry","blueberry","cucumber","zucchini","potato","bell pepper","kale","mushroom",
        "edamame","barley","quinoa","brown rice","chickpea","lentil","skim milk","dark chocolate"
    ]
    for i, name in enumerate(base_names[:n]):
        cat = rng.choice(CATEG)
        serving = rng.integers(50, 200)  # g
        # 영양 생성(대략적 분포)
        calories = max(10, rng.normal(1.2*serving, 30))
        carb = max(0, rng.normal(0.15*serving/10, 5))
        protein = max(0, rng.normal(0.08*serving/10, 3))
        fat = max(0, rng.normal(0.05*serving/10, 2))
        fiber = max(0, rng.normal(2, 1))
        sugars = max(0, rng.normal(5, 3))
        vitA = max(0, rng.normal(200, 150))
        vitC = max(0, rng.normal(20, 15))
        vitD = max(0, rng.normal(1.5, 0.8))
        vitE = max(0, rng.normal(2.5, 1.2))
        vitK = max(0, rng.normal(40, 30))
        vitB1 = max(0, rng.normal(0.25, 0.1))
        vitB2 = max(0, rng.normal(0.3, 0.15))
        vitB6 = max(0, rng.normal(0.35, 0.15))
        folate = max(0, rng.normal(80, 40))
        calcium = max(0, rng.normal(120, 60))
        iron = max(0, rng.normal(1.5, 0.8))
        zinc = max(0, rng.normal(1.2, 0.6))
        magnesium = max(0, rng.normal(40, 20))
        potassium = max(0, rng.normal(300, 120))
        sodium = max(0, rng.normal(120, 80))

        foods.append({
            "food_id": i+1,
            "food_name": name,
            "category": cat,
            "serving_size_g": serving,
            "calories_kcal": calories,
            "carb_g": carb,
            "protein_g": protein,
            "fat_g": fat,
            "fiber_g": fiber,
            "sugars_g": sugars,
            "vitA_µg": vitA,
            "vitC_mg": vitC,
            "vitD_µg": vitD,
            "vitE_mg": vitE,
            "vitK_µg": vitK,
            "vitB1_mg": vitB1,
            "vitB2_mg": vitB2,
            "vitB6_mg": vitB6,
            "folate_µg": folate,
            "calcium_mg": calcium,
            "iron_mg": iron,
            "zinc_mg": zinc,
            "magnesium_mg": magnesium,
            "potassium_mg": potassium,
            "sodium_mg": sodium,
        })
    return pd.DataFrame(foods)


def make_demo_rda():
    rows = []
    for age, sex, act in [("14-18","M","moderate"),("14-18","F","moderate"),("19-29","M","moderate"),("19-29","F","moderate")]:
        base = {
            "age_group": age, "sex": sex, "activity_level": act,
            "calories_kcal": 2400 if sex=="M" else 2000,
            "carb_g": 300, "protein_g": 65 if sex=="M" else 55, "fat_g": 70, "fiber_g": 25 if sex=="F" else 30,
            "sugars_g": 50, "vitA_µg": 900 if sex=="M" else 700, "vitC_mg": 90 if sex=="M" else 75,
            "vitD_µg": 15, "vitE_mg": 15, "vitK_µg": 120 if sex=="M" else 90, "vitB1_mg": 1.2 if sex=="M" else 1.1,
            "vitB2_mg": 1.3 if sex=="M" else 1.1, "vitB6_mg": 1.3, "folate_µg": 400, "calcium_mg": 1000,
            "iron_mg": 11 if sex=="M" else 15, "zinc_mg": 11 if sex=="M" else 8, "magnesium_mg": 400 if sex=="M" else 310,
            "potassium_mg": 3500, "sodium_mg": 2000,
        }
        rows.append(base)
    return pd.DataFrame(rows)

# -------------------------------------------------
# 데이터 로딩 섹션
# -------------------------------------------------
st.sidebar.header("📁 데이터 입력")
use_demo = st.sidebar.toggle("데모 데이터 사용", value=True, help="실제 CSV가 있으면 끄고 아래에서 업로드/경로 지정")

uploaded_foods = st.sidebar.file_uploader("foods_nutrition.csv 업로드", type=["csv"], accept_multiple_files=False)
uploaded_rda = st.sidebar.file_uploader("rda_reference.csv 업로드", type=["csv"], accept_multiple_files=False)

foods_path = st.sidebar.text_input("Foods CSV 경로(선택)")
rda_path = st.sidebar.text_input("RDA CSV 경로(선택)")

@st.cache_data(show_spinner=False)
def load_df(uploaded_file, path, demo_fn):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    if path and os.path.exists(path):
        return pd.read_csv(path)
    return demo_fn()

foods_df = load_df(uploaded_foods, foods_path, make_demo_foods)
rda_df = load_df(uploaded_rda, rda_path, make_demo_rda)

# 공통 칼럼 존재 확인
missing = [c for c in NUTR_COLS if c not in foods_df.columns]
if missing:
    st.error(f"foods_nutrition 데이터에 필요한 칼럼이 없습니다: {missing}")
    st.stop()

# -------------------------------------------------
# 검색/선택 UI
# -------------------------------------------------
st.sidebar.header("🔎 탐색")
q = st.sidebar.text_input("음식 검색", value="")
filtered = foods_df[foods_df["food_name"].str.contains(q, case=False, na=False)] if q else foods_df

max_sel = st.sidebar.slider("최대 선택 개수", 1, 8, 5)
choices = st.sidebar.multiselect("음식 선택", filtered["food_name"].tolist()[:500], max_selections=max_sel)
sel_df = foods_df[foods_df["food_name"].isin(choices)].copy()

st.sidebar.header("👤 RDA 프로필")
age_group = st.sidebar.selectbox("연령대", sorted(rda_df["age_group"].unique().tolist()))
sex = st.sidebar.selectbox("성별", sorted(rda_df["sex"].unique().tolist()))
activity = st.sidebar.selectbox("활동량", sorted(rda_df["activity_level"].unique().tolist()))

# -------------------------------------------------
# 탭 구성
# -------------------------------------------------
t_overview, t_compare, t_rda, t_reco, t_corr = st.tabs(["📊 개요", "⚖️ 비교", "🧭 RDA 진단", "✨ 추천", "🧪 상관분석"]) 

# -------------------------------------------------
# 📊 개요
# -------------------------------------------------
with t_overview:
    st.subheader("선택 음식 영양 성분(1회 제공량 기준)")
    if sel_df.empty:
        st.info("왼쪽 사이드바에서 음식을 검색/선택하세요.")
    else:
        long = sel_df.melt(id_vars=["food_name", "category"], value_vars=NUTR_COLS, var_name="nutrient", value_name="amount")
        fig = px.bar(long, x="nutrient", y="amount", color="food_name", barmode="group")
        fig.update_layout(xaxis_tickangle=-45, legend_title_text="음식")
        st.plotly_chart(fig, use_container_width=True)

        # 레이다(폴라) — 첫 2개만 비교
        if len(sel_df) >= 2:
            st.markdown("**레이다(영양 균형 비교)** — 처음 2개 항목 기준")
            radar_cols = ["protein_g","carb_g","fat_g","fiber_g","vitC_mg","calcium_mg","iron_mg","potassium_mg","sodium_mg"]
            r2 = sel_df.iloc[:2][["food_name"] + radar_cols].copy()
            # 정규화(0-1)
            rmin = foods_df[radar_cols].min()
            rmax = foods_df[radar_cols].max()
            rnorm = (r2[radar_cols] - rmin) / (rmax - rmin + 1e-9)
            rlong = pd.concat([r2[["food_name"]], rnorm], axis=1).melt(id_vars=["food_name"], var_name="nutrient", value_name="norm")
            fig_r = px.line_polar(rlong, r="norm", theta="nutrient", color="food_name", line_close=True)
            st.plotly_chart(fig_r, use_container_width=True)

        # 다운로드
        csv = sel_df[["food_name","category","serving_size_g"] + NUTR_COLS].to_csv(index=False).encode("utf-8")
        st.download_button("선택 데이터 CSV 다운로드", csv, "selected_foods.csv", mime="text/csv")

# -------------------------------------------------
# ⚖️ 비교 (정규화)
# -------------------------------------------------
with t_compare:
    st.subheader("정규화 비교 (z-score)")
    if sel_df.empty:
        st.info("음식을 선택하면 정규화 비교가 가능합니다.")
    else:
        scaler = StandardScaler()
        X = scaler.fit_transform(sel_df[NUTR_COLS].fillna(0))
        zdf = pd.DataFrame(X, columns=NUTR_COLS, index=sel_df["food_name"]).reset_index().melt(
            id_vars=["index"], var_name="nutrient", value_name="z")
        zdf.rename(columns={"index":"food_name"}, inplace=True)
        fig = px.bar(zdf, x="nutrient", y="z", color="food_name", barmode="group")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# 🧭 RDA 진단
# -------------------------------------------------
with t_rda:
    st.subheader("RDA(권장 섭취량) 대비 진단")
    key = (rda_df["age_group"] == age_group) & (rda_df["sex"] == sex) & (rda_df["activity_level"] == activity)
    rda_row = rda_df[key]
    if rda_row.empty:
        st.warning("해당 조건의 RDA 기준이 없습니다. rda_reference.csv를 확인하세요.")
    else:
        r = rda_row.iloc[0]
        st.info("현재 RDA 기준 (요약)")
        st.dataframe(pd.DataFrame(r[NUTR_COLS]).T)
        if sel_df.empty:
            st.info("음식을 선택하면 1회 제공량 기준 RDA 대비를 볼 수 있어요.")
        else:
            for _, row in sel_df.iterrows():
                pct = (row[NUTR_COLS] / (r[NUTR_COLS].replace(0, np.nan))) * 100
                pct = pct.fillna(0).clip(upper=300)
                p_df = pd.DataFrame({"nutrient": NUTR_COLS, "pct_RDA": pct.values})
                st.markdown(f"**{row['food_name']} — RDA 충족률(%)**")
                fig = px.bar(p_df, x="nutrient", y="pct_RDA")
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# ✨ 추천 (유사도/목표 영양소)
# -------------------------------------------------
with t_reco:
    st.subheader("대체 음식 추천 (영양소 유사도 + 목표)")
    target = st.selectbox("보강/감소하고 싶은 영양소", NUTR_COLS)
    mode = st.radio("목표", ["보강", "감소"], horizontal=True)

    if sel_df.empty:
        st.info("음식을 1개 선택하면 해당 음식 기준으로 추천을 계산합니다.")
    else:
        base = sel_df.iloc[0]
        X = foods_df[NUTR_COLS].fillna(0).values
        base_vec = base[NUTR_COLS].fillna(0).values.reshape(1, -1)
        sim = cosine_similarity(base_vec, X).flatten()

        cand = foods_df.copy()
        cand["similarity"] = sim
        if mode == "보강":
            cand = cand.sort_values([target, "similarity"], ascending=[False, False])
        else:
            cand = cand.sort_values([target, "similarity"], ascending=[True, False])
        out = cand[cand["food_name"] != base["food_name"]].head(12)[["food_name","category",target,"similarity"]]
        st.dataframe(out, use_container_width=True)

        # 다운로드
        st.download_button(
            "추천 결과 CSV 다운로드",
            out.to_csv(index=False).encode("utf-8"),
            file_name="recommendations.csv",
            mime="text/csv"
        )

# -------------------------------------------------
# 🧪 상관분석
# -------------------------------------------------
with t_corr:
    st.subheader("영양소 간 상관 히트맵 (Pearson)")
    corr = foods_df[NUTR_COLS].corr(method="pearson")
    fig = px.imshow(corr, text_auto=False, aspect="auto", title="Correlation (Pearson)")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# 푸터/도움말
# -------------------------------------------------
st.divider()
st.markdown(
    """
**사용 팁**  
- 좌측에서 CSV 업로드 또는 데모 데이터로 바로 체험할 수 있어요.  
- RDA 프로필을 바꾸면 진단 결과가 달라집니다.  
- 추천 탭에서 첫 번째 선택 음식이 기준이 됩니다.  
    """
)

st.toast("Nutrition Insight loaded.", icon="🥗")

