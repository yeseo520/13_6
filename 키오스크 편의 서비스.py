
import streamlit as st

st.set_page_config(
    page_title="편한 키오스크",
    page_icon="🖐️",
    layout="centered",
    initial_sidebar_state="expanded",
)

SIZE_MAP = {
    "작게": 16,
    "보통": 19,
    "크게": 23,
    "아주 크게": 28,
}


def set_page(target):
    st.session_state["page_choice"] = target


with st.sidebar:
    st.title("🖐️ 편한 키오스크")
    st.caption("누구나 천천히, 쉽게")

    font_choice = st.select_slider(
        "글자 크기 변경",
        options=list(SIZE_MAP.keys()),
        value="크게",
        key="font_size_choice",
    )

    st.divider()

    if "page_choice" not in st.session_state:
        st.session_state["page_choice"] = "처음 화면"

    page = st.radio(
        "메뉴",
        ["처음 화면", "주문 방법 배우기", "도움이 필요해요"],
        key="page_choice",
    )

    st.caption("키오스크 사용 방법을 배우는 안내용 앱입니다.")


font_size = SIZE_MAP.get(font_choice, 23)

st.markdown(
    f"""
    <style>
    html, body, [class*="css"] {{
        font-size: {font_size}px;
    }}
    .block-container {{
        max-width: 850px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }}
    div.stButton > button {{
        min-height: 3.2rem;
        font-size: {max(font_size, 18)}px;
        font-weight: 650;
        border-radius: 12px;
        width: 100%;
    }}
    div[data-testid="stAlert"] {{
        border-radius: 12px;
    }}
    .hero {{
        padding: 1.4rem;
        border-radius: 18px;
        background: #F2F7F4;
        border: 1px solid #D8E7DE;
        margin-bottom: 1rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>편한 키오스크</h1>
      <p>화면을 하나씩 따라 하면 주문 방법을 쉽게 배울 수 있어요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if page == "처음 화면":
    st.subheader("어떤 도움이 필요하세요?")
    st.write("원하는 항목을 선택해 주세요. 서두르지 않아도 괜찮아요.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🛒")
        st.markdown("**주문 방법 배우기**")
        st.write("메뉴 선택부터 결제까지 순서대로 알아봐요.")
        st.button(
            "주문 방법 보기",
            key="go_order",
            type="primary",
            on_click=set_page,
            args=("주문 방법 배우기",),
        )

    with col2:
        st.markdown("### 🙋")
        st.markdown("**도움 요청하기**")
        st.write("어려운 상황에서 도움을 요청하는 방법이에요.")
        st.button(
            "도움 요청 방법 보기",
            key="go_help",
            on_click=set_page,
            args=("도움이 필요해요",),
        )

    st.divider()
    st.subheader("주문할 때 기억하세요")
    st.markdown(
        """
        - 천천히 눌러도 괜찮아요.
        - 잘못 눌렀다면 화면의 '뒤로' 또는 '취소'를 찾아보세요.
        - 결제 전에는 메뉴와 금액을 한 번 더 확인하세요.
        """
    )

elif page == "주문 방법 배우기":
    st.subheader("키오스크 주문 5단계")
    st.write("배우고 싶은 단계를 선택해 보세요.")

    steps = [
        {
            "title": "1단계 · 주문 시작",
            "short": "화면에서 '주문하기' 또는 '시작'을 눌러요.",
            "detail": "처음 화면에서 '주문하기'나 '시작하기'처럼 적힌 버튼을 찾아 눌러 보세요. 매장마다 표현은 다를 수 있어요.",
            "tip": "매장 식사와 포장 중 선택하는 화면이 나오면 원하는 방식을 골라요.",
        },
        {
            "title": "2단계 · 메뉴 고르기",
            "short": "원하는 음식이나 음료를 선택해요.",
            "detail": "메뉴 종류를 살펴보고 원하는 메뉴의 사진이나 이름을 눌러요. 메뉴 이름과 가격도 함께 확인해요.",
            "tip": "메뉴가 많으면 커피, 음료, 식사 같은 분류를 먼저 눌러 보세요.",
        },
        {
            "title": "3단계 · 옵션과 수량 확인",
            "short": "필요한 옵션과 수량을 선택해요.",
            "detail": "크기, 온도, 추가 재료, 수량 등을 고르는 화면이 나올 수 있어요. 원하는 항목만 선택하면 돼요.",
            "tip": "선택을 마쳤다면 '담기', '추가', '확인' 버튼을 찾아요.",
        },
        {
            "title": "4단계 · 주문과 결제 확인",
            "short": "주문 목록과 금액을 확인한 뒤 결제해요.",
            "detail": "메뉴, 수량, 총금액이 맞는지 살펴봐요. 맞다면 '결제하기'를 누르고 화면의 결제 안내를 따라요.",
            "tip": "결제 방법이 헷갈리면 직원에게 도움을 요청하세요.",
        },
        {
            "title": "5단계 · 주문 완료 확인",
            "short": "완료 화면이나 주문 번호를 확인해요.",
            "detail": "결제가 끝나면 주문 완료 화면이나 주문 번호가 표시될 수 있어요. 화면의 안내를 확인하세요.",
            "tip": "주문 번호가 표시되면 음식을 받을 때 필요할 수 있어요.",
        },
    ]

    selected_step = st.radio(
        "배우고 싶은 단계",
        options=range(len(steps)),
        format_func=lambda i: steps[i]["title"],
    )

    item = steps[selected_step]

    st.markdown(f"### {item['title']}")
    st.info(item["short"])
    st.write(item["detail"])
    st.success("💡 쉬운 팁: " + item["tip"])

    st.divider()
    st.subheader("주문 전 마지막 확인")
    st.checkbox("원하는 메뉴를 골랐어요.")
    st.checkbox("수량과 옵션을 확인했어요.")
    st.checkbox("결제할 금액을 확인했어요.")
    st.caption("연습용 확인표이며 실제 주문이나 결제는 진행하지 않습니다.")

elif page == "도움이 필요해요":
    st.subheader("어려운 상황에서는 이렇게 해 보세요.")

    situations = {
        "어디를 눌러야 할지 모르겠어요": (
            "화면을 잠시 살펴보고 '시작', '다음', '확인' 같은 글자를 찾아보세요.",
            "죄송하지만 키오스크 사용을 도와주실 수 있을까요?",
        ),
        "잘못 선택했어요": (
            "화면에 '뒤로', '취소', '삭제'가 있는지 확인하세요. 결제 전이라면 주문 목록을 살펴보세요.",
            "선택을 잘못했는데 취소하는 방법을 알려주시겠어요?",
        ),
        "결제가 진행되지 않아요": (
            "같은 버튼을 여러 번 누르지 말고 화면의 안내를 확인하세요. 결제 여부가 불확실하면 직원에게 먼저 물어보세요.",
            "결제가 완료됐는지 확인하고 도와주실 수 있을까요?",
        ),
        "화면이 멈췄어요": (
            "버튼을 계속 누르지 말고 잠시 기다려 보세요. 화면이 계속 멈춰 있다면 직원에게 알려주세요.",
            "키오스크 화면이 멈춘 것 같아요. 확인해 주시겠어요?",
        ),
    }

    situation = st.selectbox(
        "어떤 상황인가요?",
        list(situations.keys()),
    )

    advice, phrase = situations[situation]

    st.warning(advice)
    st.markdown("### 직원에게 이렇게 말해 보세요")
    st.info(f"“{phrase}”")
    st.caption("예시 문장입니다. 편한 말로 도움을 요청해도 괜찮아요.")

    st.divider()
    st.subheader("기억하면 좋은 세 가지")
    st.markdown(
        """
        1. 결제가 됐는지 모를 때는 반복 결제하지 말고 먼저 확인해요.
        2. 카드나 소지품을 두고 오지 않았는지 확인해요.
        3. 혼자 해결하기 어려우면 직원에게 도움을 요청해도 괜찮아요.
        """
    )

st.divider()
st.caption("편한 키오스크 · 누구나 쉽게 이용할 수 있는 키오스크 안내 서비스")
