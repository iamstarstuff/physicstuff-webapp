"""Lorenz Attractor — exploring chaos in 3-D."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── Post Metadata ────────────────────────────────────────────
TITLE = "Lorenz Attractor"
ICON = "🦋"
DATE = "2026-02-01"
DESCRIPTION = "Experience the butterfly effect through an interactive 3-D chaotic system."
TAGS = ["chaos", "dynamics", "attractor"]


# ── Cached computation (10 k-step Euler loop) ───────────────
@st.cache_data
def _integrate_lorenz(sigma, rho, beta, dt=0.01, num_steps=10_000):
    xs, ys, zs = np.empty(num_steps), np.empty(num_steps), np.empty(num_steps)
    xs[0], ys[0], zs[0] = 0.0, 1.0, 1.05
    for i in range(num_steps - 1):
        dx = sigma * (ys[i] - xs[i])
        dy = xs[i] * (rho - zs[i]) - ys[i]
        dz = xs[i] * ys[i] - beta * zs[i]
        xs[i + 1] = xs[i] + dx * dt
        ys[i + 1] = ys[i] + dy * dt
        zs[i + 1] = zs[i] + dz * dt
    return xs, ys, zs


# ── Render Function ──────────────────────────────────────────
def render():
    st.title(f"{ICON} {TITLE}")

    st.markdown("""
    The Lorenz attractor is a set of chaotic solutions to the Lorenz system,
    demonstrating how small changes in initial conditions can lead to vastly
    different outcomes — the famous **"butterfly effect"**.
    """)

    st.latex(r"\dot{x} = \sigma(y - x) \qquad \dot{y} = x(\rho - z) - y \qquad \dot{z} = xy - \beta z")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Parameters")
        sigma = st.slider("σ (Prandtl number)", 5.0, 15.0, 10.0, 0.1)
        rho   = st.slider("ρ (Rayleigh number)", 20.0, 35.0, 28.0, 0.1)
        beta  = st.slider("β", 1.0, 5.0, 8 / 3, 0.05)

        st.markdown("""
        **Try these:**
        - Classic: σ=10, ρ=28, β=2.67
        - Periodic: σ=10, ρ=21, β=2.67
        """)

    with col2:
        xs, ys, zs = _integrate_lorenz(sigma, rho, beta)

        fig = go.Figure(data=[go.Scatter3d(
            x=xs, y=ys, z=zs,
            mode='lines',
            line=dict(color=np.arange(len(xs)), colorscale='Viridis', width=2),
        )])
        fig.update_layout(
            title="Lorenz Attractor 3D",
            scene=dict(
                xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
                bgcolor='rgba(0,0,0,0)',
            ),
            template="plotly_dark",
            height=600,
        )
        st.plotly_chart(fig, width='stretch')
