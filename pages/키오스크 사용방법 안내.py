import streamlit as st

# 어르신을 위한 키오스크 연습 앱
# 외부 API나 이미지 파일 없이 실행되는 교육용 시뮬레이터입니다.

st.set_page_config(
    page_title="천천히 배우는 키오스크",
    page_icon="☕",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp { background: #FFF9EF; color: #252525; }
    [data-testid="stHeader"] { background: rgba(255,249,239,0.9); }
    .main .block-container { max-width: 850px; padding-top: 1.3rem; padding-bottom: 2rem; }
    h1, h2, h3 { color: #263238; }
    .intro-card {
        background: #FFFFFF; border: 2px solid #E8DCC8; border-radius: 18px;
        padding: 20px; margin: 8px 0 16px 0;
    }
    .screen-card {
        background: #FFFFFF; border: 3px solid #D7C7AF; border-radius: 20px;
        padding: 22px; margin: 12px 0;
    }
    .big-note {
        background: #FFF0C9; border-left: 7px solid #D18B00; border-radius: 10px;
        padding: 14px 16px; font-size: 1.15rem; line-height: 1.6;
    }
    .muted { color: #505050; font-size: 1rem; }
    div.stButton > button {
        min-height: 3.2rem; border-radius: 12px; font-size: 1.1rem;
        font-weight: 700; border: 2px solid #52616B;
    }
    div[data-testid="stRadio"] label, div[data-testid="stCheckbox"] label {
        font-size: 1.08rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

st.title("☕ 천천히 배우는 키오스크")
st.markdown(
    '<div class="intro-card"><h3>실수해도 괜찮아요!</h3>'
    '<p style="font-size:1.15rem;line-height:1.7;">카페 키오스크를 실제처럼 연습해 보는 공간입니다. '
    '화면의 큰 글씨를 읽고, 원하는 항목을 누르세요. 이 앱은 연습용이라 실제 결제나 주문은 발생하지 않습니다.</p>'
    '</div>',
    unsafe_allow_html=True,
)

# 진행 단계 표시
current = st.session_state.step
st.progress((current + 1) / len(STEPS), text=f"연습 {current + 1} / {len(STEPS)}단계 · {STEPS[current]}")

with st.expander("🧭 키오스크 사용 순서 보기", expanded=False):
    st.write("1. 메뉴 선택 → 2. 옵션 선택 → 3. 주문 확인 → 4. 결제 → 5. 주문 완료")
    st.write("화면 아래의 **이전 단계**와 **다음 단계** 버튼으로 천천히 이동할 수 있어요.")

def order_total():
    unit_price = MENU_INFO[st.session_state.menu]["price"]
    if st.session_state.size == "크게":
        unit_price += 500
    return unit_price * int(st.session_state.cup_count)

def show_order_summary():
    menu = st.session_state.menu
    info = MENU_INFO[menu]
    total = order_total()
    st.markdown(
        f"""
        <div class="screen-card">
          <h3>🧾 주문 내역</h3>
          <p style="font-size:1.2rem;">{info['emoji']} <b>{menu}</b></p>
          <p style="font-size:1.05rem;">온도: {st.session_state.temperature}　|　크기: {st.session_state.size}</p>
          <p style="font-size:1.05rem;">수량: {st.session_state.cup_count}잔</p>
          <hr>
          <p style="font-size:1.35rem;">총 금액: <b>{total:,}원</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if current == 0:
    st.header("1단계. 메뉴를 골라 보세요")
    st.write("마시고 싶은 음료 하나를 선택하세요. 메뉴 이름과 가격을 천천히 확인하면 됩니다.")
    cols = st.columns(2)
    menu_names = list(MENU_INFO.keys())
    for i, name in enumerate(menu_names):
        with cols[i % 2]:
            info = MENU_INFO[name]
            selected = st.session_state.menu == name
            label = f"{'✅ ' if selected else ''}{info['emoji']} {name}\n\n{info['price']:,}원"
            if st.button(label, key=f"menu_{i}", use_container_width=True):
                st.session_state.menu = name
                st.rerun()
    st.markdown('<div class="big-note">💡 도움말: 메뉴를 한 번 누르면 선택됩니다. 잘못 눌렀다면 다른 메뉴를 다시 누르세요.</div>', unsafe_allow_html=True)

elif current == 1:
    st.header("2단계. 음료 옵션을 선택하세요")
    st.write("음료를 어떻게 드실지 고릅니다. 잘 모르겠다면 기본 선택을 그대로 두셔도 됩니다.")
    st.markdown('<div class="screen-card"><h3>🌡️ 온도를 선택하세요</h3></div>', unsafe_allow_html=True)
    st.session_state.temperature = st.radio(
        "온도",
        ["따뜻하게", "차갑게"],
        index=["따뜻하게", "차갑게"].index(st.session_state.temperature),
        horizontal=True,
        label_visibility="collapsed",
    )
    st.markdown('<div class="screen-card"><h3>🥤 컵 크기를 선택하세요</h3><p>큰 컵은 500원이 추가됩니다.</p></div>', unsafe_allow_html=True)
    st.session_state.size = st.radio(
        "컵 크기",
        ["보통", "크게"],
        index=["보통", "크게"].index(st.session_state.size),
        horizontal=True,
        label_visibility="collapsed",
    )
    st.markdown('<div class="screen-card"><h3>🔢 수량을 선택하세요</h3></div>', unsafe_allow_html=True)
    st.session_state.cup_count = st.selectbox(
        "몇 잔 주문할까요?",
        [1, 2, 3, 4, 5],
        index=[1, 2, 3, 4, 5].index(int(st.session_state.cup_count)),
    )
    st.info(f"현재 예상 금액은 **{order_total():,}원**입니다.")

elif current == 2:
    st.header("3단계. 주문 내용을 확인하세요")
    st.write("결제하기 전에 메뉴, 옵션, 수량, 금액이 맞는지 살펴보세요.")
    show_order_summary()
    st.session_state.confirmed = st.checkbox(
        "주문 내용이 맞는지 확인했습니다.",
        value=st.session_state.confirmed,
    )
    if not st.session_state.confirmed:
        st.warning("내용이 맞으면 위 확인란을 눌러 주세요. 바꾸고 싶다면 이전 단계로 돌아가면 됩니다.")

elif current == 3:
    st.header("4단계. 결제 방법을 선택하세요")
    st.write("실제 결제는 진행되지 않습니다. 연습할 결제 방법을 선택해 보세요.")
    st.session_state.payment = st.radio(
        "결제 방법",
        ["카드", "간편결제", "현금(직원에게 문의)"],
        index=["카드", "간편결제", "현금(직원에게 문의)"].index(st.session_state.payment),
    )
    show_order_summary()
    st.markdown(
        '<div class="big-note">💡 실제 키오스크에서는 화면의 안내에 따라 카드를 넣거나 대고, '
        '비밀번호 입력 등이 필요하면 주변에 도움을 요청하세요. 이 연습 앱은 카드 정보나 개인정보를 받지 않습니다.</div>',
        unsafe_allow_html=True,
    )

else:
    st.header("5단계. 주문이 완료되었습니다!")
    show_order_summary()
    st.markdown(
        f"""
        <div class="screen-card" style="text-align:center;">
          <div style="font-size:4rem;">🎉</div>
          <h2>주문 완료</h2>
          <p style="font-size:1.25rem;">주문 번호 <b>001</b></p>
          <p style="font-size:1.1rem;">결제 연습 방법: {st.session_state.payment}</p>
          <p style="font-size:1.1rem;">실제 매장에서는 영수증이나 주문 번호를 확인하고 음료를 기다리세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.success("잘하셨어요! 메뉴 선택부터 주문 완료까지 모든 단계를 연습했습니다.")
    st.caption("이 화면은 연습 결과입니다. 실제 주문이나 결제는 이루어지지 않았습니다.")

st.divider()
left, middle, right = st.columns([1, 1, 1])
with left:
    if st.button("⬅️ 이전 단계", disabled=(current == 0), use_container_width=True):
        st.session_state.step = max(0, current - 1)
        st.rerun()
with middle:
    if st.button("처음부터 다시", use_container_width=True):
        reset_order()
        st.rerun()
with right:
    next_disabled = current == len(STEPS) - 1
    if st.button("다음 단계 ➡️", disabled=next_disabled, type="primary", use_container_width=True):
        if current == 2 and not st.session_state.confirmed:
            st.warning("다음 단계로 가기 전에 주문 확인란을 눌러 주세요.")
        else:
            st.session_state.step = min(len(STEPS) - 1, current + 1)
            st.rerun()

st.caption("천천히 하셔도 괜찮습니다. 실제 키오스크에서도 모르는 화면이 나오면 직원에게 도움을 요청해도 됩니다.")
