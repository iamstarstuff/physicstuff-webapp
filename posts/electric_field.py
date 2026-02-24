"""Electric Field — visualize fields from point charges."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff

# ── Post Metadata ────────────────────────────────────────────
TITLE = "Electric Field"
ICON = "⚡"
DATE = "2026-02-15"
DESCRIPTION = "Visualize electric field lines for various charge configurations."
TAGS = ["electromagnetism", "fields", "charges"]


# ── Render Function ──────────────────────────────────────────
def render():
    st.title(f"{ICON} {TITLE}")

    st.markdown("""
    The electric field $\\vec{E}$ at a point describes the force per unit charge
    that a positive test charge would feel. For a point charge $q$:
    """)

    st.latex(r"\vec{E} = \frac{1}{4\pi\epsilon_0}\,\frac{q}{r^2}\,\hat{r}")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Configuration")
        config = st.radio("Charge layout",
                          ["Single Charge", "Dipole", "Two Positive Charges"])
        q1 = st.slider("Charge 1 (μC)", -10, 10, 5)
        if config != "Single Charge":
            q2  = st.slider("Charge 2 (μC)", -10, 10, -5)
            sep = st.slider("Separation", 1.0, 5.0, 2.0, 0.5)

    with col2:
        # Grid
        pts = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(pts, pts)
        Ex = np.zeros_like(X)
        Ey = np.zeros_like(Y)

        # Charge 1 position
        x1, y1 = (0, 0) if config == "Single Charge" else (-sep / 2, 0)
        r1 = np.sqrt((X - x1) ** 2 + (Y - y1) ** 2 + 0.1)
        Ex += q1 * (X - x1) / r1 ** 3
        Ey += q1 * (Y - y1) / r1 ** 3

        # Charge 2
        if config != "Single Charge":
            x2, y2 = sep / 2, 0
            r2 = np.sqrt((X - x2) ** 2 + (Y - y2) ** 2 + 0.1)
            Ex += q2 * (X - x2) / r2 ** 3
            Ey += q2 * (Y - y2) / r2 ** 3

        # Normalize arrows for visibility
        mag = np.sqrt(Ex ** 2 + Ey ** 2)
        Ex_norm = Ex / (mag + 1e-8)
        Ey_norm = Ey / (mag + 1e-8)

        # Build quiver with plotly figure_factory
        fig = ff.create_quiver(
            X, Y, Ex_norm, Ey_norm,
            scale=0.3, arrow_scale=0.3,
            line=dict(color='#3a75c4', width=1),
            name='E field',
        )

        # Plot charge markers
        charges_x = [x1] if config == "Single Charge" else [x1, x2]
        charges_y = [y1] if config == "Single Charge" else [y1, y2]
        charges_q = [q1] if config == "Single Charge" else [q1, q2]

        for xi, yi, qi in zip(charges_x, charges_y, charges_q):
            color = 'red' if qi > 0 else 'blue'
            symbol = '+' if qi > 0 else '−'
            fig.add_trace(go.Scatter(
                x=[xi], y=[yi], mode='markers+text',
                marker=dict(size=18, color=color),
                text=[symbol], textfont=dict(size=16, color='white'),
                textposition='middle center',
                showlegend=False,
            ))

        fig.update_layout(
            title="Electric Field",
            xaxis_title="X", yaxis_title="Y",
            template="plotly_dark",
            height=550,
            xaxis=dict(scaleanchor='y', scaleratio=1),
        )
        st.plotly_chart(fig, width='stretch')
