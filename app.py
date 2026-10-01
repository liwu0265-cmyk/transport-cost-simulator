import streamlit as st

# =========================================================
# ページ設定
# =========================================================
st.set_page_config(
    page_title="輸送原価シミュレーター",
    layout="wide"
)

# =========================================================
# 見た目の設定
# =========================================================
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1300px;
    }

    h1 {
        font-size: 2.2rem !important;
        margin-bottom: 0.2rem !important;
    }

    h2, h3 {
        margin-top: 1rem !important;
        margin-bottom: 0.8rem !important;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #d9dde3;
        padding: 18px;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.95rem;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# タイトル
# =========================================================
st.title("輸送原価シミュレーター")

st.caption(
    "1運行あたりの原価を入力すると、"
    "輸送原価と運賃検討額を自動計算します。"
)

# =========================================================
# 全体レイアウト
# =========================================================
left, right = st.columns([2.2, 1], gap="large")

# =========================================================
# 左側
# =========================================================
with left:

    # -----------------------------------------------------
    # 運行情報
    # -----------------------------------------------------
    st.subheader("運行情報")

    c1, c2 = st.columns(2)

    with c1:
        vehicle_number = st.text_input(
            "車両番号",
            value="",
            placeholder="例：1450"
        )

        departure = st.text_input(
            "出発地",
            value="",
            placeholder="例：上越環境工場"
        )

        distance = st.number_input(
            "走行距離（km）",
            min_value=0.0,
            value=10.0,
            step=1.0
        )

    with c2:
        destination = st.text_input(
            "到着地",
            value="",
            placeholder="例：吉川工場"
        )

        load_weight = st.number_input(
            "積載量（t）",
            min_value=0.0,
            value=1.0,
            step=0.1
        )

    # -----------------------------------------------------
    # 輸送原価入力
    # -----------------------------------------------------
    st.subheader("輸送原価を入力")

    c1, c2 = st.columns(2)

    with c1:
        fuel = st.number_input(
            "燃料費（円）",
            min_value=0,
            value=450
        )

        labor = st.number_input(
            "人件費（円）",
            min_value=0,
            value=2000
        )

        maintenance = st.number_input(
            "車両維持費（円）",
            min_value=0,
            value=2500
        )

        tire = st.number_input(
            "タイヤ代（円）",
            min_value=0,
            value=0
        )

        depreciation = st.number_input(
            "車両償却費（円）",
            min_value=0,
            value=3000
        )

    with c2:
        highway = st.number_input(
            "高速料金（円）",
            min_value=0,
            value=0
        )

        repair = st.number_input(
            "修繕費（円）",
            min_value=0,
            value=1500
        )

        insurance = st.number_input(
            "保険料（円）",
            min_value=0,
            value=0
        )

        other = st.number_input(
            "その他経費（円）",
            min_value=0,
            value=1000
        )

    profit_rate = st.number_input(
        "利益率（%）",
        min_value=0.0,
        value=15.0,
        step=1.0
    )

# =========================================================
# 計算処理
# =========================================================
total_cost = (
    fuel
    + labor
    + highway
    + maintenance
    + repair
    + tire
    + insurance
    + depreciation
    + other
)

cost_per_km = total_cost / distance if distance > 0 else 0

cost_per_ton = (
    total_cost / load_weight
    if load_weight > 0
    else 0
)

# 利益率は原価に対する上乗せ率
freight_price = total_cost * (1 + profit_rate / 100)

freight_per_km = (
    freight_price / distance
    if distance > 0
    else 0
)

freight_per_ton = (
    freight_price / load_weight
    if load_weight > 0
    else 0
)

# =========================================================
# 右側：計算結果
# =========================================================
with right:

    st.subheader("計算結果")

    with st.container(border=True):

        st.write("輸送原価合計")

        st.markdown(
            f"## ¥{total_cost:,.0f}"
        )

        st.write(
            f"1km当たり原価："
            f"¥{cost_per_km:,.0f}/km"
        )

        st.write(
            f"1t当たり原価："
            f"¥{cost_per_ton:,.0f}/t"
        )

    with st.container(border=True):

        st.write("運賃検討額")

        st.markdown(
            f"## ¥{freight_price:,.0f}"
        )

        st.write(
            f"運賃換算："
            f"¥{freight_per_km:,.0f}/km"
        )

        st.write(
            f"積載量換算："
            f"¥{freight_per_ton:,.0f}/t"
        )

    st.caption(
        "利益率は「原価に対する上乗せ率」"
        "として計算しています。"
    )

# =========================================================
# 原価内訳
# =========================================================
st.divider()

st.subheader("原価内訳")

cost_items = [
    ("車両償却費", depreciation),
    ("車両維持費", maintenance),
    ("人件費", labor),
    ("修繕費", repair),
    ("その他経費", other),
    ("燃料費", fuel),
    ("高速料金", highway),
    ("タイヤ代", tire),
    ("保険料", insurance),
]

col_a, col_b = st.columns(2)

for i, (name, amount) in enumerate(cost_items):

    if total_cost > 0:
        ratio = amount / total_cost * 100
    else:
        ratio = 0

    target = col_a if i % 2 == 0 else col_b

    with target:
        with st.container(border=True):
            c_name, c_value = st.columns([2, 1])

            with c_name:
                st.write(name)

            with c_value:
                st.write(
                    f"**¥{amount:,.0f}**"
                )

            st.caption(
                f"原価構成比 {ratio:.1f}%"
            )

# =========================================================
# 運行情報まとめ
# =========================================================
st.divider()

st.subheader("運行情報まとめ")

summary1, summary2, summary3, summary4, summary5 = st.columns(5)

with summary1:
    st.metric(
        "車両番号",
        vehicle_number if vehicle_number else "未入力"
    )

with summary2:
    st.metric(
        "出発地",
        departure if departure else "未入力"
    )

with summary3:
    st.metric(
        "到着地",
        destination if destination else "未入力"
    )

with summary4:
    st.metric(
        "走行距離",
        f"{distance:,.1f} km"
    )

with summary5:
    st.metric(
        "積載量",
        f"{load_weight:,.1f} t"
    )