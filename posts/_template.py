"""
=============================================================
POST TEMPLATE - Copy this file to create a new blog post
=============================================================

HOW TO ADD A NEW POST:
1. Copy this file: cp posts/_template.py posts/my_new_topic.py
2. Fill in the metadata (TITLE, ICON, DATE, etc.)
3. Write your render() function using Streamlit + Plotly
4. Restart the app — your post appears automatically!

WORKFLOW (from Jupyter notebook):
1. Prototype your plots & math in a Jupyter notebook
2. Once happy, copy the code into render() below
3. Replace matplotlib/static plots with Plotly interactive ones
4. Add st.slider / st.selectbox for user-adjustable parameters
5. Use st.markdown() for your explanatory text

TIPS:
- Use col1, col2 = st.columns([1, 2]) for sidebar params + plot layout
- Use st.latex() for equations
- Use st.plotly_chart(fig, width='stretch') for responsive plots
- All Plotly figures should use template="plotly_dark"
=============================================================
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── Post Metadata ────────────────────────────────────────────
TITLE = "My New Post Title"
ICON = "🔬"                          # emoji shown in sidebar & cards
DATE = "2026-02-24"                  # YYYY-MM-DD (used for sorting)
DESCRIPTION = "A short one-liner describing this post."
TAGS = ["physics", "simulation"]     # used for filtering on home page


# ── Render Function ──────────────────────────────────────────
def render():
    """Main render function — called by app.py when user navigates here."""
    
    st.title(f"{ICON} {TITLE}")
    
    # ── Introduction (paste your notebook markdown here) ─────
    st.markdown("""
    Write your intro / explanation here. You can use **bold**, *italic*,
    LaTeX inline $E = mc^2$ and display equations:
    """)
    
    st.latex(r"F = ma")
    
    # ── Interactive Controls + Plot ──────────────────────────
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Parameters")
        param_a = st.slider("Parameter A", 1, 100, 50)
        param_b = st.slider("Parameter B", 0.1, 10.0, 1.0, 0.1)
    
    with col2:
        # Generate data
        x = np.linspace(0, 10, 500)
        y = param_a * np.sin(param_b * x)
        
        # Create Plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            line=dict(color='#3a75c4', width=3),
        ))
        fig.update_layout(
            title="My Plot",
            xaxis_title="X",
            yaxis_title="Y",
            template="plotly_dark",
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # ── More text / equations / plots below ──────────────────
    st.markdown("---")
    st.markdown("### Further Reading")
    st.markdown("Add references, links, etc.")
