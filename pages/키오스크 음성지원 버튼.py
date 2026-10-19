
import json
import html

import streamlit as st
import streamlit.components.v1 as components


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="키오스크 음성지원 도우미",
    page_icon="🔊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f8fc;
    }
    .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3 {
        color: #183153;
    }
    .hero {
        background: linear-gradient(135deg, #173f75, #2876b9);
        padding: 28px 24px;
        border-radius: 20px;
        color: white;
        margin-bottom: 20px;
    }
    .hero h1 {
        color: white;
        font-size: 2rem;
        margin-bottom: 10px;
    }
    .hero p {
        font-size: 1.1rem;
        line-height: 1.7;
        margin-bottom: 0;
    }
    .info-card {
        background: white;
        border: 1px solid #d9e3f0;
        padding: 20px;
        border-radius: 16px;
        margin: 10px 0;
    }
    .step-label {
        color: #245d99;
        font-weight: 700;
        font-size: 1rem;
    }
    div.stButton > button {
        min-height: 54px;
        border-radius: 12px;
        font-size: 1.05rem;
        font-weight: 600;
        width: 100%;
    }
    div[data-testid="stAlert"] {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 메뉴 데이터
# --------------------------------------------------
MENU = {
    "아메리카노": {"price": 2500, "emoji": "☕"},
    "카페라떼": {"price": 3500, "emoji": "🥛"},
    "레몬에이드": {"price": 4000, "emoji": "🍋"},
    "초코머핀": {"price": 2800, "emoji": "🧁"},
}

STEPS = ["menu", "cart", "confirm", "complete"]

STEP_NAMES = {
    "menu": "메뉴 선택",
    "cart": "장바구니 확인",
    "confirm": "주문 확인",
    "complete": "주문 완료",
}

STEP_GUIDANCE = {
    "menu": (
        "메뉴 선택 화면입니다. "
        "원하는 메뉴 아래의 담기 버튼을 눌러 주세요. "
        "메뉴를 담았다면 장바구니 확인 버튼을 눌러 다음 단계로 이동하세요."
    ),
    "cart": (
        "장바구니 확인 화면입니다. "
        "선택한 메뉴와 수량, 결제 예정 금액을 확인하세요. "
        "주문할 준비가 되었다면 주문 계속하기 버튼을 눌러 주세요. "
        "메뉴를 더 고르고 싶으면 메뉴 선택으로 돌아갈 수 있습니다."
    ),
    "confirm": (
        "주문 확인 화면입니다. "
        "주문 내역과 총금액을 확인하세요. "
        "주문을 진행하려면 주문 완료 버튼을 누르세요. "
        "아직 준비가 되지 않았다면 이전 단계로 돌아갈 수 있습니다."
    ),
    "complete": (
        "주문 체험이 완료되었습니다. "
        "실제 결제는 진행되지 않았습니다. "
        "처음부터 다시 안내 버튼을 누르면 새로운 주문을 시작할 수 있습니다."
    ),
}

SPEEDS = {
    "느리게": 0.75,
    "보통": 1.0,
    "빠르게": 1.2,
}


# --------------------------------------------------
# 세션 상태 초기화
# --------------------------------------------------
def init_state():
    defaults = {
        "step": "menu",
        "cart": {},
        "speed": "보통",
        "speech_text": "",
        "notice": "",
        "history": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


# --------------------------------------------------
# 공통 기능
# --------------------------------------------------
def announce(message):
    """다음 화면에서 읽을 음성 안내를 저장합니다."""
    st.session_state["speech_text"] = str(message)


def navigate(step, message=None):
    """화면을 이동하고 이전 단계 기록을 관리합니다."""
    current = st.session_state["step"]

    if current != step:
        history = st.session_state["history"]
        history.append(current)
        st.session_state["history"] = history[-20:]

    st.session_state["step"] = step

    if message:
        announce(message)


def previous_step():
    """이전 단계로 돌아갑니다."""
    history = st.session_state["history"]

    if history:
        previous = history.pop()
        st.session_state["history"] = history
        st.session_state["step"] = previous
        announce(
            f"{STEP_NAMES[previous]} 화면으로 돌아왔습니다. "
            + STEP_GUIDANCE[previous]
        )
    else:
        st.session_state["step"] = "menu"
        announce("첫 화면입니다. " + STEP_GUIDANCE["menu"])


def restart():
    """주문 체험을 처음부터 다시 시작합니다."""
    st.session_state["step"] = "menu"
    st.session_state["cart"] = {}
    st.session_state["history"] = []
    st.session_state["notice"] = ""
    announce(
        "처음부터 다시 안내하겠습니다. "
        + STEP_GUIDANCE["menu"]
    )


def money(amount):
    return f"{amount:,}원"


def cart_total():
    total = 0

    for name, quantity in st.session_state["cart"].items():
        if name in MENU:
            total += MENU[name]["price"] * quantity

    return total


def cart_summary():
    cart = st.session_state["cart"]

    if not cart:
        return "장바구니가 비어 있습니다."

    parts = []
    for name, quantity in cart.items():
        if name in MENU and quantity > 0:
            parts.append(f"{name} {quantity}개")

    if not parts:
        return "장바구니가 비어 있습니다."

    return (
        "주문 내역은 "
        + ", ".join(parts)
        + f"입니다. 총금액은 {money(cart_total())}입니다."
    )


def render_speech(text, speed):
    """
    브라우저 내장 음성 합성을 사용합니다.
    외부 API나 별도 음성 파일은 필요하지 않습니다.
    """
    if not text:
        return

    try:
        safe_text = json.dumps(text, ensure_ascii=False)
        rate = SPEEDS.get(speed, 1.0)

        # HTML script 종료 문자열이 입력에 포함되어도
        # 스크립트 태그가 조기에 닫히지 않도록 처리합니다.
        safe_text = safe_text.replace("</", "<\\/")

        speech_html = f"""
        <!doctype html>
        <html lang="ko">
        <head><meta charset="utf-8"></head>
        <body>
        <script>
        (() => {{
            const text = {safe_text};
            const rate = {rate};

            try {{
                if (!("speechSynthesis" in window) ||
                    !("SpeechSynthesisUtterance" in window)) {{
                    document.body.innerText =
                        "이 브라우저에서는 음성 읽기를 지원하지 않습니다. 화면의 안내 문구를 읽어 주세요.";
                    return;
                }}

                window.speechSynthesis.cancel();

                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = "ko-KR";
                utterance.rate = rate;
                utterance.pitch = 1.0;
                utterance.volume = 1.0;

                const voices = window.speechSynthesis.getVoices();
                const koreanVoice = voices.find(
                    voice => voice.lang &&
                    voice.lang.toLowerCase().startsWith("ko")
                );

                if (koreanVoice) {{
                    utterance.voice = koreanVoice;
                }}

                window.speechSynthesis.speak(utterance);
            }} catch (error) {{
                document.body.innerText =
                    "음성 안내를 시작하지 못했습니다. 화면의 안내 문구를 확인해 주세요.";
            }}
        }})();
        </script>
        </body>
        </html>
        """

        components.html(speech_html, height=35, scrolling=False)

    except Exception:
        st.info(
            "음성 안내를 실행할 수 없습니다. "
            "아래 화면 안내를 읽고 진행해 주세요."
        )


# --------------------------------------------------
# 상단 제목
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🔊 키오스크 음성지원 도우미</h1>
        <p>
            천천히, 하나씩 따라 해 보세요.<br>
            화면의 안내를 듣고 버튼을 눌러 주문을 체험할 수 있습니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 음성 설정 및 공통 도움말
# --------------------------------------------------
st.subheader("🎧 음성 안내 설정")

st.radio(
    "원하는 음성 속도를 선택하세요.",
    options=list(SPEEDS.keys()),
    horizontal=True,
    key="speed",
)

col_help1, col_help2 = st.columns(2)

with col_help1:
    if st.button("🔊 현재 화면 읽어주기", type="primary"):
        announce(
            STEP_GUIDANCE[st.session_state["step"]]
            + " "
            + cart_summary()
            if st.session_state["step"] in ("cart", "confirm")
            else STEP_GUIDANCE[st.session_state["step"]]
        )

with col_help2:
    if st.button("❓ 도움말 보기"):
        step = st.session_state["step"]
        st.session_state["notice"] = (
            "도움말: 버튼을 눌러 다음 단계로 이동하세요. "
            "이전 단계로 돌아가거나 처음부터 다시 시작할 수도 있습니다. "
            + STEP_GUIDANCE[step]
        )
        announce(st.session_state["notice"])

if st.session_state["notice"]:
    st.info(st.session_state["notice"])

# --------------------------------------------------
# 진행 단계 표시
# --------------------------------------------------
step = st.session_state["step"]
step_index = STEPS.index(step)

st.progress((step_index + 1) / len(STEPS))
st.markdown(
    f'<div class="step-label">진행 단계: {step_index + 1}/4 · '
    f'{html.escape(STEP_NAMES[step])}</div>',
    unsafe_allow_html=True,
)

st.divider()


# --------------------------------------------------
# 1단계: 메뉴 선택
# --------------------------------------------------
if step == "menu":
    st.header("1. 메뉴를 선택하세요")
    st.write(
        "원하는 메뉴의 담기 버튼을 누르면 장바구니에 추가됩니다."
    )

    for name, item in MENU.items():
        with st.container(border=True):
            left, right = st.columns([3, 1])

            with left:
                st.subheader(f"{item['emoji']} {name}")
                st.write(f"가격: **{money(item['price'])}**")

            with right:
                if st.button(
                    "담기",
                    key=f"add_{name}",
                    use_container_width=True,
                ):
                    cart = st.session_state["cart"]
                    cart[name] = cart.get(name, 0) + 1
                    st.session_state["cart"] = cart
                    announce(
                        f"{name} 한 개를 담았습니다. "
                        f"현재 {name} 수량은 {cart[name]}개입니다. "
                        "계속 메뉴를 고르거나 장바구니 확인 버튼을 누르세요."
                    )
                    st.rerun()

    st.divider()

    st.markdown("### 🛒 장바구니")
    st.write(cart_summary())

    if st.button(
        "장바구니 확인하기 →",
        type="primary",
        use_container_width=True,
    ):
        navigate(
            "cart",
            "장바구니 확인 화면으로 이동합니다. " + STEP_GUIDANCE["cart"],
        )
        st.rerun()


# --------------------------------------------------
# 2단계: 장바구니
# --------------------------------------------------
elif step == "cart":
    st.header("2. 장바구니를 확인하세요")
    cart = st.session_state["cart"]

    if not cart:
        st.warning("아직 선택한 메뉴가 없습니다.")
        st.write("메뉴 선택 화면으로 돌아가 메뉴를 담아 주세요.")

        if st.button("메뉴 선택으로 돌아가기", type="primary"):
            navigate("menu", STEP_GUIDANCE["menu"])
            st.rerun()
    else:
        for name in list(cart.keys()):
            if name not in MENU:
                continue

            with st.container(border=True):
                left, middle, right = st.columns([2, 1, 1])

                with left:
                    st.write(f"**{MENU[name]['emoji']} {name}**")
                    st.caption(money(MENU[name]["price"]))

                with middle:
                    st.write(f"수량: {cart[name]}개")

                with right:
                    if st.button("1개 삭제", key=f"remove_{name}"):
                        cart[name] -= 1

                        if cart[name] <= 0:
                            del cart[name]

                        st.session_state["cart"] = cart
                        announce(
                            f"{name} 한 개를 삭제했습니다. "
                            + cart_summary()
                        )
                        st.rerun()

        st.markdown(
            f'<div class="info-card"><h3>총금액: '
            f'{money(cart_total())}</h3>'
            f'<p>실제 결제는 발생하지 않습니다.</p></div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("← 메뉴 더 고르기"):
                navigate("menu", STEP_GUIDANCE["menu"])
                st.rerun()

        with col2:
            if st.button("주문 계속하기 →", type="primary"):
                navigate(
                    "confirm",
                    STEP_GUIDANCE["confirm"] + " " + cart_summary(),
                )
                st.rerun()


# --------------------------------------------------
# 3단계: 주문 확인
# --------------------------------------------------
elif step == "confirm":
    st.header("3. 주문 내용을 확인하세요")
    st.write("주문하기 전에 메뉴와 총금액을 확인해 주세요.")

    if not st.session_state["cart"]:
        st.warning("장바구니가 비어 있습니다. 메뉴를 먼저 선택해 주세요.")

        if st.button("메뉴 선택으로 이동", type="primary"):
            navigate("menu", STEP_GUIDANCE["menu"])
            st.rerun()
    else:
        for name, quantity in st.session_state["cart"].items():
            if name in MENU:
                st.write(
                    f"- {MENU[name]['emoji']} {name} × {quantity}개 "
                    f"— {money(MENU[name]['price'] * quantity)}"
                )

        st.subheader(f"총금액: {money(cart_total())}")
        st.info(
            "체험용 주문입니다. 이 앱은 카드 결제, 현금 결제 또는 "
            "실제 주문 전송을 수행하지 않습니다."
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("← 이전 단계"):
                previous_step()
                st.rerun()

        with col2:
            if st.button("주문 완료", type="primary"):
                navigate(
                    "complete",
                    "주문 체험이 완료되었습니다. "
                    + cart_summary()
                    + " 실제 결제는 진행되지 않았습니다.",
                )
                st.rerun()


# --------------------------------------------------
# 4단계: 완료
# --------------------------------------------------
elif step == "complete":
    st.header("4. 주문 체험이 완료되었습니다!")
    st.success("🎉 잘하셨습니다. 모든 단계를 완료했습니다.")

    st.markdown(
        f"""
        <div class="info-card">
            <h3>주문 결과</h3>
            <p>{html.escape(cart_summary())}</p>
            <p><strong>결제 금액: {money(cart_total())}</strong></p>
            <p>이 화면은 교육용 체험이며 실제 결제는 없습니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "🔄 처음부터 다시 안내",
        type="primary",
        use_container_width=True,
    ):
        restart()
        st.rerun()


# --------------------------------------------------
# 하단 공통 도움 요청
# --------------------------------------------------
st.divider()
st.subheader("도움이 필요하신가요?")

help_col1, help_col2 = st.columns(2)

with help_col1:
    if st.button("🔁 처음부터 다시 안내", key="footer_restart"):
        restart()
        st.rerun()

with help_col2:
    if st.button("⬅️ 이전 단계로 돌아가기", key="footer_back"):
        previous_step()
        st.rerun()

st.caption(
    "접근성 체험용 앱 · 음성 기능은 브라우저의 한국어 음성 지원 여부에 따라 달라질 수 있습니다."
)


# --------------------------------------------------
# 음성 실행: 새 안내가 있을 때만 호출
# --------------------------------------------------
pending_speech = st.session_state.get("speech_text", "")

if pending_speech:
    # 먼저 비워 다음 Streamlit 재실행에서 같은 안내가
    # 반복해서 재생되지 않도록 합니다.
    st.session_state["speech_text"] = ""
    render_speech(pending_speech, st.session_state["speed"])
