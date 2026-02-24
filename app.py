"""
PhysicStuff — Interactive Physics Blog
=======================================
Posts are auto-discovered from the  posts/  directory.
To add a new post:  cp posts/_template.py posts/my_topic.py  → edit → done.
"""

import base64
from pathlib import Path

import streamlit as st
from PIL import Image
from posts import get_all_posts, get_subjects


# ── Image helpers (inline base-64 so images work everywhere) ─
@st.cache_data
def _load_image_b64(path: str) -> str:
    data = Path(path).read_bytes()
    return base64.b64encode(data).decode()


_STATIC = Path(__file__).parent / "static"
LOGO_B64 = _load_image_b64(_STATIC / "Logo.png")
HEADER_B64 = _load_image_b64(_STATIC / "Header.png")
LOGO_IMG = Image.open(_STATIC / "Logo.png")  # PIL Image for favicon

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="PhysicStuff — Interactive Physics Blog",
    page_icon=LOGO_IMG,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS (mobile-friendly + dark theme) ────────────────
st.markdown("""
<style>
    @media (max-width: 768px) {
        .block-container { padding: 1rem; }
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.2rem !important; }
    }
    .stPlotlyChart { background-color: transparent; }
    [data-testid="stSidebar"] { background-color: #1E1E1E; }
    .post-card {
        padding: 1.2rem 1.5rem; border-radius: 0.75rem; margin: 0.75rem 0;
        background-color: rgba(58, 117, 196, 0.08);
        border-left: 4px solid #3a75c4;
        transition: background-color 0.2s;
    }
    .post-card:hover {
        background-color: rgba(58, 117, 196, 0.15);
    }
    .post-card h4 { margin-top: 0; }
    .tag {
        display: inline-block; font-size: 0.75rem; padding: 2px 8px;
        border-radius: 12px; margin-right: 4px;
        background-color: rgba(58, 117, 196, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# ── Session State ────────────────────────────────────────────
if "current_post" not in st.session_state:
    st.session_state.current_post = None

# ── Discover & Group Posts ───────────────────────────────────
posts = get_all_posts()           # dict  {title: module}  sorted newest-first
subjects = get_subjects(posts)    # dict  {subject: [modules]}

SUBJECT_ICONS = {
    "Chaos": "🦋",
    "Electromagnetism": "⚡",
    "Mechanics": "📐",
    "Quantum Mechanics": "⚛️",
    "Statistical Mechanics": "🌡️",
    "Statistics": "📊",
    "Waves": "🌊",
}

# ── Sidebar Navigation ──────────────────────────────────────
st.sidebar.markdown(
    f'<div style="text-align:center;padding:0.5rem 0 0.25rem;">'
    f'<img src="data:image/png;base64,{LOGO_B64}" '
    f'style="width:80%;max-width:220px;border-radius:12px;" />'
    f'</div>',
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

# Build navigation options and a reverse-lookup map
nav_items = ["🏠 Home"]
nav_to_key = {"🏠 Home": ("home", None)}

for subj in subjects:
    icon = SUBJECT_ICONS.get(subj, "📁")
    label = f"{icon} {subj}"
    nav_items.append(label)
    nav_to_key[label] = ("subject", subj)

nav_items.append("ℹ️ About")
nav_to_key["ℹ️ About"] = ("about", None)


def _on_nav_change():
    """Clear the active post whenever the user picks a different page."""
    st.session_state.current_post = None


choice = st.sidebar.selectbox(
    "Navigate to:", nav_items,
    key="nav_select",
    on_change=_on_nav_change,
)

st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Streamlit")
st.sidebar.markdown("© 2026 PhysicStuff")


# ── Helpers ──────────────────────────────────────────────────
def _render_card(mod, key_suffix=""):
    """Render a single-column post card with an *Open* button."""
    tags_html = "".join(f'<span class="tag">{t}</span>' for t in mod.TAGS)
    st.markdown(f"""
    <div class="post-card">
        <h4>{mod.ICON} {mod.TITLE}</h4>
        <p style="margin:4px 0; color:#aaa; font-size:0.85rem;">{mod.DATE}</p>
        <p>{mod.DESCRIPTION}</p>
        {tags_html}
    </div>
    """, unsafe_allow_html=True)
    if st.button(
        f"Open {mod.ICON} {mod.TITLE}",
        key=f"open_{mod.TITLE}{key_suffix}",
        use_container_width=True,
    ):
        st.session_state.current_post = mod.TITLE
        st.rerun()


# ── Routing ──────────────────────────────────────────────────
page_type, page_value = nav_to_key.get(choice, ("home", None))


# ─ Individual Post View ──────────────────────────────────────
if st.session_state.current_post and st.session_state.current_post in posts:
    if st.button("← Back"):
        st.session_state.current_post = None
        st.rerun()
    posts[st.session_state.current_post].render()


# ─ Home Page ─────────────────────────────────────────────────
elif page_type == "home":
    # Full-width header banner
    st.markdown(
        f'<div style="text-align:center;margin-bottom:1.5rem;">'
        f'<img src="data:image/png;base64,{HEADER_B64}" '
        f'style="width:100%;max-width:900px;border-radius:12px;" />'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Interactive Physics Simulations & Visualizations")
    st.markdown(
        "Adjust parameters, see real-time updates, and build intuition "
        "about physical phenomena.  **Pick a subject from the sidebar** "
        "or browse the posts below."
    )
    st.markdown("---")

    for subj, mods in subjects.items():
        icon = SUBJECT_ICONS.get(subj, "📁")
        st.subheader(f"{icon} {subj}")
        for mod in mods:
            _render_card(mod, key_suffix="_home")
        st.markdown("")


# ─ About Page ────────────────────────────────────────────────
elif page_type == "about":
    st.markdown(
        f'<div style="text-align:center;margin-bottom:1rem;">'
        f'<img src="data:image/png;base64,{HEADER_B64}" '
        f'style="width:100%;max-width:900px;border-radius:12px;" />'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.title("About PhysicStuff")

    # ── The Project ───────────────────────────────────────────
    st.markdown("""
    This interactive physics blog brings concepts to life through
    visualizations and simulations. Rather than just reading about physics,
    you can **experience** it — tweak parameters, watch plots update in
    real-time, and build intuition about physical phenomena.

    #### 🎯 Mission
    Make physics accessible, intuitive, and fun through interactive learning.
    """)

    st.markdown("---")

    # ── About the Author ─────────────────────────────────────
    st.markdown("### 👨‍🔬 About the Author")

    col_pic, col_bio = st.columns([1, 3])
    with col_pic:
        st.markdown(
            f'<img src="data:image/png;base64,{LOGO_B64}" '
            f'style="width:100%;border-radius:50%;" />',
            unsafe_allow_html=True,
        )
    with col_bio:
        st.markdown("""
        **Hi, I'm Pratik!** 👋

        I am currently working as a **Data Engineer** in the
        Payments & Splunk CoE (Center of Excellence) teams at **AIB, Ireland**.
        My interests lie in finance, NLP, neural networks, ML, and Big Data.

        I am an **amateur astronomer** and **astrophotographer**, passionate
        about science, technology, and art.

        I hold a **Masters in Data Science** from South East Technological
        University (SETU), Ireland, and a **BSc & MSc in Physics** from the
        University of Mumbai.
        """)

    st.markdown("---")

    # ── Links ─────────────────────────────────────────────────
    st.markdown("### 🔗 Find Me Online")
    link_cols = st.columns(4)
    with link_cols[0]:
        st.markdown("[🐙 GitHub](https://github.com/iamstarstuff)")
    with link_cols[1]:
        st.markdown("[💼 LinkedIn](https://linkedin.com/in/pratik-barve/)")
    with link_cols[2]:
        st.markdown("[🐦 Twitter / X](https://twitter.com/astropratikb)")
    with link_cols[3]:
        st.markdown("[🌐 Portfolio](https://iamstarstuff.github.io/)")

    st.markdown("---")

    # ── Projects ──────────────────────────────────────────────
    st.markdown("### 🚀 Featured Projects")
    st.markdown("""
    - **[PhysicStuff](https://github.com/iamstarstuff/PhysicStuff)** —
      Visualizing physics concepts using Python
    - **[maglimit](https://github.com/iamstarstuff/maglimit)** —
      Determine observability of astronomical objects using magnitude
      and telescope limiting magnitude
    - **[Detailed CV (PDF)](https://iamstarstuff.github.io/pratik-barve-cv/cv.pdf)**
    """)

    st.markdown("---")

    # ── Tech Stack ────────────────────────────────────────────
    st.markdown("### 🔧 Tech Stack")
    st.markdown("""
    | Category | Tools |
    |----------|-------|
    | **Languages** | Python, R, SQL |
    | **Data Science** | NumPy, Pandas, Scikit-learn, TensorFlow, Keras |
    | **Visualization** | Plotly, Matplotlib, Streamlit |
    | **Environment** | Jupyter, Anaconda, Google Colab, VS Code |
    | **This App** | Streamlit + Plotly + NumPy, hosted on Render.com |
    """)


# ─ Subject Page ──────────────────────────────────────────────
elif page_type == "subject" and page_value in subjects:
    icon = SUBJECT_ICONS.get(page_value, "📁")
    st.title(f"{icon} {page_value}")
    st.markdown(f"Explore all posts in **{page_value}**")
    st.markdown("---")
    for mod in subjects[page_value]:
        _render_card(mod)
