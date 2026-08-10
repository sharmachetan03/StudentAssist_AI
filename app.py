import sys
import os
import re

# Ensure root directory is on sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import streamlit.components.v1 as components
from pipeline.orchestrator import PipelineOrchestrator

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="StudentAssist_AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Custom CSS Styling (Fixes Invisible Spinner Text & Enforces High Contrast)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* 1. Universal Slate Theme Enforcement */
    html, body, [data-testid="stAppViewContainer"], .stApp, [data-testid="stHeader"] {
        background-color: #0f172a !important;
        background-image: 
            radial-gradient(#1e293b 1px, transparent 1px),
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'%3E%3Cpath d='M25 15 l10 0 l0 20 l-10 0 z M28 10 l4 0 l0 5 l-4 0 z M22 35 l16 0 M20 40 l20 0' fill='none' stroke='%2338bdf8' stroke-width='1.0' stroke-dasharray='2,2' opacity='0.12'/%3E%3Ccircle cx='85' cy='30' r='10' fill='none' stroke='%2338bdf8' stroke-width='1.0' stroke-dasharray='2,2' opacity='0.12'/%3E%3Cpath d='M85 18 l0 -5 M80 42 l10 0' stroke='%2338bdf8' stroke-width='0.8' opacity='0.12'/%3E%3Cpath d='M15 85 l20 -10 l3 3 l-20 10 z M15 85 l-2 5 l5 -2 z' fill='none' stroke='%2338bdf8' stroke-width='1.0' opacity='0.12'/%3E%3Cpath d='M70 75 h20 v25 h-20 z M75 75 v25 M80 75 v25' fill='none' stroke='%2338bdf8' stroke-width='1.0' stroke-dasharray='2,2' opacity='0.12'/%3E%3C/svg%3E") !important;
        background-attachment: fixed !important;
        background-size: cover, 90px 90px !important;
        color: #f8fafc !important;
    }

    /* 2. Top Header Styling */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        background: transparent !important;
    }
    header[data-testid="stHeader"] * {
        color: #f8fafc !important;
    }

    /* 3. Eliminate Bottom Wrapper Backgrounds */
    footer,
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stChatInputContainer"],
    .stChatInputContainer {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* 4. Sidebar Custom Styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155 !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] caption,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #94a3b8 !important;
    }

    /* Clear Chat History Button Styling */
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] button[kind="secondary"],
    section[data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {
        background-color: #334155 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    }

    section[data-testid="stSidebar"] button *,
    section[data-testid="stSidebar"] button p,
    section[data-testid="stSidebar"] button span {
        color: #f8fafc !important;
        font-weight: 600 !important;
    }

    /* 5. Sidebar Inputs & Dropdowns */
    div[data-baseweb="input"] input, 
    div[data-baseweb="select"] div,
    input[type="text"] {
        color: #f8fafc !important;
        background-color: #1e293b !important;
        font-weight: 600 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 6px !important;
        -webkit-text-fill-color: #f8fafc !important;
    }

    /* 6. CHAT INPUT BAR FIX */
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div {
        background-color: #1e293b !important;
        border: 1.5px solid #38bdf8 !important;
        border-radius: 12px !important;
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.5) !important;
    }

    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] textarea * {
        color: #f8fafc !important;
        background-color: transparent !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        -webkit-text-fill-color: #f8fafc !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
    }

    /* 7. SPINNER TEXT VISIBILITY FIX */
    .stSpinner,
    [data-testid="stSpinner"],
    [data-testid="stSpinner"] * {
        color: #38bdf8 !important;
        font-weight: 600 !important;
    }

    /* 8. Main Content Layout & Typography */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 6rem !important;
        max-width: 1100px !important;
    }

    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown li {
        color: #f8fafc !important;
    }

    /* Parent Helper Guide Box */
    .style-guide-card {
        background-color: rgba(30, 41, 59, 0.85);
        border-left: 4px solid #38bdf8;
        padding: 12px 16px;
        border-radius: 8px;
        margin-top: 10px;
        margin-bottom: 20px;
        color: #e2e8f0;
        font-size: 0.95rem;
    }

    /* 9. Glassmorphic Cards for Chat Messages */
    .stChatMessage {
        background-color: rgba(30, 41, 59, 0.92) !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin-bottom: 16px !important;
        backdrop-filter: blur(8px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
    }
    
    /* Collapsible Details styling for solutions */
    details {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 8px;
        padding: 10px;
        margin-top: 8px;
    }
    summary {
        font-weight: bold;
        cursor: pointer;
        color: #38bdf8 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Dynamic Mermaid & Response Parsing Engine
# -----------------------------------------------------------------------------
def sanitize_markdown_text(text: str) -> str:
    """Pre-processes text to fix malformed LaTeX and squished single-line headers."""
    text = re.sub(r"([^\n])\s*(#{1,4}\s)", r"\1\n\n\2", text)
    text = re.sub(r"([^\n])\s*(\*\s+)([A-Z0-9])", r"\1\n\2\3", text)
    
    if "\\end{aligned}" in text and "\\begin{aligned}" not in text:
        text = text.replace("\\end{aligned}", "")
        
    return text


def render_assistant_response(text_content: str):
    """
    Parses response text, sanitizes markdown formatting errors, 
    isolates Mermaid blocks, and renders them cleanly.
    """
    text_content = sanitize_markdown_text(text_content)
    
    mermaid_pattern = r"```mermaid\s*\n?(.*?)\n?```"
    matches = list(re.finditer(mermaid_pattern, text_content, re.DOTALL))
    
    if not matches:
        if "graph TD" in text_content or "graph LR" in text_content:
            parts = re.split(r"(graph (?:TD|LR).*)", text_content, flags=re.DOTALL)
            for part in parts:
                if part.startswith("graph TD") or part.startswith("graph LR"):
                    cleaned_code = part.replace("subgraph", "\nsubgraph") \
                                       .replace("end", "\nend") \
                                       .replace("-->", " --> ")
                    _render_mermaid_html(cleaned_code)
                else:
                    if part.strip():
                        st.markdown(part, unsafe_allow_html=True)
            return

        st.markdown(text_content, unsafe_allow_html=True)
        return

    last_idx = 0
    for match in matches:
        start, end = match.span()
        if start > last_idx:
            st.markdown(text_content[last_idx:start], unsafe_allow_html=True)
            
        mermaid_code = match.group(1).strip()
        _render_mermaid_html(mermaid_code)
        last_idx = end
        
    if last_idx < len(text_content):
        st.markdown(text_content[last_idx:], unsafe_allow_html=True)


def _render_mermaid_html(mermaid_code: str):
    """Injects JavaScript Mermaid renderer into Streamlit component."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ 
                startOnLoad: true, 
                theme: 'dark',
                securityLevel: 'loose',
                themeVariables: {{
                    darkMode: true,
                    background: '#0f172a',
                    primaryColor: '#1e293b',
                    primaryTextColor: '#f8fafc',
                    primaryBorderColor: '#38bdf8',
                    lineColor: '#38bdf8',
                    secondaryColor: '#334155',
                    tertiaryColor: '#1e293b'
                }}
            }});
        </script>
        <style>
            body {{
                background-color: transparent;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .mermaid {{
                background: #1e293b !important;
                color: #f8fafc !important;
                border: 2px solid #38bdf8;
                border-radius: 10px;
                padding: 16px;
                width: 95%;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }}
            .mermaid text {{
                fill: #f8fafc !important;
                font-size: 14px !important;
            }}
        </style>
    </head>
    <body>
        <div class="mermaid">
        {mermaid_code}
        </div>
    </body>
    </html>
    """
    components.html(html_content, height=420, scrolling=True)


def auto_scroll_to_bottom():
    """Escapes iframe sandbox to smoothly scroll parent window to bottom."""
    js_scroll = """
    <script>
        setTimeout(function() {
            window.parent.document.querySelector('section.main').scrollTo({
                top: window.parent.document.querySelector('section.main').scrollHeight,
                behavior: 'smooth'
            });
        }, 150);
    </script>
    """
    components.html(js_scroll, height=0)


# -----------------------------------------------------------------------------
# 3. Session State Initialization
# -----------------------------------------------------------------------------
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = PipelineOrchestrator()

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------------------------------------------
# 4. Sidebar: Dynamic User & Curriculum Context Capture
# -----------------------------------------------------------------------------
st.sidebar.title("🎓 StudentAssist AI")
st.sidebar.caption("Personalized Academic & Pedagogical Partner")

st.sidebar.subheader("User Profile")
user_name = st.sidebar.text_input("Name", value="")
role = st.sidebar.selectbox("Role", ["Student", "Parent", "Teacher"])
grade = st.sidebar.selectbox(
    "Grade / Level", 
    ["Select Grade"] + [f"Grade {i}" for i in range(1, 13)] + ["Higher Education"], 
    index=5
)

st.sidebar.subheader("Curriculum & Pedagogy")
curriculum = st.sidebar.selectbox(
    "Curriculum / Board",
    [
        "NCERT / CBSE",
        "Karnataka State Board (KTBS)",
        "ICSE / CISCE",
        "General / International"
    ],
    help="Aligns explanations with textbook standards and terminology for this specific board."
)

learning_style = st.sidebar.selectbox(
    "Preferred Learning Style",
    [
        "Visual & Diagrammatic",
        "Step-by-Step Analytical",
        "Socratic / Guided Questioning",
        "Simplified / Storytelling"
    ]
)

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# -----------------------------------------------------------------------------
# 5. Main Chat Interface
# -----------------------------------------------------------------------------
st.title("📚 Interactive Learning Portal")
display_name = user_name.strip() if user_name.strip() else "Student"

# Welcome Banner
st.markdown(f"Welcome, **{display_name}**! Ask any subject question tailored to your **{curriculum}** syllabus.")

# Parent Helper Guide: Simple 1-line explanations for Learning Styles
STYLE_EXPLANATIONS = {
    "Visual & Diagrammatic": "📊 **Visual & Diagrammatic:** Teaches through flowcharts, mind maps, and diagrams—ideal for visual learners.",
    "Step-by-Step Analytical": "🧩 **Step-by-Step Analytical:** Breaks concepts down into logical, structured, numbered steps for deep understanding.",
    "Socratic / Guided Questioning": "💡 **Socratic / Guided Questioning:** Asks helpful guiding questions to encourage students to think and find answers themselves.",
    "Simplified / Storytelling": "📖 **Simplified / Storytelling:** Explains complex ideas using real-world analogies, stories, and easy everyday language."
}

# Render selected learning style explanation for parents
current_style_desc = STYLE_EXPLANATIONS.get(learning_style, "")
st.markdown(f'<div class="style-guide-card">ℹ️ <b>Parent Guide:</b> {current_style_desc}</div>', unsafe_allow_html=True)

# Render prior message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            render_assistant_response(msg["content"])
        else:
            st.markdown(msg["content"], unsafe_allow_html=True)

# Process active user input
if prompt := st.chat_input("Ask a question, concept, or math problem..."):
    # Render user prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Clean Chat History payload
    history_payload = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]

    # Package context payload for the pipeline orchestrator
    payload = {
        "user_input": prompt,
        "context": {
            "name": display_name,
            "role": role,
            "grade": grade,
            "curriculum": curriculum,
            "learning_style": learning_style
        },
        "history": history_payload
    }

    # Generate response via orchestrator
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.orchestrator.run_pipeline(payload)
                render_assistant_response(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Scroll parent window down to the latest answer
                auto_scroll_to_bottom()
            except Exception as e:
                error_msg = f"❌ An error occurred while generating the response: {str(e)}"
                st.error(error_msg)