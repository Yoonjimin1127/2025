import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine\_similarity
import io

st.set\_page\_config(page\_title="Nutrition Insight", page\_icon="🥗", layout="wide")

# CSV 로딩 (경로 기반)

@st.cache\_data
def load\_csv\_path(path: str):
return pd.read\_csv(path)

st.title("🥗 Nutrition Insight — 식품 영양 분석 대시보드")
st.caption("공개 데이터 기반 영양소 비교 · RDA 대비 진단 · 대체 음식 추천")

# 파일 업로드 or 경로 입력

uploaded\_foods = st.sidebar.file\_uploader("음식 CSV 업로드")
foods\_path = st.sidebar.text\_input("Foods CSV path (or leave empty if uploaded)", "")
uploaded\_rda = st.sidebar.file\_uploader("RDA CSV 업로드")
rda\_path = st.sidebar.text\_input("RDA CSV path (or leave empty if uploaded)", "")

age\_group = st.sidebar.selectbox("Age Group", \["14-18", "19-29", "30-49", "50-64"])
sex = st.sidebar.selectbox("Sex", \["M", "F"])
activity = st.sidebar.selectbox("Activity Level", \["low", "moderate", "high"])

try:
if uploaded\_foods:
foods = pd.read\_csv(uploaded\_foods)
elif foods\_path:
foods = load\_csv\_path(foods\_path)
else:
st.stop()

```
if uploaded_rda:
    rda = pd.read_csv(uploaded_rda)
elif rda_path:
    rda = load_csv_path(rda_path)
else:
    st.stop()
```

except Exception as e:
st.error(f"데이터 로드 오류: {e}")
st.stop()

nutr\_cols = \[
"calories\_kcal","carb\_g","protein\_g","fat\_g","fiber\_g","sugars\_g",
"vitA\_µg","vitC\_mg","vitD\_µg","vitE\_mg","vitK\_µg",
"calcium\_mg","iron\_mg","zinc\_mg","magnesium\_mg","potassium\_mg","sodium\_mg"
]

q = st.text\_input("음식 검색", "banana")
filtered = foods\[foods\["food\_name"].str.contains(q, case=False, na=False)]
choices = st.multiselect("음식 선택(최대 5개)", filtered\["food\_name"].tolist(), max\_selections=5)
sel\_df = foods\[foods\["food\_name"].isin(choices)]

t\_overview, t\_compare, t\_rda, t\_reco, t\_corr = st.tabs(\["📊 개요", "⚖️ 비교", "🧭 RDA 진단", "✨ 추천", "🧪 상관분석"])

with t\_overview:
st.subheader("선택한 음식의 영양 성분")
if not sel\_df.empty:
long = sel\_df.melt(id\_vars=\["food\_name"], value\_vars=nutr\_cols, var\_name="nutrient", value\_name="amount")
fig = px.bar(long, x="nutrient", y="amount", color="food\_name", barmode="group")
fig.update\_layout(xaxis\_tickangle=-45)
st.plotly\_chart(fig, use\_container\_width=True)
else:
st.info("왼쪽에서 음식을 검색/선택하세요.")

with t\_compare:
st.subheader("정규화 비교")
if not sel\_df.empty:
scaler = StandardScaler()
X = scaler.fit\_transform(sel\_df\[nutr\_cols])
zdf = pd.DataFrame(X, columns=nutr\_cols, index=sel\_df\["food\_name"]).reset\_index().melt(
id\_vars=\["food\_name"], var\_name="nutrient", value\_name="z"
)
fig = px.bar(zdf, x="nutrient", y="z", color="food\_name", barmode="group")
fig.update\_layout(xaxis\_tickangle=-45)
st.plotly\_chart(fig, use\_container\_width=True)
else:
st.info("음식을 선택하면 비교할 수 있어요.")

with t\_rda:
st.subheader("RDA 대비 진단")
key = (rda\["age\_group"] == age\_group) & (rda\["sex"] == sex) & (rda\["activity\_level"] == activity)
rda\_row = rda\[key]
if not rda\_row\.empty and not sel\_df.empty:
r = rda\_row\.iloc\[0]
for \_, row in sel\_df.iterrows():
pct = (row\[nutr\_cols] / (r\[nutr\_cols].replace(0, np.nan))) \* 100
pct = pct.clip(upper=300)
p\_df = pd.DataFrame({"nutrient": nutr\_cols, "pct\_RDA": pct.values})
st.markdown(f"**{row\['food\_name']} — RDA 충족률(%)**")
fig = px.bar(p\_df, x="nutrient", y="pct\_RDA")
fig.update\_layout(xaxis\_tickangle=-45)
st.plotly\_chart(fig, use\_container\_width=True)
else:
st.info("음식 선택 또는 RDA 데이터 확인 필요.")

with t\_reco:
st.subheader("대체 음식 추천")
if not sel\_df.empty:
target\_nutrient = st.selectbox("보강/감소하고 싶은 영양소", nutr\_cols)
mode = st.radio("목표", \["보강", "감소"], horizontal=True)
base = sel\_df.iloc\[0]
X = foods\[nutr\_cols].fillna(0).values
base\_vec = base\[nutr\_cols].fillna(0).values.reshape(1, -1)
sim = cosine\_similarity(base\_vec, X).flatten()
foods\["similarity"] = sim
if mode == "보강":
cand = foods.sort\_values(\[target\_nutrient, "similarity"], ascending=\[False, False])
else:
cand = foods.sort\_values(\[target\_nutrient, "similarity"], ascending=\[True, False])
out = cand\[cand\["food\_name"] != base\["food\_name"]].head(10)\[\["food\_name", target\_nutrient, "similarity"]]
st.dataframe(out, use\_container\_width=True)
else:
st.info("음식을 선택하면 추천을 볼 수 있습니다.")

with t\_corr:
st.subheader("영양소 간 상관 히트맵")
corr = foods\[nutr\_cols].corr(method="pearson")
fig = px.imshow(corr, text\_auto=False, aspect="auto", title="Correlation")
st.plotly\_chart(fig, use\_container\_width=True)
