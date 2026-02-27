import os
import streamlit as st
import requests
import base64

st.set_page_config(
    page_title="Titanic Chat Agent",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# CSS - Production-quality dark theme
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');

/* ---- Reset & base ---- */
html, body, [class*="css"], [class*="st-"] {
    font-family: 'EB Garamond', Garamond, serif !important;
    color: #e4e4e7 !important;
    font-size: 1.0rem !important;
}

.stApp {
    background-color: #0f0f11 !important;
    padding-bottom: 140px !important; /* space so content doesn't hide behind fixed bar */
}

/* ---- Main container ---- */
.main .block-container {
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 16px;
    padding: 0 !important;
    padding-bottom: 2rem !important;
    margin-top: -4.5rem !important; /* push right to top */
    margin-bottom: 0 !important;
    max-width: 90% !important;
    background-color: #18181b !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4) !important;
    display: flex !important;
    flex-direction: column !important;
    min-height: 85vh !important;
}

/* Inner content padding */
.stVerticalBlock {
    padding: 0 3rem !important;
}

/* ---- Hide chrome ---- */
header, footer { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* ---- Header wrapper ---- */
.header-wrapper {
    background-color: transparent !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    padding: 0.75rem 3rem 1.15rem 3rem;
    margin-bottom: 1rem;
    border-radius: 16px 16px 0 0;
}

/* ---- Typography ---- */
.app-title {
    text-align: center;
    font-family: 'EB Garamond', Garamond, serif !important;
    font-size: 2.8rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em;
    margin-top: 0 !important;
    margin-bottom: 1rem !important;
    padding-bottom: 0 !important;
    color: #fafafa !important;
}

.app-description {
    text-align: center;
    font-size: 1.25rem !important;
    color: #a1a1aa !important;
    margin-bottom: 0 !important;
    line-height: 1.5 !important;
}

/* ---- Chat messages ---- */
.stChatMessage {
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 12px !important;
    background-color: #1e1e22 !important;
    padding: 1.15rem 1.5rem !important;
    margin-bottom: 1rem !important;
    font-size: 1.3rem !important;
}

.stChatMessage p,
.stChatMessage li,
.stChatMessage span {
    font-size: 1.3rem !important;
    line-height: 1.6 !important;
}

/* Visualization image constraints */
[data-testid="stChatMessage"] img {
    max-width: 600px !important;
    height: auto !important;
    border-radius: 8px;
    margin-top: 0.5rem;
}

/* user message accent */
.stChatMessage[data-testid="chat-message-user"] {
    border-left: 3px solid #3b82f6 !important;
}

/* assistant message accent */
.stChatMessage[data-testid="chat-message-assistant"] {
    border-left: 3px solid #ef4444 !important;
}

/* ---- Welcome card ---- */
.welcome-card {
    text-align: center;
    padding: 3rem 2.25rem !important;
    border: 1px dashed rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(59,130,246,0.04), rgba(139,92,246,0.04));
    margin-bottom: 2rem;
}
.welcome-card .welcome-icon {
    font-size: 3rem !important;
    margin-bottom: 0.75rem;
}
.welcome-card h3 {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    color: #fafafa !important;
    margin-bottom: 0.75rem !important;
}
.welcome-card p {
    font-size: 1.15rem !important;
    color: #a1a1aa !important;
    line-height: 1.5 !important;
    max-width: 600px;
    margin: 0 auto;
}

/* ---- Quick Actions ---- */
.qa-header {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #a1a1aa !important;
    margin-bottom: 0.5rem !important;
    margin-top: 1.5rem !important;
}

/* Remove default gaps and allow standard spacing for rounded buttons */
[data-testid="stHorizontalBlock"] {
    gap: 0.75rem !important;
}

/* Quick action buttons */
div.stColumn button[kind="secondary"],
button[kind="secondary"] {
    background-color: #27272a !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important; /* fully rounded */
    color: #d4d4d8 !important;
    font-family: 'EB Garamond', serif !important;
    font-size: 1.0rem !important;
    font-weight: 500 !important;
    padding: 0.75rem 0.9rem !important;
    min-height: unset !important;
    line-height: 1.35 !important;
    white-space: normal !important;
    word-wrap: break-word !important;
    text-align: center !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
}

/* Round all edges for all buttons */
div.stColumn button[kind="secondary"] {
    border-radius: 12px !important;
}

div.stColumn button[kind="secondary"]:hover,
button[kind="secondary"]:hover {
    background-color: #3f3f46 !important;
    border-color: rgba(255, 255, 255, 0.15) !important;
    color: #fafafa !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
}

div.stColumn button[kind="secondary"]:active,
button[kind="secondary"]:active {
    transform: translateY(0px);
}

/* ========== FIXED BOTTOM BAR ========== */
/* Keep Streamlit bottom wrapper neutral and pin controls manually */
[data-testid="stBottom"] {
    position: static !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* Chat input styling */
div[data-testid="stChatInput"] {
    position: fixed !important;
    left: 5% !important;
    bottom: 24px !important;
    width: calc(90% - 190px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    background-color: #1e1e22 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
    padding: 1.25rem 2rem !important;
    margin: 0 !important;
    min-height: 70px !important;
    z-index: 1001 !important;
}

/* Remove red/pink focus outline */
div[data-testid="stChatInput"]:focus-within {
    outline: none !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6) !important;
}

/* Kill all default Streamlit container borders/outlines */
.stChatInputContainer,
[data-testid="stChatInputContainer"] {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    background: transparent !important;
}
.stChatInputContainer:focus-within,
[data-testid="stChatInputContainer"]:focus-within {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

div[data-testid="stChatInputTextArea"] {
    background-color: transparent !important;
}

div[data-testid="stChatInput"] textarea {
    color: #e4e4e7 !important;
    font-family: 'EB Garamond', serif !important;
    font-size: 1.5rem !important;
    line-height: 1.5 !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #71717a !important;
    font-size: 1.5rem !important;
}

/* Send button inside chat input */
div[data-testid="stChatInput"] button {
    background-color: #3b82f6 !important;
    border: none !important;
    border-radius: 8px !important;
    color: #fff !important;
    padding: 0.5rem 1rem !important;
    transition: background-color 0.15s ease !important;
}

div[data-testid="stChatInput"] button:hover {
    background-color: #2563eb !important;
}

div[data-testid="stChatInput"] svg {
    color: #fff !important;
    width: 28px !important;
    height: 28px !important;
}

/* ---- Clear Chat button (beside query bar) ---- */
button[kind="primary"] {
    background-color: #27272a !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important; 
    color: #d4d4d8 !important;
    font-family: 'EB Garamond', serif !important;
    font-size: 1.0rem !important;
    font-weight: 500 !important;
    height: 70px !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 170px !important;
    position: fixed !important;
    right: 5% !important;
    bottom: 24px !important; /* matched with query bar */
    z-index: 1002 !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    line-height: 70px !important; /* Force text to center vertically */
}

/* Ensure the button content is centered */
button[kind="primary"] div {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* No padding between query input and clear button containers */
[data-testid="column"] {
    padding-left: 0 !important;
    padding-right: 0 !important;
}

button[kind="primary"]:hover {
    background-color: #3f3f46 !important;
    border-color: rgba(255, 255, 255, 0.15) !important;
    color: #fafafa !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
}

button[kind="primary"]:active {
    transform: translateY(0px);
}

/* ---- Layout spacing ---- */
div.stVerticalBlock {
    gap: 0.25rem !important;
}

/* ---- Spinner ---- */
.stSpinner > div {
    border-color: #3b82f6 transparent transparent transparent !important;
}

/* ---- Horizontal rule ---- */
hr {
    border-color: rgba(255, 255, 255, 0.06) !important;
    margin: 0.75rem 0 !important;
}

/* ---- Scrollbar ---- */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #3f3f46; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #52525b; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Config & Avatars
# ---------------------------------------------------------------------------
BACKEND_URL = st.secrets.get(
    "BACKEND_URL",
    os.getenv("BACKEND_URL", "http://localhost:8000"),
).rstrip("/")

if "messages" not in st.session_state:
    st.session_state.messages = []


def get_avatar(role):
    if role == "user":
        return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%233b82f6' stroke-width='2'%3E%3Ccircle cx='12' cy='12' r='8'/%3E%3C/svg%3E"
    else:
        return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23ef4444' stroke-width='2'%3E%3Cpolygon points='12 4 20 19 4 19'/%3E%3C/svg%3E"


# ---------------------------------------------------------------------------
# Helper: send message to backend
# ---------------------------------------------------------------------------
def send_message(message: str):
    """Send a message to the backend and append the response to session state."""
    st.session_state.messages.append({"role": "user", "content": message})

    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/chat",
                json={"message": message},
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": data.get("text_response", "No response received."),
                    "visualization": data.get("visualization"),
                }
            )
        except requests.exceptions.ConnectionError:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "Cannot connect to the backend server at "
                        f"{BACKEND_URL}. Make sure the FastAPI server is running "
                        "and the BACKEND_URL setting is correct."
                    ),
                }
            )
        except Exception as e:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"An error occurred: {str(e)}",
                }
            )

    st.rerun()


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

# -- Header --
st.markdown(
    """
    <div class="header-wrapper">
        <h1 class='app-title'>Titanic Chat Agent</h1>
        <p class='app-description'>Ask questions, get insights, and generate visualizations from the Titanic passenger data.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -- Chat messages --
if len(st.session_state.messages) == 0:
    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-icon">🚢</div>
            <h3>Welcome aboard!</h3>
            <p>
                Start a conversation by typing a question below or try one of the quick actions.
                <br>
                I can analyze data, answer questions, and create charts.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=get_avatar(msg["role"])):
            st.markdown(msg["content"])
            if msg.get("visualization"):
                image_bytes = base64.b64decode(msg["visualization"])
                st.image(image_bytes, use_container_width=True)

# -- Quick actions --
st.markdown(
    "<p class='qa-header'>Quick Actions</p>",
    unsafe_allow_html=True,
)

qa_questions = [
    ("Gender Split", "Show me a pie chart of male vs female passengers"),
    ("Age Distribution", "Show me a histogram of passenger ages"),
    ("Avg Fare by Class", "What was the average ticket fare for each class?"),
    ("Survival Rate", "What was the overall survival rate on the Titanic?"),
    ("Embarkation Ports", "How many passengers embarked from each port?"),
]

qa_cols = st.columns(len(qa_questions))
for i, (label, question) in enumerate(qa_questions):
    with qa_cols[i]:
        if st.button(label, key=f"qa_{i}", use_container_width=True):
            st.session_state.pending_question = question

# -- Handle pending question --
if "pending_question" in st.session_state:
    pending = st.session_state.pop("pending_question")
    send_message(pending)

# -- Fixed bottom bar: Query input + Clear Chat --
with st.container():
    input_col, clear_col = st.columns([9, 1])

    with input_col:
        if user_input := st.chat_input("Ask anything about the Titanic dataset..."):
            send_message(user_input)

    with clear_col:
        if st.button("Clear Chat", type="primary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
