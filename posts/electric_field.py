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
    The **electric field** $\\vec{E}$ is a vector field that permeates all of space
    around electric charges. It represents the force per unit charge that a small
    positive *test charge* would experience at every point.

    #### Coulomb's Law and the Electric Field

    For a single point charge $q$ located at the origin, the field at position
    $\\vec{r}$ is:
    """)

    st.latex(r"\vec{E} = \frac{1}{4\pi\epsilon_0}\,\frac{q}{r^2}\,\hat{r}")

    st.markdown("""
    | Symbol | Meaning |
    |--------|---------|
    | $\\epsilon_0$ | Permittivity of free space ($8.854 \\times 10^{-12}$ F/m) |
    | $q$ | Source charge (positive or negative) |
    | $r$ | Distance from the charge to the field point |
    | $\\hat{r}$ | Unit vector pointing from the charge to the field point |

    #### Superposition Principle

    If multiple charges are present, the total field is the **vector sum** of the
    individual fields:

    $$\\vec{E}_{\\text{total}} = \\sum_i \\vec{E}_i$$

    This is why adding a second charge doesn't replace the first field — the
    arrows you see in the plot are the combined contribution from *all* charges.

    #### Reading a Field-Line Diagram

    - **Direction** of each arrow shows the direction of the force on a positive
      test charge.
    - **Density** of arrows indicates field strength — closely packed arrows
      mean a stronger field.
    - Field lines **originate** at positive charges and **terminate** at
      negative charges (or at infinity).
    """)

    st.markdown("---")

    @st.fragment
    def _interactive():
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
            pts = np.linspace(-5, 5, 25)
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

        # ── Post-plot explanation ────────────────────────────────
        st.markdown("---")
        st.subheader("Things to Try")
        st.markdown("""
        1. **Single positive charge** — field lines radiate outward uniformly in all
           directions, weakening with distance ($1/r^2$).
        2. **Dipole** (one positive, one negative) — field lines arc from the
           positive charge to the negative charge. This is the most common
           configuration in nature (molecules, antennas, magnetic analogs).
        3. **Two positive charges** — field lines repel between the charges, creating
           a "dead zone" (saddle point) at the midpoint where $\\vec{E} = 0$.
        4. **Vary charge magnitudes** — make one charge much larger than the other
           to see how the field becomes dominated by the stronger source.
        5. **Change separation** — bring charges closer together to see the field
           intensify between them.
        """)

        st.subheader("Where Electric Fields Appear")
        st.markdown("""
        - **Capacitors**: Two parallel plates with opposite charges create a nearly
          uniform field between them — the basis of energy storage.
        - **Lightning**: Charge separation in clouds creates enormous fields
          ($\\sim 3 \\times 10^6$ V/m) that ionize air, causing dielectric breakdown.
        - **Biological systems**: The electric field across a cell membrane
          ($\\sim 10^7$ V/m over ~10 nm) drives nerve impulses and ion transport.
        - **Particle accelerators**: Carefully shaped electric fields accelerate
          charged particles to near light speed.
        """)

        st.info("""
        **Limitations of the visualization** — The quiver plot shows
        *normalized* arrows (all the same length) to keep the diagram readable.
        In reality, the field strength varies enormously — it's extremely strong
        near the charges and drops off as $1/r^2$. Also, this is a 2-D cross-section
        of what is really a 3-D field.
        """)

    _interactive()
