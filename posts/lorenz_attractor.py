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
    The Lorenz attractor is one of the most iconic objects in the study of
    **chaos theory**. It arises from a simplified model of atmospheric
    convection proposed by meteorologist **Edward Lorenz** in 1963. Despite
    being governed by just three *deterministic* equations, the system exhibits
    wildly unpredictable behaviour — the famous **"butterfly effect"**.

    #### The Lorenz System

    The system consists of three coupled ordinary differential equations:
    """)

    st.latex(r"\dot{x} = \sigma(y - x) \qquad \dot{y} = x(\rho - z) - y \qquad \dot{z} = xy - \beta z")

    st.markdown("""
    | Parameter | Symbol | Physical Meaning |
    |-----------|--------|------------------|
    | **Prandtl number** | $\\sigma$ | Ratio of momentum diffusivity to thermal diffusivity |
    | **Rayleigh number** | $\\rho$ | Driving force — temperature difference across the fluid layer |
    | **Geometric factor** | $\\beta$ | Related to the aspect ratio of the convection cell |

    #### What Makes It Chaotic?

    - The system is **deterministic** — given exact initial conditions, the
      future is completely determined.
    - Yet it is **extremely sensitive to initial conditions**: two trajectories
      starting almost identically will diverge exponentially over time.
    - The trajectory never repeats exactly and never settles to a fixed point,
      yet it stays confined to a **strange attractor** — that butterfly-shaped
      region in 3D space.

    > *"Does the flap of a butterfly's wings in Brazil set off a tornado in
    > Texas?"* — Edward Lorenz, 1972
    """)

    st.markdown("---")

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

    # ── Post-plot explanation ────────────────────────────────
    st.markdown("---")
    st.subheader("Things to Try")
    st.markdown("""
    1. **Classic chaos** — Set $\\sigma = 10$, $\\rho = 28$, $\\beta = 8/3$.
       The trajectory should trace two lobes, switching unpredictably between
       them.
    2. **Edge of chaos** — Lower $\\rho$ toward **21**. The attractor collapses
       into a stable periodic orbit.
    3. **Increase $\\rho$ beyond 28** — Watch the attractor expand and the
       switching pattern become even more irregular.
    4. **Vary $\\sigma$** — A higher Prandtl number makes the trajectory
       "stickier" on each lobe before switching.
    """)

    st.subheader("Why Does It Matter?")
    st.markdown("""
    - **Weather prediction**: Lorenz's discovery showed that long-range weather
      forecasting has a fundamental limit — not because our models are bad, but
      because the atmosphere is inherently chaotic.
    - **Nature is full of chaos**: Turbulence in fluids, population dynamics,
      the double pendulum and even cardiac rhythms can exhibit similar
      behaviour.
    - **Strange attractors & fractals**: The Lorenz attractor has a fractal
      structure with a dimension of about **2.06**. It occupies zero volume in
      3-D space, yet has an infinite surface area.
    """)

    st.info("""
    **A note on the numerics** — This simulation uses the
    **Euler method** (simplest first-order integrator) with a fixed time step
    of 0.01. For chaotic systems, numerical errors grow exponentially, so
    the *specific* trajectory you see will diverge from the "true" solution
    after some time. However, the overall attractor shape and statistical
    properties are faithfully reproduced.
    """)
