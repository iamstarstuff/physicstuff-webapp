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
    harmonic motion. They appear whenever **two perpendicular oscillations** are
    combined — for instance on an oscilloscope when two sinusoidal signals are fed
    into the X and Y channels.

    #### The Equations

    A point traces out a Lissajous figure when its $(x, y)$ coordinates are
    driven by two independent sinusoidal functions:
    """)

    st.latex(r"x(t) = A\sin(a\,t + \delta) \qquad y(t) = B\sin(b\,t)")

    st.markdown("""
    | Parameter | Meaning |
    |-----------|--------|
    | $A$, $B$ | Amplitudes — control the **size** of the figure in x and y |
    | $a$, $b$ | Frequencies — their **ratio** $a : b$ determines the shape's complexity |
    | $\\delta$ | Phase shift — rotates / morphs the figure continuously |

    #### Why the Ratio Matters

    - When $a : b$ is a simple ratio (like 1:1, 1:2, 3:2) the curve **closes**
      and repeats after a finite time.
    - When $a : b$ is irrational (e.g. $\\sqrt{2} : 1$) the curve **never
      closes** — it fills a region of space over infinite time.
    - The number of lobes / crossings increases with the complexity of the ratio.

    #### Phase Shift

    At $\\delta = 0$ or $\\delta = \\pi$ with $a = b$, you get a straight line
    (the two oscillations are perfectly in-phase or anti-phase). At
    $\\delta = \\pi/2$ with $a = b$, you get a circle or ellipse.
    """)

    st.markdown("---")

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

    # ── Post-plot explanation ─────────────────────────────────
    st.markdown("---")
    st.markdown("""
    #### 🔍 Things to Try

    1. **Circle / Ellipse:** Set $a = b = 1$, $\\delta = \\pi/2$ (1.57). You'll
       see a perfect ellipse. Make $A = B$ and it becomes a circle.
    2. **Figure-8:** Set $a = 1$, $b = 2$, $\\delta \\approx \\pi/2$.
    3. **Infinity symbol:** $a = 2$, $b = 1$ traces the ∞ shape.
    4. **Slowly sweep δ:** Keep $a = 3$, $b = 2$ and drag δ from 0 to 2π.
       Watch the figure morph through strikingly different patterns.
    5. **High complexity:** Try $a = 7$, $b = 5$ — the number of lobes
       multiplies with the ratio's numerator and denominator.

    #### 🌍 Where Lissajous Figures Appear

    - **Oscilloscopes:** Historically used to compare two signal frequencies.
       The shape tells you the frequency ratio at a glance.
    - **Music & Acoustics:** Tuning forks held at right angles trace these
       patterns on smoked glass (a 19th-century experiment).
    - **Laser shows:** Mirrors vibrating at precise frequencies draw Lissajous
       patterns with laser beams.
    - **Mechanical engineering:** Vibration analysis of coupled oscillators
       reveals Lissajous-like motion in structural modes.
    """)
