
import streamlit as st

st.set_page_config(
    page_title="키오스크 도우미",
    page_icon="🖐️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 세션 상태 초기화
if "font_size" not in st.session_state:
    st.session_state.font_size = 22

if "step" not in st.session_state:
    st.session_state.step = 0

# 안내 자료
GUIDES = {
    "음식 주문하기": [
        ("주문 시작", "화면에서 '주문하기' 또는 '매장 식사' 버튼을 찾아 눌러 주세요."),
        ("메뉴 고르기", "원하는 음식 사진이나 메뉴 이름을 누르세요."),
        ("수량 확인", "주문할 음식과 개수를 확인하고 '담기' 또는 '주문하기'를 누르세요."),
        ("주문 확인", "장바구니에서 메뉴와 금액을 확인한 뒤 '결제하기'를 누르세요."),
        ("결제하기", "화면의 결제 안내에 따라 카드나 다른 결제 수단을 이용하세요."),
        ("주문 완료", "주문 번호나 영수증을 확인하고 음식이 나올 때까지 기다리세요."),
    ],
    "기차표 예매하기": [
        ("출발지와 도착지", "출발역과 도착역을 선택하세요."),
        ("날짜와 시간", "원하는 날짜와 출발 시간을 선택하세요."),
        ("열차 선택", "열차 시간과 요금을 확인하고 원하는 열차를 누르세요."),
        ("좌석 선택", "좌석 선택 화면이 나오면 원하는 좌석을 선택하세요."),
        ("결제하기", "예약 정보와 금액을 확인한 후 안내에 따라 결제하세요."),
        ("예매 완료", "승차권과 열차 시간, 좌석 정보를 확인하세요."),
    ],
    "무인민원발급기 이용하기": [
        ("민원 선택", "화면에서 필요한 증명서 종류를 선택하세요."),
        ("본인 확인", "화면의 안내에 따라 본인 확인 절차를 진행하세요."),
        ("항목 확인", "발급 내용과 필요한 정보를 확인하세요."),
        ("수수료 확인", "발급 수수료가 있는지 확인하세요."),
        ("발급하기", "화면 안내에 따라 발급을 진행하세요."),
        ("서류 확인", "출력된 서류를 챙기고 개인정보가 남지 않았는지 확인하세요."),
    ],
}

def show_notice(message):
    st.info(message)

# 글자 크기와 공통 스타일
font_size = st.session_state.font_size
st.markdown(
    f"""
    <style>
    html, body, [class*="css"] {{
        font-size: {font_size}px;
    }}
    .main .block-container {{
        max-width: 850px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}
    div.stButton > button {{
        min-height: 3.2rem;
        border-radius: 12px;
        font-size: 1.05rem;
        font-weight: 600;
        width: 100%;
    }}
    div[data-testid="stRadio"] label {{
        padding-top: 0.3rem;
        padding-bottom: 0.3rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# 상단 제목
st.title("🖐️ 키오스크 도우미")
st.write("천천히 따라 해 보세요. 누구나 쉽게 이용할 수 있어요.")
st.divider()

# 글자 크기 설정
with st.expander("🔎 글자 크기 바꾸기", expanded=False):
    st.write("읽기 편한 크기로 조절해 주세요.")
    st.slider(
        "글자 크기",
        min_value=16,
        max_value=32,
        step=2,
        key="font_size",
        format="%d px",
    )
    st.caption("글자 크기는 16px부터 32px까지 바꿀 수 있어요.")

# 메뉴
page = st.radio(
    "원하는 도움을 선택하세요.",
    [
        "🏠 처음 화면",
        "📖 사용 방법 배우기",
        "🙋 도움이 필요해요",
    ],
    horizontal=False,
    label_visibility="visible",
)

st.divider()

if page == "🏠 처음 화면":
    st.header("무엇을 도와드릴까요?")
    st.write("아래에서 필요한 항목을 선택하세요.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🍽️")
        st.subheader("음식 주문")
        st.write("식당이나 카페에서 주문하는 방법")
        if st.button("음식 주문 배우기", key="home_food"):
            st.session_state.selected_guide = "음식 주문하기"
            st.session_state.step = 0
            st.session_state.home_action = "guide"

    with col2:
        st.markdown("### 🚆")
        st.subheader("기차표 예매")
        st.write("기차표를 예매하는 순서")
        if st.button("기차표 예매 배우기", key="home_train"):
            st.session_state.selected_guide = "기차표 예매하기"
            st.session_state.step = 0
            st.session_state.home_action = "guide"

    st.markdown("### 🏢")
    st.subheader("민원서류 발급")
    st.write("무인민원발급기를 이용하는 방법")
    if st.button("민원서류 발급 배우기", key="home_civil"):
        st.session_state.selected_guide = "무인민원발급기 이용하기"
        st.session_state.step = 0
        st.session_state.home_action = "guide"

    if st.session_state.get("home_action") == "guide":
        st.session_state.home_action = None
        st.rerun()

    st.divider()
    st.success("💡 잘 모르겠다면 '사용 방법 배우기'에서 한 단계씩 확인하세요.")

elif page == "📖 사용 방법 배우기":
    st.header("📖 사용 방법 배우기")
    guide_name = st.selectbox(
        "어떤 사용 방법을 알아볼까요?",
        list(GUIDES.keys()),
        key="guide_select",
    )

    steps = GUIDES[guide_name]
    st.session_state.step = min(
        max(st.session_state.step, 0), len(steps) - 1
    )

    # 선택한 안내가 바뀌면 첫 단계부터 시작
    if st.session_state.get("last_guide") != guide_name:
        st.session_state.step = 0
        st.session_state.last_guide = guide_name

    current = st.session_state.step
    title, description = steps[current]

    st.progress((current + 1) / len(steps))
    st.caption(f"전체 {len(steps)}단계 중 {current + 1}단계")

    st.markdown(f"## {current + 1}. {title}")
    st.info(description)

    st.write("### 전체 순서")
    for index, (step_title, _) in enumerate(steps):
        if index == current:
            st.markdown(f"👉 **{index + 1}. {step_title} — 현재 단계**")
        else:
            st.write(f"{index + 1}. {step_title}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 이전 단계", disabled=(current == 0)):
            st.session_state.step -= 1
            st.rerun()

    with col2:
        if st.button(
            "다음 단계 ➡️",
            disabled=(current == len(steps) - 1),
        ):
            st.session_state.step += 1
            st.rerun()

    if current == len(steps) - 1:
        st.success("모든 안내를 확인했어요. 수고하셨습니다!")
        if st.button("처음부터 다시 보기"):
            st.session_state.step = 0
            st.rerun()

elif page == "🙋 도움이 필요해요":
    st.header("🙋 도움이 필요할 때")
    st.write("어떤 상황인지 선택하면 해결 방법을 알려드릴게요.")

    problem = st.radio(
        "현재 겪고 있는 상황은 무엇인가요?",
        [
            "어디를 눌러야 할지 모르겠어요.",
            "화면이 멈췄어요.",
            "결제가 되지 않아요.",
            "주문이나 발급이 끝났는지 모르겠어요.",
        ],
    )

    advice = {
        "어디를 눌러야 할지 모르겠어요.": (
            "화면의 제목과 안내 문구를 천천히 읽어 보세요. "
            "확실하지 않으면 아무 버튼이나 누르지 말고 직원에게 물어보세요."
        ),
        "화면이 멈췄어요.": (
            "버튼을 반복해서 누르지 마세요. 잠시 기다린 뒤에도 화면이 "
            "바뀌지 않으면 직원에게 도움을 요청하세요."
        ),
        "결제가 되지 않아요.": (
            "결제 완료 여부를 먼저 확인하세요. 돈이 빠져나갔는지 확실하지 "
            "않다면 다시 결제하지 말고 직원에게 확인을 요청하세요."
        ),
        "주문이나 발급이 끝났는지 모르겠어요.": (
            "주문 번호, 영수증 또는 출력된 서류를 확인하세요. "
            "완료 여부가 불분명하면 직원에게 확인해 달라고 요청하세요."
        ),
    }

    st.info(advice[problem])

    st.markdown("### 직원에게 이렇게 말해 보세요")
    st.success("“죄송합니다. 키오스크 사용이 어려워서 도움이 필요합니다.”")

    st.caption(
        "이 앱은 안내를 제공하며 실제 직원 호출이나 결제를 대신 수행하지는 않습니다."
    )

st.divider()
st.caption("키오스크 도우미 | 쉽고 편리한 디지털 생활을 위한 안내 서비스")
