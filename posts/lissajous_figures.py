"""Lissajous Figures — parametric harmonic curves."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── Post Metadata ────────────────────────────────────────────
TITLE = "Lissajous Figures"
ICON = "∞"
DATE = "2026-01-20"
DESCRIPTION = "Visualize the beautiful curves formed by two perpendicular oscillations."
TAGS = ["waves", "oscillations", "harmonic motion"]


# ── Render Function ──────────────────────────────────────────
def render():
    st.title(f"{ICON} {TITLE}")

    st.markdown("""
    Lissajous curves are the graphs of parametric equations that describe complex
    harmonic motion. They appear in systems where two perpendicular oscillations
    occur — for instance on an oscilloscope when two signals are fed into the X and
    Y channels.
    """)

    st.latex(r"x(t) = A\sin(a\,t + \delta) \qquad y(t) = B\sin(b\,t)")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Parameters")
        A = st.slider("Amplitude X", 1, 10, 5)
        B = st.slider("Amplitude Y", 1, 10, 5)
        a = st.slider("Frequency X", 1, 10, 3)
        b = st.slider("Frequency Y", 1, 10, 2)
        delta = st.slider("Phase Shift (δ)", 0.0, 6.28, 1.57, 0.01)

        st.markdown(f"**Frequency Ratio:** {a}:{b}")
        st.markdown(f"**Phase:** {delta:.2f} rad = {np.degrees(delta):.1f}°")

    with col2:
        t = np.linspace(0, 2 * np.pi, 2000)
        x = A * np.sin(a * t + delta)
        y = B * np.sin(b * t)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='markers',
            marker=dict(
                color=np.linspace(0, 1, len(t)),
                colorscale='Viridis',
                size=1.5,
                showscale=False,
            ),
        ))
        fig.update_layout(
            title="Lissajous Figure",
            xaxis_title="X",
            yaxis_title="Y",
            template="plotly_dark",
            height=500,
            showlegend=False,
            xaxis=dict(scaleanchor="y", scaleratio=1, range=[-11, 11]),
            yaxis=dict(range=[-11, 11]),
        )
        st.plotly_chart(fig, width='stretch')
