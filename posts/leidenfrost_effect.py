"""Leidenfrost Effect — when water droplets dance on hot surfaces."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from rate_limit import check_rate_limit

# ── Post Metadata ────────────────────────────────────────────
TITLE = "The Leidenfrost Effect"
ICON = "💧"
DATE = "2026-03-02"
DESCRIPTION = "Why water droplets dance and survive on scorching-hot surfaces instead of evaporating instantly."
TAGS = ["thermodynamics", "fluid dynamics", "phase transitions"]


# ── Physics model: droplet lifetime vs surface temperature ───
def _droplet_lifetime(T_surface, T_boil=100.0, T_leiden=193.0):
    """
    Simplified model of water-droplet lifetime on a hot surface.

    Three regimes:
      1. Nucleate boiling  (T_boil < T < T_leiden):
         Lifetime drops sharply as vigorous bubble nucleation
         accelerates evaporation.
      2. Transition region  (near T_leiden):
         Minimum lifetime — the most violent boiling regime.
      3. Film boiling / Leidenfrost  (T > T_leiden):
         Vapour layer insulates the droplet; lifetime *increases*.

    Returns lifetime in seconds for a ~2 mm water droplet.
    """
    T = np.atleast_1d(T_surface).astype(float)
    tau = np.zeros_like(T)

    # Below boiling — no rapid evaporation, droplet just sits
    mask_cold = T <= T_boil
    tau[mask_cold] = 60.0  # slow evaporation

    # Nucleate boiling regime: lifetime falls exponentially
    mask_nuc = (T > T_boil) & (T <= T_leiden)
    tau[mask_nuc] = 60.0 * np.exp(-4.0 * (T[mask_nuc] - T_boil) / (T_leiden - T_boil))

    # Film-boiling / Leidenfrost regime: lifetime rises again
    mask_film = T > T_leiden
    tau[mask_film] = tau[mask_nuc][-1] if mask_nuc.any() else 1.0
    tau[mask_film] = 1.1 + 30.0 * (1 - np.exp(-0.008 * (T[mask_film] - T_leiden)))

    return tau


# ── Render Function ──────────────────────────────────────────
def render():
    st.title(f"{ICON} {TITLE}")

    # ── Introduction ─────────────────────────────────────────
    st.markdown("""
    Here's something remarkably cool that happens when water meets a
    scorching-hot surface: instead of evaporating instantly, tiny droplets
    **bounce and skitter around**, surviving for far longer than you'd expect.
    This counter-intuitive behaviour is called the **Leidenfrost Effect**,
    named after the German doctor and theologian
    **Johann Gottlob Leidenfrost**, who first described it in 1751 in his
    treatise *A Tract About Some Qualities of Common Water*.
    """)

    st.image(
        "static/leidenfrost_effect/1024px-Leidenfrost_droplet.svg_.webp",
        caption="A water droplet levitating on a vapour cushion above a hot surface — the Leidenfrost effect in action.",
        width=600,
    )

    # ── How it works ─────────────────────────────────────────
    st.markdown("---")
    st.subheader("How Does It Work?")

    st.markdown("""
    When a liquid droplet lands on a surface that is **at or just above**
    its boiling point, it spreads out and evaporates rapidly — you hear a
    sharp hiss and it's gone in seconds. The liquid is in direct thermal
    contact with the metal, so heat flows efficiently through conduction
    and the droplet vaporises almost entirely through violent nucleate
    boiling.

    But raise the surface temperature **well beyond** the boiling point, and
    something qualitatively different happens. The bottom layer of the
    droplet — the thin shell in direct contact with the surface — vaporises
    **instantaneously** upon contact. This flash of vapour creates a thin
    insulating cushion, typically 10–100 µm thick, between the remaining
    liquid and the hot surface. Because steam has a thermal conductivity of
    only about 0.025 W·m⁻¹·K⁻¹ — roughly **15× lower** than stainless
    steel — heat transfer to the rest of the droplet slows dramatically.
    The vapour cushion simultaneously **levitates** the droplet, eliminating
    solid–liquid contact and friction, so the droplet glides and skitters
    freely across the surface. The result is that the droplet survives
    **much longer** than it would at lower temperatures where it boils
    violently on contact.
    """)

    st.image(
        "static/leidenfrost_effect/Drop - Martin.webp",
        caption="Close-up of a Leidenfrost droplet hovering on its own vapour layer.",
        width=600,
    )

    # ── The Leidenfrost Temperature ──────────────────────────
    st.markdown("---")
    st.subheader("The Leidenfrost Temperature")

    st.markdown("""
    The **Leidenfrost temperature** (or Leidenfrost point) is the minimum
    surface temperature at which the vapour cushion becomes stable enough to
    fully levitate the droplet. Below this temperature, the droplet still
    makes partial contact with the surface and boils away quickly.

    For **water**, the boiling point is 100 °C, but the Leidenfrost point
    is significantly higher — around **193 °C** on a polished metal surface.
    At pan temperatures between 100 °C and 193 °C, water droplets hiss
    violently and evaporate in seconds. Above 193 °C, they start to
    levitate and can survive for **over a minute**.

    | Liquid | Boiling Point (°C) | Approx. Leidenfrost Point (°C) |
    |--------|--------------------|-------------------------------|
    | Water  | 100  | ~193 |
    | Ethanol | 78  | ~130 |
    | Nitrogen (liquid) | −196 | −160 (on room-temp surface) |
    | Acetone | 56 | ~135 |

    > The exact Leidenfrost temperature depends on surface roughness,
    > material, droplet volume, and even atmospheric pressure.
    """)

    # ── Interactive simulation ───────────────────────────────
    st.markdown("---")
    st.subheader("Interactive: Droplet Lifetime vs. Surface Temperature")

    st.markdown("""
    The relationship between surface temperature and droplet lifetime is
    strikingly non-monotonic. One might naïvely expect that a hotter surface
    always evaporates a droplet faster, but the Leidenfrost effect inverts
    this logic. The plot below models the lifetime of a ~2 mm water droplet
    as a function of the surface temperature beneath it.

    In the **nucleate boiling** regime (between the boiling point and the
    Leidenfrost point), bubbles form directly at the liquid–surface
    interface, maximising the heat transfer coefficient — values can exceed
    $10^4 \\, \\text{W·m}^{-2}\\text{·K}^{-1}$ — and the droplet evaporates
    in just a few seconds. As the surface temperature crosses the
    Leidenfrost point, the heat transfer mode shifts abruptly to **film
    boiling**: the vapour layer's low thermal conductivity throttles the
    heat flux down to roughly $10^2 \\, \\text{W·m}^{-2}\\text{·K}^{-1}$,
    and the droplet lifetime rebounds sharply. This produces the
    characteristic **V-shaped curve** visible in the plot.
    """)

    @st.fragment
    def _interactive():
        check_rate_limit()
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Parameters")
            T_boil = st.slider("Boiling point (°C)", 50, 150, 100, 1)
            T_leiden = st.slider("Leidenfrost point (°C)", 120, 350, 193, 1)
            T_max = st.slider("Max surface temp (°C)", 250, 600, 450, 10)

            st.markdown(f"""
            At **{T_boil} °C** the liquid begins to boil on
            contact. The lifetime reaches its minimum near
            **{T_leiden} °C** where nucleate boiling is most
            violent. Above this Leidenfrost point, a stable
            vapour film forms and the droplet survives
            progressively longer as the insulating layer
            thickens.
            """)

        with col2:
            T = np.linspace(20, T_max, 500)
            tau = _droplet_lifetime(T, T_boil=T_boil, T_leiden=T_leiden)

            fig = go.Figure()

            # Lifetime curve
            fig.add_trace(go.Scatter(
                x=T, y=tau,
                mode='lines',
                line=dict(color='#00d4ff', width=3),
                name='Droplet lifetime',
            ))

            # Boiling point marker
            tau_boil = _droplet_lifetime(np.array([T_boil]), T_boil, T_leiden)
            fig.add_trace(go.Scatter(
                x=[T_boil], y=tau_boil,
                mode='markers+text',
                marker=dict(size=12, color='#ff6b6b', symbol='diamond'),
                text=[f'Boiling point ({T_boil} °C)'],
                textposition='top right',
                textfont=dict(color='#ff6b6b', size=11),
                name='Boiling point',
            ))

            # Leidenfrost point marker
            tau_leid = _droplet_lifetime(np.array([T_leiden]), T_boil, T_leiden)
            fig.add_trace(go.Scatter(
                x=[T_leiden], y=tau_leid,
                mode='markers+text',
                marker=dict(size=12, color='#ffd93d', symbol='star'),
                text=[f'Leidenfrost point ({T_leiden} °C)'],
                textposition='top right',
                textfont=dict(color='#ffd93d', size=11),
                name='Leidenfrost point',
            ))

            # Shaded regions
            fig.add_vrect(x0=20, x1=T_boil, fillcolor='#3a75c4', opacity=0.08,
                          annotation_text='Sub-boiling', annotation_position='top left',
                          annotation_font_color='#888')
            fig.add_vrect(x0=T_boil, x1=T_leiden, fillcolor='#ff6b6b', opacity=0.08,
                          annotation_text='Nucleate boiling', annotation_position='top left',
                          annotation_font_color='#888')
            fig.add_vrect(x0=T_leiden, x1=T_max, fillcolor='#ffd93d', opacity=0.08,
                          annotation_text='Film boiling (Leidenfrost)', annotation_position='top left',
                          annotation_font_color='#888')

            fig.update_layout(
                title="Water Droplet Lifetime on a Hot Surface",
                xaxis_title="Surface Temperature (°C)",
                yaxis_title="Droplet Lifetime (s)",
                template="plotly_dark",
                height=550,
                uirevision="leidenfrost",
                showlegend=False,
                yaxis=dict(range=[0, 70]),
            )
            st.plotly_chart(fig, width='stretch')

        # ── Post-plot explanation ────────────────────────────
        st.markdown("---")
        st.subheader("Understanding the Curve")
        st.markdown("""
        The three colour-shaded regions in the plot correspond to
        fundamentally different heat-transfer regimes.

        In the **sub-boiling** region (blue, $T < T_{\\text{boil}}$), the
        surface is not hot enough to trigger rapid phase change. The droplet
        loses mass slowly through ordinary convective evaporation and can
        persist for about a minute.

        In the **nucleate boiling** region (red,
        $T_{\\text{boil}} < T < T_{\\text{Leidenfrost}}$), the liquid makes
        direct contact with the superheated surface. Vapour bubbles nucleate
        at microscopic cavities on the metal, grow rapidly, and burst through
        the droplet surface, carrying away latent heat very efficiently. The
        heat transfer coefficient in this regime can be two orders of
        magnitude higher than in film boiling, which is why the droplet
        lifetime plunges to its minimum here.

        In the **film boiling / Leidenfrost** region (yellow,
        $T > T_{\\text{Leidenfrost}}$), the vapour production rate is so
        high that a continuous, stable gas film forms beneath the droplet.
        Heat must now cross this insulating gap primarily by conduction and
        radiation rather than direct contact, so the overall heat flux
        actually *decreases* despite the higher surface temperature. The
        droplet lifetime climbs back up, and the droplet levitates
        frictionlessly on its own vapour.

        > Try lowering the Leidenfrost point to simulate different liquids —
        > for example, ethanol transitions at roughly 130 °C, giving a much
        > narrower nucleate boiling window.
        """)

    _interactive()

    # ── Inverse Leidenfrost ──────────────────────────────────
    st.markdown("---")
    st.subheader("The Inverse Leidenfrost Effect")

    st.markdown("""
    The Leidenfrost effect also works in reverse: a **hot liquid droplet**
    can levitate on a **cold liquid surface** if the temperature difference
    is large enough.

    For example, Anaïs Gauthier's team at the University of Twente
    demonstrated this by depositing a room-temperature droplet of alcohol
    onto a pool of liquid nitrogen at **−196 °C**. The nitrogen at the
    interface vaporises instantly, creating the same insulating vapour
    cushion — but this time it's the *cold* liquid doing the evaporating.
    """)

    # ── Propelling droplets ──────────────────────────────────
    st.markdown("---")
    st.subheader("Propelling Droplets with Surface Texture")

    st.markdown("""
    On a flat hot surface, a Leidenfrost droplet drifts randomly because the
    vapour escaping from beneath it has no preferred direction. However, if
    the surface is textured with **asymmetric ratchet-like ridges** — tiny
    saw-tooth steps typically 0.1–1 mm tall — the escaping vapour is
    channelled preferentially along the shallower slope of each ridge. This
    creates a net viscous drag on the vapour film in one direction, which in
    turn propels the droplet along the surface like a miniature hovercraft
    with a built-in jet. The thrust is modest (on the order of micronewtons)
    but sufficient to accelerate the nearly frictionless droplet to speeds
    of several centimetres per second — and even to **drive it uphill**
    against gravity.
    """)

    st.video("static/leidenfrost_effect/using-the-leidenfrost-effect-to-propel-water-drops-uphill.mp4")

    # ── Leidenfrost thermostat ───────────────────────────────
    st.markdown("---")
    st.subheader("A Thermostat with No Moving Parts")

    st.markdown("""
    This directional propulsion has a clever application: a **Leidenfrost
    thermostat** — a temperature regulator with **no moving parts**.
    When the ratcheted surface is above the Leidenfrost point, water
    droplets are propelled toward the heat source, where they absorb
    thermal energy and cool it down through evaporative heat extraction.
    As the surface cools below the Leidenfrost point, the stable vapour
    film collapses, the self-propulsion ceases, and the droplets either
    boil away on contact or drift in the opposite direction — allowing
    the surface to heat back up. The system therefore self-regulates
    around the Leidenfrost temperature without any electronics, sensors,
    or mechanical parts. Published in the *Journal of Heat Transfer*, the
    concept was demonstrated by undergraduate students in this short film:
    """)

    # Embed Vimeo video
    st.markdown("""
    <div style="padding:56.25% 0 0 0;position:relative;">
        <iframe src="https://player.vimeo.com/video/128153030?h=&title=0&byline=0&portrait=0"
                style="position:absolute;top:0;left:0;width:100%;height:100%;"
                frameborder="0" allow="autoplay; fullscreen; picture-in-picture"
                allowfullscreen>
        </iframe>
    </div>
    """, unsafe_allow_html=True)

    # ── Dangerous stunts ─────────────────────────────────────
    st.markdown("---")
    st.subheader("Leidenfrost in Everyday Life (Don't Try This at Home)")

    st.markdown("""
    The Leidenfrost effect explains some seemingly impossible stunts that
    occasionally appear in viral videos. When someone
    [dips a wet finger into molten lead](https://www.youtube.com/watch?v=yTOCAd2QhGg)
    (melting point 327 °C), the thin film of moisture on the skin flash-
    vaporises on contact, generating a transient steam barrier that
    insulates the finger for a fraction of a second. The same principle is
    at work when a person
    [slaps a stream of molten metal](https://www.youtube.com/watch?v=-cfcsdGODMA)
    with a wet hand — the vapour shield deflects the liquid metal before
    it can transfer lethal amounts of heat to the skin. Even blowing out a
    mouthful of liquid nitrogen relies on a variant of the effect: the
    enormous temperature gap between body temperature (~37 °C) and liquid
    nitrogen (−196 °C) instantly generates an insulating vapour layer on
    every tissue surface the nitrogen touches.

    > ⚠️ **These stunts are extremely dangerous.** The Leidenfrost
    > protection lasts only for **fractions of a second** and depends on
    > precise conditions — correct moisture level, very brief contact time,
    > and a clean surface. Any prolonged contact causes severe burns or
    > frostbite. Do not attempt them.
    """)

    # ── Further reading ──────────────────────────────────────
    st.markdown("---")
    st.subheader("Further Reading")
    st.markdown("""
    - Leidenfrost, J. G. (1756). *De Aquae Communis Nonnullis Qualitatibus Tractatus.*
    - Quéré, D. (2013). "Leidenfrost Dynamics." *Annual Review of Fluid Mechanics*, 45, 197–215.
    - Gauthier, A. et al. (2019). "Self-propulsion of inverse Leidenfrost drops on a cryogenic bath." *PNAS*.
    - Linke, H. et al. (2006). "Self-propelled Leidenfrost droplets." *Physical Review Letters*, 96(15).
    """)
