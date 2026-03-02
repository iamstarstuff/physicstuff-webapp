"""Fourier Synthesis — building waveforms from sine waves."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from rate_limit import check_rate_limit

# ── Post Metadata ────────────────────────────────────────────
TITLE = "Fourier Synthesis"
ICON = "🎵"
DATE = "2026-02-20"
DESCRIPTION = "See how complex waveforms emerge from simple sinusoidal harmonics."
TAGS = ["waves & oscillations", "signal processing", "fourier analysis"]


# ── Render Function ──────────────────────────────────────────
def render():
    st.title(f"{ICON} {TITLE}")

    st.markdown("""
    In 1807, Joseph Fourier made a revolutionary claim: **any** periodic function
    — no matter how complicated — can be represented as a (possibly infinite) sum
    of simple sinusoids. This idea, now known as **Fourier's theorem**, underpins
    an enormous range of science and engineering, from audio compression (MP3) to
    quantum mechanics.

    #### The Fourier Series

    A periodic function $f(t)$ with period $T$ can be written as:
    """)

    st.latex(
        r"f(t) = \frac{a_0}{2} + \sum_{n=1}^{\infty}"
        r"\bigl[a_n \cos(n\omega t) + b_n \sin(n\omega t)\bigr]"
    )

    st.markdown("""
    where $\\omega = 2\\pi / T$ is the fundamental angular frequency and the
    coefficients $a_n$, $b_n$ determine how much of each harmonic is present.

    #### How Each Wave Is Built

    | Target Wave | Non-zero Terms | Series |
    |-------------|---------------|--------|
    | **Square wave** | Odd harmonics only ($n = 1, 3, 5, \\ldots$) | $\\frac{4}{\\pi} \\sum \\frac{\\sin(n t)}{n}$ |
    | **Sawtooth wave** | All harmonics | $\\frac{2}{\\pi} \\sum \\frac{(-1)^{n+1} \\sin(n t)}{n}$ |
    | **Triangle wave** | Odd harmonics only | $\\frac{8}{\\pi^2} \\sum \\frac{(-1)^{(n-1)/2} \\sin(n t)}{n^2}$ |

    Notice that the triangle wave coefficients fall off as $1/n^2$ (much faster
    than the square wave's $1/n$), which is why it converges more smoothly.

    #### The Gibbs Phenomenon

    No matter how many harmonics you add, a **sharp discontinuity** (like the
    jump in a square wave) will always have an overshoot of about **9%** near
    the edge. This is called the *Gibbs phenomenon* and is a fundamental
    limitation of Fourier series for discontinuous functions.
    """)

    st.markdown("---")

    @st.fragment
    def _interactive():
        check_rate_limit()
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

        # ── Post-plot explanation ────────────────────────────────
        st.markdown("---")
        st.subheader("Things to Try")
        st.markdown("""
        1. **Square wave with 1 harmonic** — you see a single sine wave. Add more
           harmonics and watch the waveform sharpen into a square shape.
        2. **Square wave with 30 harmonics** — zoom in on the discontinuity to see
           the **Gibbs overshoot** (~9% ripple that never goes away).
        3. **Triangle wave** — notice how quickly it converges even with just 3-5
           harmonics, because its coefficients decay as $1/n^2$.
        4. **Sawtooth wave** — uses *all* harmonics (both even and odd), so it
           converges differently from the square and triangle waves.
        5. **Compare all three** at the same number of harmonics to appreciate how
           smoothness of the target function affects convergence speed.
        """)

        st.subheader("Where Fourier Analysis Appears")
        st.markdown("""
        - **Audio & music**: Every musical instrument produces a unique mix of
          harmonics (timbre). The equalizer on your stereo adjusts individual
          Fourier components.
        - **Image compression** (JPEG): Images are decomposed into 2-D cosine
          components; discarding high-frequency ones compresses the file.
        - **Signal processing**: Filtering noise, designing antennas, and
          analysing seismic data all rely on Fourier transforms.
        - **Quantum mechanics**: The wave function in momentum space is the Fourier
          transform of the wave function in position space.
        - **Heat conduction**: Fourier originally developed his series to solve
          the heat equation — each harmonic decays at a rate proportional to $n^2$.
        """)

        st.info("""
        **From series to transform** — The Fourier *series* works for periodic
        functions. For non-periodic signals, we generalize to the **Fourier
        transform**, which decomposes a function into a *continuous* spectrum
        of frequencies rather than discrete harmonics.
        """)

    _interactive()
