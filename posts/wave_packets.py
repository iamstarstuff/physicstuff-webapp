"""Wave Packets — quantum uncertainty meets superposition."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from rate_limit import check_rate_limit

# ── Post Metadata ────────────────────────────────────────────
TITLE = "Wave Packets"
ICON = "🌊"
DATE = "2026-02-10"
DESCRIPTION = "Visualize Gaussian wave packets and the uncertainty principle."
TAGS = ["quantum mechanics", "wave-particle duality", "uncertainty principle"]


# ── Render Function ──────────────────────────────────────────
def render():
    st.title(f"{ICON} {TITLE}")

    st.markdown("""
    In quantum mechanics, particles are described not by a single position
    but by a **wave function** $\\psi(x,t)$. A *wave packet* is a localized
    disturbance built from the **superposition** of many plane waves with
    slightly different wave numbers $k$ (and thus different momenta
    $p = \\hbar k$).

    #### Why Wave Packets?

    A single plane wave $e^{ikx}$ extends infinitely in both directions —
    it describes a particle with perfectly known momentum but
    *completely unknown* position. By combining many such waves, we
    create a localized bump in $|\\psi|^2$ (the probability density), at
    the cost of introducing a spread in momentum.

    This trade-off is codified in **Heisenberg's uncertainty principle**:
    """)

    st.latex(r"\Delta x \, \Delta p \;\geq\; \frac{\hbar}{2}")

    st.markdown("""
    #### The Gaussian Wave Packet

    The simplest and most commonly used wave packet has a Gaussian envelope:

    $$\\psi(x,t) = e^{ik_0 x - i\\omega t} \\cdot e^{-x^2 / 4\\sigma_k^2}$$

    | Parameter | Symbol | Physical Meaning |
    |-----------|--------|------------------|
    | **Central wave number** | $k_0$ | Average momentum of the particle ($p_0 = \\hbar k_0$) |
    | **Wave number width** | $\\Delta k$ ($\\sigma_k$) | Spread in momentum — wider $\\Delta k$ means better position localization |
    | **Time** | $t$ | Evolution of the packet — in free space, it spreads over time (**dispersion**) |

    The probability density $|\\psi|^2$ tells you *where* the particle is
    most likely to be found.
    """)

    st.markdown("---")

    @st.fragment
    def _interactive():
        check_rate_limit()
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

        # ── Post-plot explanation ────────────────────────────────
        st.markdown("---")
        st.subheader("Things to Try")
        st.markdown("""
        1. **Narrow the wave-number width** ($\\Delta k \\to 0.5$) — the wave packet
           becomes very wide in position space. This is the uncertainty principle
           in action: less spread in momentum forces more spread in position.
        2. **Widen the wave-number width** ($\\Delta k \\to 5$) — the packet becomes
           tightly localized. At the extreme, the real and imaginary parts oscillate
           rapidly inside a narrow envelope.
        3. **Increase $k_0$** — the carrier wave oscillates faster (higher momentum
           particle), but the envelope width stays the same.
        4. **Advance time** — watch the packet spread out (disperse). In this
           simplified model the spreading is slow, but in a full quantum treatment
           the width grows as $\\sigma(t) = \\sigma_0 \\sqrt{1 + (\\hbar t / 2m\\sigma_0^2)^2}$.
        5. **Compare with the ghost reference** — the faint dotted curve shows the
           default $|\\psi|^2$ at $k_0=10$, $\\Delta k=2$, $t=0$, so you can see
           exactly how your changes affect the probability distribution.
        """)

        st.subheader("Key Concepts")
        st.markdown("""
        - **Group velocity vs. phase velocity**: The envelope (the bump) travels at the
          *group velocity* $v_g = d\\omega/dk$, while the internal oscillations
          travel at the *phase velocity* $v_p = \\omega/k$. These can differ!
        - **Dispersion**: If $\\omega(k)$ is not a linear function of $k$, different
          components travel at different speeds, causing the packet to spread over
          time. This is why quantum particles "delocalize" as they evolve.
        - **Born interpretation**: $|\\psi(x,t)|^2\\, dx$ is the probability of finding
          the particle between $x$ and $x + dx$. The teal-filled curve in the plot
          is this probability density.
        """)

        st.info("""
        **A note on this simulation** — The time evolution shown here is simplified.
        A full treatment requires solving the free-particle Schrodinger equation,
        which produces a complex-valued Gaussian that spreads in a specific way
        depending on the particle mass. The qualitative behaviour
        (spreading, oscillation) is faithfully captured.
        """)

    _interactive()
