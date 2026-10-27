
import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="키오스크 음성 지원",
    page_icon="🔊",
    layout="centered"
)

if "step" not in st.session_state:
    st.session_state.step = 0

if "speed" not in st.session_state:
    st.session_state.speed = "보통"

steps = [
    ("주문 시작", "주문 시작 버튼을 눌러주세요."),
    ("메뉴 선택", "원하는 메뉴를 선택하고 메뉴 담기를 눌러주세요."),
    ("주문 확인", "선택한 메뉴를 확인하고 결제 버튼을 눌러주세요."),
    ("결제 안내", "화면의 안내에 따라 결제를 진행해주세요."),
    ("주문 완료", "주문이 완료되었습니다. 주문 번호를 확인해주세요.")
]

st.title("🔊 키오스크 음성 지원")
st.write("음성 안내를 통해 키오스크를 쉽게 이용하세요.")

st.session_state.speed = st.radio(
    "🔈 음성 속도",
    ["느리게", "보통", "빠르게"],
    horizontal=True,
    index=["느리게", "보통", "빠르게"].index(
        st.session_state.speed
    )
)

speed_values = {
    "느리게": 0.7,
    "보통": 1.0,
    "빠르게": 1.3
}

title, description = steps[st.session_state.step]

st.progress((st.session_state.step + 1) / len(steps))
st.subheader(f"{st.session_state.step + 1}. {title}")
st.info(description)

speech_text = json.dumps(
    f"{title}. {description}",
    ensure_ascii=False
)
speech_rate = speed_values[st.session_state.speed]

components.html(
    f"""
    <button onclick="speak()" style="
        width:100%; padding:16px; font-size:20px;
        background:#1769aa; color:white;
        border:0; border-radius:12px; cursor:pointer;">
        🔊 현재 화면 읽어주기
    </button>
    <script>
    function speak() {{
        if (!window.speechSynthesis) {{
            alert("이 브라우저는 음성 안내를 지원하지 않습니다.");
            return;
        }}
        window.speechSynthesis.cancel();
        let msg = new SpeechSynthesisUtterance({speech_text});
        msg.lang = "ko-KR";
        msg.rate = {speech_rate};
        window.speechSynthesis.speak(msg);
    }}
    </script>
    """,
    height=75
)

st.write("### 다음 행동")
if st.session_state.step < len(steps) - 1:
    st.write(steps[st.session_state.step + 1][1])
else:
    st.write("모든 안내가 끝났습니다.")

col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ 전 단계", use_container_width=True):
        st.session_state.step = max(
            0, st.session_state.step - 1
        )
        st.rerun()

with col2:
    if st.button("➡️ 다음 단계", use_container_width=True):
        st.session_state.step = min(
            len(steps) - 1, st.session_state.step + 1
        )
        st.rerun()

if st.button("🔄 처음부터 다시 안내", use_container_width=True):
    st.session_state.step = 0
    st.rerun()

if st.button("🆘 도움 요청", use_container_width=True):
    st.warning(
        "현재 화면의 음성 안내를 다시 듣거나 "
        "전 단계 버튼을 눌러주세요. "
        "필요하면 직원에게 도움을 요청하세요."
    )

st.caption("음성 기능은 브라우저의 한국어 음성 지원 여부에 따라 달라질 수 있습니다.")
