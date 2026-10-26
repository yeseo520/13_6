```python
import streamlit as st

st.set_page_config(
    page_title="천천히 배우는 키오스크",
    page_icon="☕",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================
# 🎨 하늘색 + 파란색 디자인
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #EAF6FF;
        color: #183247;
    }

    [data-testid="stHeader"] {
        background-color: rgba(234, 246, 255, 0.92);
    }

    .main .block-container {
        max-width: 850px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #124A78;
    }

    p, label {
        color: #183247;
    }

    /* 소개 카드 */
    .intro-card {
        background-color: #FFFFFF;
        border: 2px solid #9CCFF2;
        border-radius: 18px;
        padding: 22px;
        margin: 10px 0 20px 0;
    }

    /* 키오스크 화면 */
    .screen-card {
        background-color: #FFFFFF;
        border: 3px solid #78B8E8;
        border-radius: 20px;
        padding: 22px;
        margin: 12px 0;
    }

    /* 도움말 */
    .big-note {
        background-color: #D9EEFF;
        border-left: 7px solid #1677B8;
        border-radius: 10px;
        padding: 15px;
        font-size: 1.1rem;
        line-height: 1.7;
        color: #183247;
    }

    /* 버튼 */
    div.stButton > button {
        min-height: 3.2rem;
        border-radius: 12px;
        font-size: 1.05rem;
        font-weight: bold;
        border: 2px solid #287DB5;
        background-color: #FFFFFF;
        color: #124A78;
    }

    div.stButton > button:hover {
        background-color: #D9EEFF;
        color: #124A78;
        border-color: #1677B8;
    }

    /* 입력 영역 */
    div[data-testid="stRadio"] label,
    div[data-testid="stCheckbox"] label {
        font-size: 1.05rem;
    }

    /* 진행 막대 */
    div[data-testid="stProgressBar"] > div > div {
        background-color: #1677B8;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# 메뉴 정보
# =========================
STEPS = [
    "메뉴 선택",
    "옵션 선택",
    "주문 확인",
    "결제",
    "주문 완료",
]

MENU_INFO = {
    "따뜻한 아메리카노": {"price": 2500, "emoji": "☕"},
    "아이스 아메리카노": {"price": 3000, "emoji": "🧊"},
    "카페라떼": {"price": 3500, "emoji": "🥛"},
    "녹차": {"price": 3000, "emoji": "🍵"},
}


# =========================
# 주문 초기화
# =========================
def reset_order():
    st.session_state.step = 0
    st.session_state.menu = "따뜻한 아메리카노"
    st.session_state.temperature = "따뜻하게"
    st.session_state.size = "보통"
    st.session_state.cup_count = 1
    st.session_state.payment = "카드"
    st.session_state.confirmed = False


if "step" not in st.session_state:
    reset_order()


# =========================
# 금액 계산
# =========================
def order_total():
    unit_price = MENU_INFO[st.session_state.menu]["price"]

    if st.session_state.size == "크게":
        unit_price += 500

    return unit_price * int(st.session_state.cup_count)


# =========================
# 주문 내역 화면
# =========================
def show_order_summary():
    menu = st.session_state.menu
    info = MENU_INFO[menu]
    total = order_total()

    st.markdown(
        f"""
        <div class="screen-card">
            <h3>🧾 주문 내역</h3>
            <p style="font-size:1.2rem;">
                {info['emoji']} <b>{menu}</b>
            </p>
            <p style="font-size:1.05rem;">
                온도: {st.session_state.temperature}
            </p>
            <p style="font-size:1.05rem;">
                컵 크기: {st.session_state.size}
            </p>
            <p style="font-size:1.05rem;">
                수량: {st.session_state.cup_count}잔
            </p>
            <hr>
            <p style="font-size:1.4rem;">
                총 금액: <b>{total:,}원</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# 앱 제목
# =========================
st.title("☕ 천천히 배우는 키오스크")

st.markdown(
    """
    <div class="intro-card">
        <h3>😊 실수해도 괜찮아요!</h3>
        <p style="font-size:1.15rem; line-height:1.8;">
            이곳에서 카페 키오스크 사용법을 연습할 수 있습니다.<br>
            화면의 안내를 천천히 읽고 원하는 버튼을 눌러 보세요.<br>
            실제 결제나 주문은 발생하지 않습니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================
# 진행 단계
# =========================
current = st.session_state.step

st.progress(
    (current + 1) / len(STEPS),
    text=f"연습 {current + 1} / {len(STEPS)}단계 · {STEPS[current]}",
)

with st.expander("🧭 키오스크 사용 순서 보기"):
    st.write(
        "1. 메뉴 선택 → 2. 옵션 선택 → "
        "3. 주문 확인 → 4. 결제 → 5. 주문 완료"
    )
    st.write("잘못 선택해도 이전 단계로 돌아갈 수 있습니다.")


# =========================
# 1단계: 메뉴 선택
# =========================
if current == 0:

    st.header("1단계. 메뉴를 골라 보세요")
    st.write("마시고 싶은 음료를 선택하세요.")

    cols = st.columns(2)
    menu_names = list(MENU_INFO.keys())

    for i, name in enumerate(menu_names):

        with cols[i % 2]:
            info = MENU_INFO[name]

            selected = st.session_state.menu == name
            prefix = "✅ " if selected else ""

            label = (
                f"{prefix}{info['emoji']} {name}\n\n"
                f"{info['price']:,}원"
            )

            if st.button(
                label,
                key=f"menu_{i}",
                use_container_width=True,
            ):
                st.session_state.menu = name
                st.rerun()

    st.markdown(
        """
        <div class="big-note">
            💡 도움말<br>
            원하는 메뉴를 한 번 누르세요.
            잘못 선택했다면 다른 메뉴를 다시 누르면 됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# 2단계: 옵션 선택
# =========================
elif current == 1:

    st.header("2단계. 음료 옵션을 선택하세요")
    st.write("원하는 온도와 컵 크기, 수량을 선택하세요.")

    st.markdown(
        '<div class="screen-card"><h3>🌡️ 온도 선택</h3></div>',
        unsafe_allow_html=True,
    )

    st.session_state.temperature = st.radio(
        "온도",
        ["따뜻하게", "차갑게"],
        index=["따뜻하게", "차갑게"].index(
            st.session_state.temperature
        ),
        horizontal=True,
        label_visibility="collapsed",
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

    st.session_state.size = st.radio(
        "컵 크기",
        ["보통", "크게"],
        index=["보통", "크게"].index(
            st.session_state.size
        ),
        horizontal=True,
        label_visibility="collapsed",
    )

    st.markdown(
        '<div class="screen-card"><h3>🔢 수량 선택</h3></div>',
        unsafe_allow_html=True,
    )

    st.session_state.cup_count = st.selectbox(
        "몇 잔 주문할까요?",
        [1, 2, 3, 4, 5],
        index=[1, 2, 3, 4, 5].index(
            int(st.session_state.cup_count)
        ),
    )

    st.info(f"현재 예상 금액: {order_total():,}원")


# =========================
# 3단계: 주문 확인
# =========================
elif current == 2:

    st.header("3단계. 주문 내용을 확인하세요")
    st.write("메뉴와 옵션, 수량, 금액이 맞는지 확인하세요.")

    show_order_summary()

    st.session_state.confirmed = st.checkbox(
        "주문 내용이 맞는지 확인했습니다.",
        value=st.session_state.confirmed,
    )

    if not st.session_state.confirmed:
        st.warning(
            "주문 내용이 맞으면 확인란을 눌러 주세요."
        )


# =========================
# 4단계: 결제 연습
# =========================
elif current == 3:

    st.header("4단계. 결제 방법을 선택하세요")

    st.write(
        "연습할 결제 방법을 선택하세요. "
        "실제 결제는 진행되지 않습니다."
    )

    st.session_state.payment = st.radio(
        "결제 방법",
        ["카드", "간편결제", "현금(직원에게 문의)"],
        index=[
            "카드",
            "간편결제",
            "현금(직원에게 문의)",
        ].index(st.session_state.payment),
    )

    show_order_summary()

    st.markdown(
        """
        <div class="big-note">
            💡 결제할 때 기억하세요!<br>
            실제 키오스크에서는 화면의 안내에 따라
            카드를 넣거나 카드 단말기에 대세요.<br>
            어려우면 주변 직원에게 도움을 요청해도 됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# 5단계: 주문 완료
# =========================
else:

    st.header("5단계. 주문이 완료되었습니다!")

    show_order_summary()

    st.markdown(
        f"""
        <div class="screen-card" style="text-align:center;">
            <div style="font-size:4rem;">🎉</div>
            <h2>주문 완료!</h2>
            <p style="font-size:1.25rem;">
                주문 번호 <b>001</b>
            </p>
            <p style="font-size:1.1rem;">
                결제 연습 방법: {st.session_state.payment}
            </p>
            <p style="font-size:1.05rem;">
                실제 매장에서는 주문 번호나 영수증을 확인하고
                음료를 기다리세요.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.success(
        "잘하셨어요! 모든 단계를 성공적으로 연습했습니다."
    )

    st.caption(
        "이 화면은 연습 결과이며 실제 주문이나 결제는 없습니다."
    )


# =========================
# 하단 이동 버튼
# =========================
st.divider()

left, middle, right = st.columns(3)

with left:

    if st.button(
        "⬅️ 이전 단계",
        disabled=(current == 0),
        use_container_width=True,
    ):
        st.session_state.step = max(0, current - 1)
        st.rerun()


with middle:

    if st.button(
        "🔄 처음부터 다시",
        use_container_width=True,
    ):
        reset_order()
        st.rerun()


with right:

    next_disabled = current == len(STEPS) - 1

    if st.button(
        "다음 단계 ➡️",
        disabled=next_disabled,
        type="primary",
        use_container_width=True,
    ):

        if current == 2 and not st.session_state.confirmed:
            st.warning(
                "다음 단계로 가기 전에 주문 확인란을 눌러 주세요."
            )

        else:
            st.session_state.step = min(
                len(STEPS) - 1,
                current + 1,
            )
            st.rerun()


st.caption(
    "천천히 하셔도 괜찮습니다. "
    "모르는 화면이 나오면 직원에게 도움을 요청하세요. 💙"
)
```
