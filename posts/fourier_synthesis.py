"""Fourier Synthesis — building waveforms from sine waves."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── Post Metadata ────────────────────────────────────────────
TITLE = "Fourier Synthesis"
ICON = "🎵"
DATE = "2026-02-20"
DESCRIPTION = "See how complex waveforms emerge from simple sinusoidal harmonics."
TAGS = ["waves", "signal processing", "fourier"]


# ── Render Function ──────────────────────────────────────────
def render():
    st.title(f"{ICON} {TITLE}")

    st.markdown("""
    Fourier's theorem tells us that **any** periodic function can be expressed as
    a sum of sines and cosines. This is the backbone of signal processing, music
    synthesis, and much of modern physics.
    """)

    st.latex(
        r"f(t) = \frac{a_0}{2} + \sum_{n=1}^{\infty}"
        r"\bigl[a_n \cos(n\omega t) + b_n \sin(n\omega t)\bigr]"
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Wave Type")
        wave_type   = st.selectbox("Target Wave",
                                   ["Square Wave", "Sawtooth Wave", "Triangle Wave"])
        n_harmonics = st.slider("Number of Harmonics", 1, 30, 5)

        st.info(f"Using **{n_harmonics}** harmonics.\nMore harmonics → better approximation.")

    with col2:
        t = np.linspace(0, 2 * np.pi, 1000)
        y = np.zeros_like(t)

        for n in range(1, n_harmonics + 1):
            if wave_type == "Square Wave":
                if n % 2 == 1:
                    y += (4 / np.pi) * np.sin(n * t) / n
            elif wave_type == "Sawtooth Wave":
                y += (2 / np.pi) * np.sin(n * t) * (-1) ** (n + 1) / n
            elif wave_type == "Triangle Wave":
                if n % 2 == 1:
                    y += (8 / np.pi ** 2) * np.sin(n * t) * (-1) ** ((n - 1) / 2) / n ** 2

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=t, y=y,
            mode='lines',
            line=dict(color='#3a75c4', width=3),
        ))
        fig.update_layout(
            title=f"Fourier Synthesis: {wave_type}",
            xaxis_title="Time (radians)",
            yaxis_title="Amplitude",
            template="plotly_dark",
            height=500,
            showlegend=False,
        )
        st.plotly_chart(fig, width='stretch')
