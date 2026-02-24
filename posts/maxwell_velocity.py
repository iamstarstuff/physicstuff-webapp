"""Maxwell-Boltzmann Velocity Distribution."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── Post Metadata ────────────────────────────────────────────
TITLE = "Maxwell Velocity Distribution"
ICON = "🌡️"
DATE = "2026-02-05"
DESCRIPTION = "Understand molecular speeds at different temperatures for various gases."
TAGS = ["statistical mechanics", "thermodynamics", "kinetic theory"]


# ── Render Function ──────────────────────────────────────────
def render():
    st.title(f"{ICON} {TITLE}")

    st.markdown("""
    The Maxwell-Boltzmann distribution describes the distribution of particle
    speeds in an ideal gas at thermal equilibrium. It is fundamental to
    statistical mechanics and kinetic theory.
    """)

    st.latex(
        r"f(v) = 4\pi \left(\frac{m}{2\pi k_B T}\right)^{3/2}"
        r"\, v^2 \, \exp\!\left(-\frac{mv^2}{2k_B T}\right)"
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Parameters")
        T = st.slider("Temperature (K)", 100, 1000, 300, 5)
        gas = st.selectbox(
            "Particle",
            ["Hydrogen (H₂)", "Helium (He)", "Nitrogen (N₂)", "Oxygen (O₂)"],
            index=2,
        )

        mass_dict = {
            "Hydrogen (H₂)": 2.016e-3,
            "Helium (He)": 4.003e-3,
            "Nitrogen (N₂)": 28.014e-3,
            "Oxygen (O₂)": 31.998e-3,
        }

        m_kg = mass_dict[gas] / 6.022e23  # kg per molecule
        k_B = 1.380649e-23

        v_mean = np.sqrt(8 * k_B * T / (np.pi * m_kg))
        v_rms  = np.sqrt(3 * k_B * T / m_kg)
        v_prob = np.sqrt(2 * k_B * T / m_kg)

        st.markdown("---")
        st.metric("Mean Speed", f"{v_mean:.1f} m/s")
        st.metric("RMS Speed", f"{v_rms:.1f} m/s")
        st.metric("Most Probable Speed", f"{v_prob:.1f} m/s")

    with col2:
        # Fixed x-range so the curve visibly shifts with temperature
        v = np.linspace(0, 2500, 1000)
        f_v = (
            4 * np.pi
            * (m_kg / (2 * np.pi * k_B * T)) ** 1.5
            * v ** 2
            * np.exp(-m_kg * v ** 2 / (2 * k_B * T))
        )

        # Ghost reference: same gas at 300 K
        T_ref = 300
        f_ref = (
            4 * np.pi
            * (m_kg / (2 * np.pi * k_B * T_ref)) ** 1.5
            * v ** 2
            * np.exp(-m_kg * v ** 2 / (2 * k_B * T_ref))
        )

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=v, y=f_ref,
            mode='lines',
            line=dict(color='rgba(255,255,255,0.15)', width=2, dash='dot'),
            name='Reference (300 K)',
        ))
        fig.add_trace(go.Scatter(
            x=v, y=f_v,
            mode='lines', fill='tozeroy',
            line=dict(color='#FF6B6B', width=3),
            name=f'{gas} at {T} K',
        ))
        fig.add_vline(x=v_mean, line_dash="dash", line_color="cyan",
                      annotation_text=f"Mean {v_mean:.0f}", annotation_position="top")
        fig.add_vline(x=v_rms, line_dash="dash", line_color="yellow",
                      annotation_text=f"RMS {v_rms:.0f}", annotation_position="top")
        fig.add_vline(x=v_prob, line_dash="dash", line_color="lime",
                      annotation_text=f"v_p {v_prob:.0f}", annotation_position="top")

        # Fixed y-max to accommodate the tallest peak (H₂ at 100 K ~ 0.0045)
        y_max = max(np.max(f_v), np.max(f_ref)) * 1.25
        fig.update_layout(
            title=f"Maxwell-Boltzmann Distribution at {T} K",
            xaxis_title="Velocity (m/s)",
            yaxis_title="Probability Density",
            template="plotly_dark",
            height=500,
            xaxis_range=[0, 2500],
            yaxis_range=[0, y_max],
            legend=dict(x=0.65, y=0.95),
        )
        st.plotly_chart(fig, width='stretch')
