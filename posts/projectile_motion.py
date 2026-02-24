"""Projectile Motion — interactive trajectory simulation."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── Post Metadata ────────────────────────────────────────────
TITLE = "Projectile Motion"
ICON = "🎯"
DATE = "2026-01-15"
DESCRIPTION = "Explore parabolic trajectories with customizable velocity, angle, and gravity."
TAGS = ["mechanics", "kinematics"]


# ── Render Function ──────────────────────────────────────────
def render():
    st.title(f"{ICON} {TITLE}")

    # ── Introduction ─────────────────────────────────────────
    st.markdown("""
    Projectile motion is one of the first problems you encounter in classical
    mechanics — and one of the most elegant. An object is launched into the air
    with some initial speed $v_0$ at an angle $\\theta$ above the horizontal.
    After that moment, the **only** force acting on it is gravity (we ignore air
    resistance).

    Because gravity acts **only downward**, the motion separates neatly into two
    independent components:

    | Component | Acceleration | Velocity | Position |
    |-----------|-------------|----------|----------|
    | **Horizontal (x)** | $0$ | $v_{0x} = v_0\\cos\\theta$ (constant) | $x = v_0 \\cos\\theta\\; t$ |
    | **Vertical (y)** | $-g$ | $v_{0y} = v_0\\sin\\theta - g\\,t$ | $y = v_0 \\sin\\theta\\; t - \\tfrac{1}{2}g\\,t^2$ |

    Combining these gives the **parabolic trajectory**:
    """)

    st.latex(r"x(t) = v_0 \cos\theta \; t \qquad y(t) = v_0 \sin\theta \; t - \tfrac{1}{2}g\,t^2")

    st.markdown("""
    #### Key Derived Quantities

    From these equations we can derive three important results (assuming level
    ground, $y_0 = 0$):

    - **Time of flight:** $\\displaystyle T = \\frac{2\\,v_0 \\sin\\theta}{g}$
    - **Maximum height:** $\\displaystyle H = \\frac{v_0^2 \\sin^2\\theta}{2g}$
    - **Range:** $\\displaystyle R = \\frac{v_0^2 \\sin 2\\theta}{g}$

    Notice that the range depends on $\\sin 2\\theta$, which is maximised when
    $2\\theta = 90°$, i.e. $\\theta = 45°$. So for any given launch speed, a
    **45° angle** gives the longest range (in the absence of air resistance).
    """)

    st.info(
        "💡 **Symmetry insight:** Launch angles that add up to 90° "
        "(e.g. 30° and 60°) give the **same range** but very different "
        "trajectories. Try it below!"
    )

    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Parameters")
        v0 = st.slider("Initial Velocity (m/s)", 10.0, 100.0, 50.0, 1.0)
        angle = st.slider("Launch Angle (°)", 1.0, 90.0, 45.0, 0.5)
        g = st.slider("Gravity (m/s²)", 1.0, 20.0, 9.81, 0.01)

        angle_rad = np.radians(angle)
        v0x = v0 * np.cos(angle_rad)
        v0y = v0 * np.sin(angle_rad)

        time_of_flight = 2 * v0y / g if g > 0 else 0
        max_height_val = (v0y ** 2) / (2 * g) if g > 0 else 0
        range_val = v0x * time_of_flight

        st.markdown("---")
        st.metric("Time of Flight", f"{time_of_flight:.2f} s")
        st.metric("Max Height", f"{max_height_val:.2f} m")
        st.metric("Range", f"{range_val:.2f} m")

    with col2:
        t = np.linspace(0, time_of_flight, 300)
        x = v0x * t
        y = v0y * t - 0.5 * g * t ** 2

        # Ghost reference: default trajectory (v0=50, 45°, g=9.81)
        v0_ref, angle_ref, g_ref = 50.0, np.radians(45.0), 9.81
        tof_ref = 2 * v0_ref * np.sin(angle_ref) / g_ref
        t_ref = np.linspace(0, tof_ref, 300)
        x_ref = v0_ref * np.cos(angle_ref) * t_ref
        y_ref = v0_ref * np.sin(angle_ref) * t_ref - 0.5 * g_ref * t_ref ** 2

        # Max possible range/height (v0=100, angle=45/90, g=1)
        # range_max ~ 100²/1 = 10000, height_max ~ 100²/(2*1) = 5000
        # We use realistic bounds for g=9.81
        max_range = 100.0 ** 2 / g  # range at v0=100, angle=45
        max_height = 100.0 ** 2 / (2 * g)  # height at v0=100, angle=90

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_ref, y=y_ref,
            mode='lines',
            line=dict(color='rgba(255,255,255,0.15)', width=2, dash='dot'),
            name='Default (50 m/s, 45°)',
        ))
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            line=dict(color='#3a75c4', width=3),
            name='Trajectory',
        ))
        # Annotate landing point
        fig.add_trace(go.Scatter(
            x=[range_val], y=[0], mode='markers+text',
            marker=dict(size=10, color='cyan', symbol='x'),
            text=[f'{range_val:.0f} m'], textposition='top center',
            textfont=dict(color='cyan'), showlegend=False,
        ))
        # Annotate max height
        fig.add_trace(go.Scatter(
            x=[range_val / 2], y=[max_height_val], mode='markers+text',
            marker=dict(size=8, color='#FF6B6B', symbol='diamond'),
            text=[f'{max_height_val:.0f} m'], textposition='top center',
            textfont=dict(color='#FF6B6B'), showlegend=False,
        ))
        fig.update_layout(
            title="Projectile Trajectory",
            xaxis_title="Distance (m)",
            yaxis_title="Height (m)",
            template="plotly_dark",
            height=500,
            xaxis_range=[0, max_range * 1.05],
            yaxis_range=[0, max_height * 0.55],
            legend=dict(x=0.65, y=0.95),
        )
        st.plotly_chart(fig, width='stretch')

    # ── Post-plot explanation ─────────────────────────────────
    st.markdown("---")
    st.markdown("""
    #### 🔍 What to Observe

    - **Angle vs Range:** Set velocity to 50 m/s. Sweep the angle from 10° to 80°.
      Notice the range peaks at **45°**, and complementary angles (e.g. 30° & 60°)
      give the same range but different peak heights.
    - **Gravity's role:** Lower gravity (think Moon at ~1.62 m/s²) dramatically
      increases both range and height. On Jupiter (~24.8 m/s²), the same throw
      barely gets off the ground.
    - **Speed matters quadratically:** Doubling $v_0$ quadruples the range
      ($R \\propto v_0^2$). That's why a small increase in launch speed makes a
      huge difference.

    #### 🌍 Real-World Applications

    - **Sports:** Every ball sport involves projectile motion — from football
      goal-kicks to basketball free throws and cricket sixes.
    - **Artillery & Rocketry:** Ballistic trajectories were the original
      motivation for studying this problem (Galileo, 1638).
    - **Space launches:** Orbital mechanics begins where projectile motion
      meets the curvature of the Earth.

    #### ⚠️ Limitations of This Model

    This simulation assumes **no air resistance**. In reality, drag force
    ($F_d = \\tfrac{1}{2} C_d \\rho A v^2$) slows the projectile, reduces the
    range, and makes the trajectory **asymmetric** — the descending arc is
    steeper than the ascending one.
    """)
