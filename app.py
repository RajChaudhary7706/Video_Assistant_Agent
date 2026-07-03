import streamlit as st
import time
import threading
from dotenv import load_dotenv

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0b0b14; color: #e2e8f0; }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1100px; }

/* ── Banner ── */
.banner-wrap {
    background: linear-gradient(135deg, #12103a 0%, #1a0e3d 50%, #0f1a2e 100%);
    border: 1px solid #3b2d6b;
    border-radius: 16px;
    padding: 2.5rem 2rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.banner-wrap::before {
    content: '';
    position: absolute;
    top: -60px; left: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(124,58,237,0.18) 0%, transparent 70%);
    pointer-events: none;
}
.banner-wrap::after {
    content: '';
    position: absolute;
    bottom: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(6,182,212,0.13) 0%, transparent 70%);
    pointer-events: none;
}
.banner-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.1rem;
    font-weight: 600;
    color: #c4b5fd;
    letter-spacing: -0.02em;
    margin: 0 0 0.3rem;
}
.banner-sub {
    color: #06b6d4;
    font-size: 0.95rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 500;
    margin: 0;
}
.banner-dot { color: #7c3aed; margin: 0 0.5rem; }

/* ── Section headings ── */
.section-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b7280;
    margin: 1.8rem 0 0.9rem;
}
.section-head::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1f1f32;
}

/* ── Source card ── */
.source-card {
    background: #111127;
    border: 1px solid #2d2d50;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: #0d0d20 !important;
    border: 1px solid #3b2d6b !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}
.stSelectbox > div > div { color: #e2e8f0 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #5b21b6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    letter-spacing: 0.02em;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* ── Pipeline steps ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 0.5rem 0 1.5rem;
}
.pipeline-step {
    background: #111127;
    border: 1px solid #1f1f38;
    border-radius: 10px;
    padding: 0.85rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.8rem;
    color: #6b7280;
    transition: border-color 0.3s, color 0.3s;
}
.pipeline-step.active {
    border-color: #7c3aed;
    color: #c4b5fd;
    background: #1a0e3d;
}
.pipeline-step.done {
    border-color: #059669;
    color: #34d399;
    background: #0a1f18;
}
.pipeline-step.error {
    border-color: #dc2626;
    color: #f87171;
    background: #1f0a0a;
}
.step-icon { font-size: 1.1rem; flex-shrink: 0; }
.step-label { font-weight: 500; line-height: 1.25; }

/* ── Result cards ── */
.result-card {
    background: #111127;
    border-radius: 14px;
    border-left: 4px solid;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
}
.result-card.violet { border-color: #7c3aed; }
.result-card.cyan   { border-color: #06b6d4; }
.result-card.green  { border-color: #10b981; }
.result-card.amber  { border-color: #f59e0b; }
.result-card.red    { border-color: #ef4444; }

.card-title {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.7rem;
}
.card-title.violet { color: #a78bfa; }
.card-title.cyan   { color: #22d3ee; }
.card-title.green  { color: #34d399; }
.card-title.amber  { color: #fbbf24; }
.card-title.red    { color: #f87171; }

.card-body { color: #d1d5db; font-size: 0.9rem; line-height: 1.75; }

/* ── Numbered list ── */
.num-list { list-style: none; padding: 0; margin: 0; }
.num-list li {
    display: flex;
    align-items: baseline;
    gap: 0.75rem;
    padding: 0.45rem 0;
    border-bottom: 1px solid #1e1e32;
    font-size: 0.88rem;
    color: #d1d5db;
    line-height: 1.5;
}
.num-list li:last-child { border-bottom: none; }
.num-badge {
    background: #1e1535;
    color: #a78bfa;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    min-width: 22px;
    height: 22px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

/* ── Meta chips ── */
.meta-row { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 1rem; }
.meta-chip {
    background: #1a1a30;
    border: 1px solid #2d2d50;
    border-radius: 20px;
    padding: 0.3rem 0.85rem;
    font-size: 0.8rem;
    color: #9ca3af;
}
.meta-chip strong { color: #c4b5fd; font-weight: 600; }

/* ── Chat ── */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
    max-height: 480px;
    overflow-y: auto;
    padding-right: 4px;
}
.chat-bubble {
    padding: 0.85rem 1.1rem;
    border-radius: 12px;
    font-size: 0.88rem;
    line-height: 1.65;
    max-width: 88%;
}
.chat-user {
    background: #1a0e3d;
    border: 1px solid #3b2d6b;
    color: #e2e8f0;
    align-self: flex-end;
    border-bottom-right-radius: 4px;
}
.chat-assistant {
    background: #0d1f18;
    border: 1px solid #064e3b;
    color: #d1fae5;
    align-self: flex-start;
    border-bottom-left-radius: 4px;
}
.chat-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.chat-label.you { color: #a78bfa; }
.chat-label.bot { color: #34d399; }

/* ── Transcript box ── */
.transcript-box {
    background: #0d0d1e;
    border: 1px solid #1f1f38;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #6b7280;
    max-height: 200px;
    overflow-y: auto;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #111127 !important;
    color: #9ca3af !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
}

/* ── Status indicators ── */
.status-bar {
    background: #0d0d20;
    border: 1px solid #1f1f38;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #4b5563;
    margin-bottom: 1rem;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #111127;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1f1f38;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b7280 !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.45rem 1rem !important;
}
.stTabs [aria-selected="true"] {
    background: #1a0e3d !important;
    color: #c4b5fd !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.2rem !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0b0b14; }
::-webkit-scrollbar-thumb { background: #3b2d6b; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Session state defaults ────────────────────────────────────────────────────
for key, default in {
    "result": None,
    "chat_history": [],
    "pipeline_state": {},
    "processing": False,
    "error": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ── Helper: render numbered list ──────────────────────────────────────────────
def render_num_list(text: str) -> str:
    lines = [l.strip().lstrip("-•*").strip() for l in text.strip().splitlines() if l.strip()]
    items = "".join(
        f'<li><span class="num-badge">{i}</span>{line}</li>'
        for i, line in enumerate(lines, 1)
    )
    return f'<ul class="num-list">{items}</ul>'


# ── Helper: pipeline step HTML ────────────────────────────────────────────────
STEPS = [
    ("⬇", "Download audio"),
    ("🎙", "Transcribe"),
    ("📝", "Summarise"),
    ("✅", "Extract actions"),
    ("🔑", "Key decisions"),
    ("❓", "Open questions"),
    ("🧠", "Build RAG index"),
    ("💬", "Ready to chat"),
]

def render_pipeline(states: dict) -> str:
    cells = ""
    for i, (icon, label) in enumerate(STEPS):
        cls = states.get(i, "idle")
        cells += f'<div class="pipeline-step {cls}"><span class="step-icon">{icon}</span><span class="step-label">{label}</span></div>'
    return f'<div class="pipeline-grid">{cells}</div>'


# ── Banner ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="banner-wrap">
  <p class="banner-title">🎙 AI Meeting Assistant</p>
  <p class="banner-sub">Transcribe <span class="banner-dot">·</span> Translate <span class="banner-dot">·</span> Summarise <span class="banner-dot">·</span> Chat</p>
</div>
""", unsafe_allow_html=True)


# ── Layout: two columns ───────────────────────────────────────────────────────
left, right = st.columns([1, 1.8], gap="large")

# ═══════════════════════════════════════════════════════════
# LEFT COLUMN — Input + Pipeline status
# ═══════════════════════════════════════════════════════════
with left:
    st.markdown('<div class="section-head">⚙ Source</div>', unsafe_allow_html=True)

    source_type = st.selectbox(
        "Input type",
        ["YouTube URL", "Local file path"],
        label_visibility="collapsed",
    )

    if source_type == "YouTube URL":
        source = st.text_input(
            "YouTube URL",
            placeholder="https://youtu.be/...",
            label_visibility="collapsed",
        )
    else:
        source = st.text_input(
            "File path",
            placeholder="/path/to/meeting.mp4",
            label_visibility="collapsed",
        )

    language = st.selectbox(
        "Language",
        ["english", "hinglish"],
        label_visibility="collapsed",
        format_func=lambda x: f"🌐 {x.capitalize()}",
    )

    run_btn = st.button("▶  Analyse Meeting", use_container_width=True)

    st.markdown('<div class="section-head">⚡ Pipeline</div>', unsafe_allow_html=True)
    pipeline_placeholder = st.empty()
    pipeline_placeholder.markdown(
        render_pipeline(st.session_state.pipeline_state),
        unsafe_allow_html=True,
    )

    if st.session_state.error:
        st.error(st.session_state.error)

    # Tips
    st.markdown('<div class="section-head" style="margin-top:2rem">💡 Tips</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="source-card" style="padding:1rem 1.2rem; font-size:0.8rem; color:#6b7280; line-height:1.75;">
  <strong style="color:#9ca3af">Supported sources</strong><br>
  YouTube, MP4, MP3, WAV, M4A<br><br>
  <strong style="color:#9ca3af">Hinglish mode</strong><br>
  Whisper detects Hindi/English and translates to English before summarising.<br><br>
  <strong style="color:#9ca3af">RAG chat</strong><br>
  After analysis, ask anything about your meeting in the chat tab.
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# RIGHT COLUMN — Results + Chat
# ═══════════════════════════════════════════════════════════
with right:
    if st.session_state.result is None and not st.session_state.processing:
        st.markdown("""
<div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
            height:420px; color:#2d2d50; text-align:center; gap:1rem;">
  <div style="font-size:3.5rem; opacity:0.4;">🎙</div>
  <div style="font-size:0.95rem; font-weight:600; color:#3b2d6b;">No meeting analysed yet</div>
  <div style="font-size:0.8rem; color:#2d2d44; max-width:280px; line-height:1.6;">
    Paste a YouTube link or file path, choose your language, and hit Analyse.
  </div>
</div>
""", unsafe_allow_html=True)

    elif st.session_state.result:
        r = st.session_state.result

        # Meta row
        st.markdown(f"""
<div class="meta-row">
  <div class="meta-chip">📌 <strong>{r['title']}</strong></div>
  <div class="meta-chip">🌐 <strong>{language.capitalize()}</strong></div>
</div>
""", unsafe_allow_html=True)

        tab_summary, tab_actions, tab_decisions, tab_questions, tab_chat, tab_transcript = st.tabs([
            "📋 Summary", "✅ Actions", "🔑 Decisions", "❓ Questions", "💬 Chat", "📄 Transcript"
        ])

        # ── Summary ──
        with tab_summary:
            st.markdown(f"""
<div class="result-card violet">
  <div class="card-title violet">Meeting summary</div>
  <div class="card-body">{r['summary']}</div>
</div>
""", unsafe_allow_html=True)

        # ── Actions ──
        with tab_actions:
            st.markdown(f"""
<div class="result-card green">
  <div class="card-title green">Action items</div>
  {render_num_list(r['action_items'])}
</div>
""", unsafe_allow_html=True)

        # ── Decisions ──
        with tab_decisions:
            st.markdown(f"""
<div class="result-card amber">
  <div class="card-title amber">Key decisions</div>
  {render_num_list(r['key_decisions'])}
</div>
""", unsafe_allow_html=True)

        # ── Questions ──
        with tab_questions:
            st.markdown(f"""
<div class="result-card red">
  <div class="card-title red">Open questions</div>
  {render_num_list(r['open_questions'])}
</div>
""", unsafe_allow_html=True)

        # ── Chat ──
        with tab_chat:
            chat_html = '<div class="chat-container">'
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    chat_html += f'<div><div class="chat-label you">You</div><div class="chat-bubble chat-user">{msg["content"]}</div></div>'
                else:
                    chat_html += f'<div><div class="chat-label bot">Assistant</div><div class="chat-bubble chat-assistant">{msg["content"]}</div></div>'
            chat_html += "</div>"

            if st.session_state.chat_history:
                st.markdown(chat_html, unsafe_allow_html=True)
                st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

            with st.form("chat_form", clear_on_submit=True):
                user_q = st.text_input(
                    "Ask about your meeting…",
                    placeholder="Who owns the RAG pipeline task?",
                    label_visibility="collapsed",
                )
                send = st.form_submit_button("Send ↗", use_container_width=True)

            if send and user_q.strip():
                from core.rag_engine import ask_question
                st.session_state.chat_history.append({"role": "user", "content": user_q.strip()})
                with st.spinner("Thinking…"):
                    answer = ask_question(r["rag_chain"], user_q.strip())
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.rerun()

        # ── Transcript ──
        with tab_transcript:
            st.markdown(f'<div class="transcript-box">{r["transcript"]}</div>', unsafe_allow_html=True)
            st.download_button(
                "⬇  Download transcript (.txt)",
                data=r["transcript"],
                file_name=f"{r['title']}.txt",
                mime="text/plain",
                use_container_width=True,
            )


# ── Pipeline runner ────────────────────────────────────────────────────────────
if run_btn and source.strip():
    st.session_state.result = None
    st.session_state.chat_history = []
    st.session_state.error = None
    st.session_state.pipeline_state = {}
    st.session_state.processing = True

    def mark(idx: int, state: str):
        st.session_state.pipeline_state[idx] = state
        pipeline_placeholder.markdown(
            render_pipeline(st.session_state.pipeline_state),
            unsafe_allow_html=True,
        )

    try:
        from utils.audio_processor import process_input
        from core.transcriber import transcribe_all
        from core.summary import summarize, generate_title
        from core.extractor import extract_action_items, extract_key_decisions, extract_questions
        from core.rag_engine import build_rag_chain, ask_question

        # Step 0 – download
        mark(0, "active")
        with right:
            with st.spinner("Downloading / loading audio…"):
                chunks = process_input(source.strip())
        mark(0, "done")

        # Step 1 – transcribe
        mark(1, "active")
        with right:
            with st.spinner("Transcribing with Whisper…"):
                transcript = transcribe_all(chunks, language)
        mark(1, "done")

        # Step 2 – summarise
        mark(2, "active")
        with right:
            with st.spinner("Summarising…"):
                title   = generate_title(transcript)
                summary = summarize(transcript)
        mark(2, "done")

        # Step 3 – actions
        mark(3, "active")
        with right:
            with st.spinner("Extracting action items…"):
                action_items = extract_action_items(transcript)
        mark(3, "done")

        # Step 4 – decisions
        mark(4, "active")
        with right:
            with st.spinner("Extracting key decisions…"):
                decisions = extract_key_decisions(transcript)
        mark(4, "done")

        # Step 5 – questions
        mark(5, "active")
        with right:
            with st.spinner("Extracting open questions…"):
                questions = extract_questions(transcript)
        mark(5, "done")

        # Step 6 – RAG
        mark(6, "active")
        with right:
            with st.spinner("Building RAG index…"):
                rag_chain = build_rag_chain(transcript)
        mark(6, "done")
        mark(7, "done")

        st.session_state.result = {
            "title":         title,
            "transcript":    transcript,
            "summary":       summary,
            "action_items":  action_items,
            "key_decisions": decisions,
            "open_questions": questions,
            "rag_chain":     rag_chain,
        }

    except Exception as e:
        st.session_state.error = f"Pipeline failed: {e}"
        for i in range(8):
            if st.session_state.pipeline_state.get(i) == "active":
                st.session_state.pipeline_state[i] = "error"
        pipeline_placeholder.markdown(
            render_pipeline(st.session_state.pipeline_state),
            unsafe_allow_html=True,
        )
    finally:
        st.session_state.processing = False
        st.rerun()

elif run_btn and not source.strip():
    st.warning("Please enter a YouTube URL or file path first.")