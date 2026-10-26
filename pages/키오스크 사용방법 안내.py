
import streamlit as st

# =====================================
# 1. 페이지 설정
# =====================================
st.set_page_config(
    page_title="키오스크 사용법 안내",
    page_icon="☕",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =====================================
# 2. 디자인 설정: 하늘색 + 파란색
# =====================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #EAF6FF;
        color: #183247;
    }

    [data-testid="stHeader"] {
        background-color: #EAF6FF;
    }

    .main .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #124A78 !important;
    }

    p {
        color: #183247;
    }

    .intro-card {
        background-color: #FFFFFF;
        border: 2px solid #9CCFF2;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .screen-card {
        background-color: #FFFFFF;
        border: 2px solid #78B8E8;
        border-radius: 18px;
        padding: 20px;
        margin: 15px 0;
    }

    .help-card {
        background-color: #D9EEFF;
        border-left: 7px solid #1677B8;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        font-size: 1.1rem;
        line-height: 1.8;
    }

    div.stButton > button {
        min-height: 55px;
        border-radius: 12px;
        border: 2px solid #287DB5;
        background-color: #FFFFFF;
        color: #124A78;
        font-size: 17px;
        font-weight: bold;
    }

    div.stButton > button:hover {
        background-color: #D9EEFF;
        color: #124A78;
        border-color: #1677B8;
    }

    div[data-testid="stProgressBar"] > div > div {
        background-color: #1677B8;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================
# 3. 메뉴 데이터
# =====================================
MENU_INFO = {
    "따뜻한 아메리카노": {
        "price": 2500,
        "emoji": "☕",
    },
    "아이스 아메리카노": {
        "price": 3000,
        "emoji": "🧊",
    },
    "카페라떼": {
        "price": 3500,
        "emoji": "🥛",
    },
    "녹차": {
        "price": 3000,
        "emoji": "🍵",
    },
}

STEPS = [
    "메뉴 선택",
    "옵션 선택",
    "주문 확인",
    "결제",
    "주문 완료",
]

# =====================================
# 4. 주문 초기화
# =====================================
def reset_order():
    st.session_state["step"] = 0
    st.session_state["menu"] = "따뜻한 아메리카노"
    st.session_state["temperature"] = "따뜻하게"
    st.session_state["size"] = "보통"
    st.session_state["quantity"] = 1
    st.session_state["payment"] = "카드"
    st.session_state["confirmed"] = False


if "step" not in st.session_state:
    reset_order()

# =====================================
# 5. 가격 계산
# =====================================
def calculate_total():
    menu = st.session_state["menu"]

    price = MENU_INFO[menu]["price"]

    if st.session_state["size"] == "크게":
        price += 500

    quantity = st.session_state["quantity"]

    return price * quantity


# =====================================
# 6. 주문 내역 표시
# =====================================
def show_order():
    menu = st.session_state["menu"]
    info = MENU_INFO[menu]
    total = calculate_total()

    st.markdown(
        f"""
        <div class="screen-card">
            <h3>🧾 주문 내역</h3>
            <p style="font-size:21px;">
                {info["emoji"]} <b>{menu}</b>
            </p>
            <p style="font-size:17px;">
                온도: {st.session_state["temperature"]}
            </p>
            <p style="font-size:17px;">
                크기: {st.session_state["size"]}
            </p>
            <p style="font-size:17px;">
                수량: {st.session_state["quantity"]}잔
            </p>
            <hr>
            <p style="font-size:25px;">
                총 금액: <b>{total:,}원</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =====================================
# 7. 앱 첫 화면
# =====================================
st.title("☕ 천천히 배우는 키오스크")

st.markdown(
    """
    <div class="intro-card">
        <h3>💙 어르신을 위한 키오스크 연습</h3>
        <p style="font-size:18px; line-height:1.8;">
            처음 사용해도 괜찮습니다!<br>
            화면을 천천히 읽고 버튼을 눌러 보세요.<br>
            메뉴 선택부터 주문 완료까지 연습할 수 있습니다.
        </p>
        <p>
            ※ 실제 주문이나 결제는 발생하지 않습니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================================
# 8. 진행 상황
# =====================================
current_step = st.session_state["step"]

st.progress(
    (current_step + 1) / len(STEPS),
    text=(
        f"{current_step + 1}단계 / {len(STEPS)}단계"
        f" · {STEPS[current_step]}"
    ),
)

with st.expander("📘 키오스크 사용 순서 보기"):
    st.write("① 메뉴 선택")
    st.write("② 옵션 선택")
    st.write("③ 주문 확인")
    st.write("④ 결제")
    st.write("⑤ 주문 완료")

# =====================================
# 9. 1단계: 메뉴 선택
# =====================================
if current_step == 0:

    st.header("1️⃣ 메뉴를 선택하세요")

    st.write("마시고 싶은 음료를 눌러 주세요.")

    menu_names = list(MENU_INFO.keys())
    columns = st.columns(2)

    for i, menu_name in enumerate(menu_names):

        info = MENU_INFO[menu_name]

        selected = (
            st.session_state["menu"] == menu_name
        )

        prefix = "✅ " if selected else ""

        button_text = (
            f"{prefix}{info['emoji']} {menu_name}\n\n"
            f"{info['price']:,}원"
        )

        with columns[i % 2]:

            if st.button(
                button_text,
                key=f"menu_button_{i}",
                use_container_width=True,
            ):
                st.session_state["menu"] = menu_name
                st.rerun()

    st.markdown(
        """
        <div class="help-card">
            💡 도움말<br>
            원하는 음료를 한 번 눌러 주세요.<br>
            다른 음료를 선택하고 싶다면
            해당 음료를 다시 누르면 됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

# =====================================
# 10. 2단계: 옵션 선택
# =====================================
elif current_step == 1:

    st.header("2️⃣ 음료 옵션을 선택하세요")

    st.write("원하는 온도와 컵 크기, 수량을 선택하세요.")

    st.markdown(
        """
        <div class="screen-card">
            <h3>🌡️ 온도 선택</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.radio(
        "온도를 선택하세요.",
        ["따뜻하게", "차갑게"],
        key="temperature",
        horizontal=True,
    )

    st.markdown(
        """
        <div class="screen-card">
            <h3>🥤 컵 크기 선택</h3>
            <p>큰 컵은 500원이 추가됩니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.radio(
        "컵 크기를 선택하세요.",
        ["보통", "크게"],
        key="size",
        horizontal=True,
    )

    st.markdown(
        """
        <div class="screen-card">
            <h3>🔢 주문 수량 선택</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.selectbox(
        "몇 잔 주문할까요?",
        [1, 2, 3, 4, 5],
        key="quantity",
    )

    st.info(
        f"예상 금액: {calculate_total():,}원"
    )

# =====================================
# 11. 3단계: 주문 확인
# =====================================
elif current_step == 2:

    st.header("3️⃣ 주문 내용을 확인하세요")

    st.write(
        "선택한 메뉴와 금액이 맞는지 확인하세요."
    )

    show_order()

    st.checkbox(
        "주문 내용이 맞는지 확인했습니다.",
        key="confirmed",
    )

    if not st.session_state["confirmed"]:
        st.warning(
            "주문 내용이 맞으면 확인란을 눌러 주세요."
        )

# =====================================
# 12. 4단계: 결제 연습
# =====================================
elif current_step == 3:

    st.header("4️⃣ 결제 방법을 선택하세요")

    st.write(
        "연습할 결제 방법을 선택하세요."
    )

    st.radio(
        "결제 방법",
        [
            "카드",
            "간편결제",
            "현금(직원에게 문의)",
        ],
        key="payment",
    )

    show_order()

    st.markdown(
        """
        <div class="help-card">
            💡 결제할 때 기억하세요!<br>
            실제 키오스크에서는 화면의 안내에 따라
            카드를 넣거나 카드 단말기에 대세요.<br>
            어려우면 직원에게 도움을 요청해도 괜찮습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

# =====================================
# 13. 5단계: 주문 완료
# =====================================
elif current_step == 4:

    st.header("5️⃣ 주문이 완료되었습니다!")

    show_order()

    st.markdown(
        f"""
        <div class="screen-card" style="text-align:center;">
            <div style="font-size:65px;">🎉</div>
            <h2>주문 완료!</h2>
            <p style="font-size:22px;">
                주문 번호: <b>001</b>
            </p>
            <p style="font-size:18px;">
                결제 연습 방법:
                {st.session_state["payment"]}
            </p>
            <p style="font-size:17px;">
                실제 매장에서는 주문 번호나 영수증을 확인하고
                음료를 기다리세요.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.success(
        "축하합니다! 모든 단계를 연습했습니다. 💙"
    )

    st.caption(
        "연습용 화면이므로 실제 주문이나 결제는 없습니다."
    )

# =====================================
# 14. 단계 이동 버튼
# =====================================
st.divider()

left, middle, right = st.columns(3)

with left:

    if st.button(
        "⬅️ 이전 단계",
        disabled=(current_step == 0),
        use_container_width=True,
    ):
        st.session_state["step"] -= 1
        st.rerun()

with middle:

    if st.button(
        "🔄 처음부터 다시",
        use_container_width=True,
    ):
        reset_order()
        st.rerun()

with right:

    if st.button(
        "다음 단계 ➡️",
        disabled=(current_step == 4),
        type="primary",
        use_container_width=True,
    ):

        if current_step == 2:
            if not st.session_state["confirmed"]:
                st.warning(
                    "주문 확인란을 먼저 눌러 주세요."
                )
            else:
                st.session_state["step"] += 1
                st.rerun()

        else:
            st.session_state["step"] += 1
            st.rerun()

st.caption(
    "천천히 연습하세요. 모르는 부분은 직원에게 도움을 요청해도 됩니다. 💙"
)
