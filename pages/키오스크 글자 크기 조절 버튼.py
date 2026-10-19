
import streamlit as st

st.set_page_config(
    page_title="어르신을 위한 쉬운 키오스크",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# 1. 메뉴 및 가격
# -----------------------------
PRODUCTS = {
    "식사류": [
        {"name": "김치볶음밥", "price": 7000, "emoji": "🍚"},
        {"name": "잔치국수", "price": 6000, "emoji": "🍜"},
    ],
    "음료": [
        {"name": "아메리카노", "price": 3000, "emoji": "☕"},
        {"name": "카페라떼", "price": 4000, "emoji": "🥛"},
    ],
    "분식": [
        {"name": "떡볶이", "price": 5000, "emoji": "🍲"},
        {"name": "햄버거", "price": 6000, "emoji": "🍔"},
    ],
    "디저트": [
        {"name": "케이크", "price": 4500, "emoji": "🍰"},
        {"name": "아이스크림", "price": 3000, "emoji": "🍦"},
    ],
}

FONT_SIZES = {
    "보통": 18,
    "크게": 24,
    "아주 크게": 30,
}

# -----------------------------
# 2. 상태 초기화
# -----------------------------
if "font_choice" not in st.session_state:
    st.session_state.font_choice = "보통"

if "show_font_options" not in st.session_state:
    st.session_state.show_font_options = False

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "notice" not in st.session_state:
    st.session_state.notice = ""

if "receipt" not in st.session_state:
    st.session_state.receipt = None

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "식사류"

font_px = FONT_SIZES[st.session_state.font_choice]

# 메뉴 이름으로 가격 찾기
PRICE_LOOKUP = {
    product["name"]: product["price"]
    for items in PRODUCTS.values()
    for product in items
}

# -----------------------------
# 3. 화면 디자인
# -----------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #F3F7FC;
        color: #17324F;
    }}

    .block-container {{
        max-width: 1100px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }}

    h1 {{
        font-size: {font_px * 1.6}px !important;
        color: #174A8B !important;
    }}

    h2 {{
        font-size: {font_px * 1.35}px !important;
        color: #174A8B !important;
    }}

    h3 {{
        font-size: {font_px * 1.15}px !important;
        color: #174A8B !important;
    }}

    p, label, [data-testid="stMarkdownContainer"] p {{
        font-size: {font_px}px !important;
    }}

    div.stButton > button {{
        min-height: 58px;
        width: 100%;
        border: 2px solid #C5D7EB;
        border-radius: 12px;
        background-color: #FFFFFF;
        color: #173B64;
        font-size: {font_px}px !important;
        font-weight: 700;
        white-space: normal;
    }}

    div.stButton > button[kind="primary"] {{
        background-color: #2673D9;
        color: #FFFFFF;
        border-color: #2673D9;
    }}

    [data-testid="stAlert"] {{
        font-size: {font_px}px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 4. 메뉴 담기 / 수량 변경
# -----------------------------
def add_to_cart(name):
    st.session_state.cart[name] = (
        st.session_state.cart.get(name, 0) + 1
    )
    st.session_state.notice = f"{name}을(를) 장바구니에 담았습니다."
    st.session_state.receipt = None


def remove_one(name):
    if name in st.session_state.cart:
        st.session_state.cart[name] -= 1

        if st.session_state.cart[name] <= 0:
            del st.session_state.cart[name]


def calculate_total():
    return sum(
        PRICE_LOOKUP[name] * quantity
        for name, quantity in st.session_state.cart.items()
    )


# -----------------------------
# 5. 상단 화면
# -----------------------------
st.title("🏪 무인 주문 키오스크")
st.write("환영합니다! 원하시는 메뉴를 선택해 주세요.")

st.divider()

# -----------------------------
# 6. 글자 크기 조절
# -----------------------------
st.subheader("🔎 글자 크기 조절")

font_col1, font_col2 = st.columns([2, 3])

with font_col1:
    if st.button(
        "Aa  글자 크기",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.show_font_options = (
            not st.session_state.show_font_options
        )
        st.rerun()

with font_col2:
    st.info(f"현재 글자 크기: {st.session_state.font_choice}")

if st.session_state.show_font_options:
    size_cols = st.columns(3)

    for index, size_name in enumerate(FONT_SIZES):
        with size_cols[index]:
            if st.button(
                size_name,
                key=f"font_size_{size_name}",
                type=(
                    "primary"
                    if st.session_state.font_choice == size_name
                    else "secondary"
                ),
                use_container_width=True,
            ):
                st.session_state.font_choice = size_name
                st.rerun()

st.divider()

# -----------------------------
# 7. 카테고리 선택
# -----------------------------
st.header("1. 메뉴 선택")

category_cols = st.columns(4)

for index, category in enumerate(PRODUCTS):
    with category_cols[index]:
        if st.button(
            category,
            key=f"category_{category}",
            type=(
                "primary"
                if st.session_state.selected_category == category
                else "secondary"
            ),
            use_container_width=True,
        ):
            st.session_state.selected_category = category
            st.rerun()

selected = st.session_state.selected_category
st.subheader(f"🍽️ {selected} 메뉴")

products = PRODUCTS[selected]
product_cols = st.columns(2)

for index, product in enumerate(products):
    with product_cols[index]:
        st.markdown(f"### {product['emoji']} {product['name']}")
        st.write(f"가격: {product['price']:,}원")

        if st.button(
            f"🛒 {product['name']} 담기",
            key=f"add_{product['name']}",
            use_container_width=True,
        ):
            add_to_cart(product["name"])
            st.rerun()

if st.session_state.notice:
    st.success(st.session_state.notice)

st.divider()

# -----------------------------
# 8. 장바구니
# -----------------------------
st.header("2. 🛒 장바구니")

if not st.session_state.cart:
    st.info("장바구니가 비어 있습니다. 메뉴를 먼저 선택해 주세요.")

else:
    for name in list(st.session_state.cart.keys()):
        quantity = st.session_state.cart[name]
        price = PRICE_LOOKUP[name]
        subtotal = price * quantity

        item_col, minus_col, quantity_col, plus_col = st.columns(
            [4, 1, 1, 1]
        )

        with item_col:
            st.write(f"**{name}**")
            st.write(
                f"{price:,}원 × {quantity}개 = {subtotal:,}원"
            )

        with minus_col:
            if st.button("−", key=f"minus_{name}"):
                remove_one(name)
                st.rerun()

        with quantity_col:
            st.write(f"**{quantity}**")

        with plus_col:
            if st.button("+", key=f"plus_{name}"):
                add_to_cart(name)
                st.rerun()

    total = calculate_total()

    st.markdown(f"## 총 구매 금액: {total:,}원")

    clear_col, buy_col = st.columns(2)

    with clear_col:
        if st.button(
            "🗑️ 장바구니 비우기",
            use_container_width=True,
        ):
            st.session_state.cart = {}
            st.session_state.notice = "장바구니를 비웠습니다."
            st.session_state.receipt = None
            st.rerun()

    with buy_col:
        if st.button(
            "🛍️ 구매하기",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.receipt = {
                "items": dict(st.session_state.cart),
                "total": total,
            }
            st.session_state.cart = {}
            st.session_state.notice = ""
            st.rerun()

# -----------------------------
# 9. 구매 완료 화면
# -----------------------------
if st.session_state.receipt is not None:
    receipt = st.session_state.receipt

    st.divider()
    st.success("✅ 구매가 완료되었습니다!")

    st.subheader("구매 내역")

    for name, quantity in receipt["items"].items():
        price = PRICE_LOOKUP[name]
        st.write(
            f"- {name} × {quantity}개 "
            f"= {price * quantity:,}원"
        )

    st.markdown(f"## 결제 예정 금액: {receipt['total']:,}원")

    st.info(
        "수행평가 시연용 구매 완료 화면입니다. "
        "실제 결제나 주문 전송은 이루어지지 않습니다."
    )

    if st.button("처음 화면으로 돌아가기", type="primary"):
        st.session_state.receipt = None
        st.session_state.notice = ""
        st.session_state.selected_category = "식사류"
        st.rerun()

st.divider()
st.caption("어르신을 위한 쉬운 키오스크 · 체험용 앱")
