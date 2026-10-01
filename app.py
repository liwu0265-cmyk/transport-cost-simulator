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

    .result-card {
        border: 1px solid #d9dde3;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        background-color: #ffffff;
    }

    .result-title {
        font-size: 0.9rem;
        color: #555;
        margin-bottom: 4px;
    }

    .result-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .result-sub {
        font-size: 0.9rem;
        color: #666;
        margin-top: 4px;
    }

    .cost-item {
        border: 1px solid #e0e3e7;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 10px;
        background-color: #ffffff;
    }

    .cost-name {
        font-size: 0.95rem;
        font-weight: 600;
    }

    .cost-value {
        font-size: 1rem;
        font-weight: 700;
        text-align: right;
    }

    .cost-ratio {
        font-size: 0.82rem;
        color: #6b7280;
        margin-top: 3px;
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

        # 車両番号を手入力に変更
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

# 1km当たり原価
if distance > 0:
    cost_per_km = total_cost / distance
else:
    cost_per_km = 0

# 1t当たり原価
if load_weight > 0:
    cost_per_ton = total_cost / load_weight
else:
    cost_per_ton = 0

# 運賃検討額
# 利益率は原価に対する上乗せ率
freight_price = total_cost * (1 + profit_rate / 100)

# 運賃 / km
if distance > 0:
    freight_per_km = freight_price / distance
else:
    freight_per_km = 0

# 運賃 / t
if load_weight > 0:
    freight_per_ton = freight_price / load_weight
else:
    freight_per_ton = 0

# =========================================================
# 右側：計算結果
# =========================================================
with right:

    st.subheader("計算結果")

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-title">
                輸送原価合計
            </div>

            <div class="result-value">
                ¥{total_cost:,.0f}
            </div>

            <div class="result-sub">
                1km当たり原価：
                ¥{cost_per_km:,.0f}/km
            </div>

            <div class="result-sub">
                1t当たり原価：
                ¥{cost_per_ton:,.0f}/t
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-title">
                運賃検討額
            </div>

            <div class="result-value">
                ¥{freight_price:,.0f}
            </div>

            <div class="result-sub">
                運賃換算：
                ¥{freight_per_km:,.0f}/km
            </div>

            <div class="result-sub">
                積載量換算：
                ¥{freight_per_ton:,.0f}/t
            </div>
        </div>
        """,
        unsafe_allow_html=True
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

    html = f"""
    <div class="cost-item">

        <div style="
            display:flex;
            justify-content:space-between;
        ">

            <div class="cost-name">
                {name}
            </div>

            <div class="cost-value">
                ¥{amount:,.0f}
            </div>

        </div>

        <div class="cost-ratio">
            原価構成比 {ratio:.1f}%
        </div>

    </div>
    """

    if i % 2 == 0:

        with col_a:
            st.markdown(
                html,
                unsafe_allow_html=True
            )

    else:

        with col_b:
            st.markdown(
                html,
                unsafe_allow_html=True
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