"""Wave Packets — quantum uncertainty meets superposition."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── Post Metadata ────────────────────────────────────────────
TITLE = "Wave Packets"
ICON = "🌊"
DATE = "2026-02-10"
DESCRIPTION = "Visualize Gaussian wave packets and the uncertainty principle."
TAGS = ["quantum mechanics", "waves", "uncertainty"]


# ── Render Function ──────────────────────────────────────────
def render():
    st.title(f"{ICON} {TITLE}")

    st.markdown("""
    A wave packet is a localized disturbance built from the superposition of waves
    with different frequencies. They are central to quantum mechanics — the spread
    in position $\\Delta x$ and momentum $\\Delta p$ satisfy Heisenberg's uncertainty
    principle:
    """)

    st.latex(r"\Delta x \, \Delta p \;\geq\; \frac{\hbar}{2}")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Parameters")
        k0      = st.slider("Central Wave Number (k₀)", 5.0, 20.0, 10.0, 0.1)
        sigma_k = st.slider("Wave Number Width (Δk)", 0.5, 5.0, 2.0, 0.05)
        t       = st.slider("Time", 0.0, 2.0, 0.0, 0.01)

        st.markdown("""
        **Try it:**
        - Narrow Δk → Wide packet in space
        - Wide  Δk → Narrow packet
        """)

    with col2:
        x = np.linspace(-20, 20, 1000)
        psi = np.exp(1j * k0 * x - t) * np.exp(-x ** 2 / (4 * sigma_k ** 2))

        # Ghost reference at defaults (k0=10, sigma_k=2, t=0)
        psi_ref = np.exp(1j * 10 * x) * np.exp(-x ** 2 / (4 * 2.0 ** 2))

        fig = go.Figure()
        # Ghost envelope
        fig.add_trace(go.Scatter(x=x, y=np.abs(psi_ref) ** 2, mode='lines',
                                 line=dict(color='rgba(255,255,255,0.12)', width=2, dash='dot'),
                                 name='Reference |ψ|²'))
        fig.add_trace(go.Scatter(x=x, y=np.real(psi), mode='lines',
                                 line=dict(color='#3a75c4', width=2), name='Re(ψ)'))
        fig.add_trace(go.Scatter(x=x, y=np.imag(psi), mode='lines',
                                 line=dict(color='#FF6B6B', width=2), name='Im(ψ)'))
        fig.add_trace(go.Scatter(x=x, y=np.abs(psi) ** 2, mode='lines',
                                 fill='tozeroy',
                                 line=dict(color='#4ECDC4', width=3), name='|ψ|²'))

        fig.update_layout(
            title="Gaussian Wave Packet",
            xaxis_title="Position (x)",
            yaxis_title="Amplitude",
            template="plotly_dark",
            height=500,
            xaxis_range=[-20, 20],
            yaxis_range=[-1.3, 1.3],
            legend=dict(x=0.7, y=0.95),
        )
        st.plotly_chart(fig, width='stretch')
