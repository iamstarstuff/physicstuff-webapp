"""Statistics Fundamentals — interactive exploration of distributions and descriptive stats."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── Post Metadata ────────────────────────────────────────────
TITLE = "Statistics Fundamentals"
ICON = "📊"
DATE = "2026-02-24"
DESCRIPTION = "Learn mean, median, mode, standard deviation, and confidence intervals — visually."
TAGS = ["statistics", "data science", "probability"]


# ── Helpers ──────────────────────────────────────────────────
def normal_pdf(x, mu, sigma):
    """Gaussian probability density function (no scipy needed)."""
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


# ── Render Function ──────────────────────────────────────────
def render():
    st.title(f"{ICON} {TITLE}")

    # ── 1. Introduction ──────────────────────────────────────
    st.markdown("""
    Statistics is the grammar of science. Whether you're analysing experimental
    data, building machine-learning models, or simply reading a poll, you need a
    handful of core ideas to make sense of numbers. This post covers the essentials
    **interactively** — drag the sliders, watch the plots change, and build real
    intuition.

    ---
    ## 1 · Measures of Central Tendency
    """)

    st.markdown("""
    When we have a collection of data, the first question is usually:
    *"What is a typical value?"*  Three common answers:

    | Measure | Definition | When to use |
    |---------|-----------|-------------|
    | **Mean** ($\\bar{x}$) | Sum of all values ÷ count | Data is symmetric, no extreme outliers |
    | **Median** | Middle value when sorted | Skewed data or outliers present |
    | **Mode** | Most frequently occurring value | Categorical data or finding peaks |
    """)

    st.latex(r"\bar{x} = \frac{1}{N}\sum_{i=1}^{N} x_i")

    # ── Interactive: Mean / Median / Mode Demo ───────────────
    st.markdown("### Try it yourself")
    st.markdown("Adjust the data below and watch how mean, median, and mode react.")

    col_a, col_b = st.columns([1, 2])

    with col_a:
        distribution = st.selectbox(
            "Data shape",
            ["Symmetric", "Right-skewed", "Left-skewed", "Bimodal"],
            key="central_dist",
        )
        n_points = st.slider("Sample size", 50, 2000, 500, 50, key="central_n")
        add_outlier = st.checkbox("Add an extreme outlier", key="central_outlier")

    rng = np.random.default_rng(42)

    if distribution == "Symmetric":
        data = rng.normal(50, 10, n_points)
    elif distribution == "Right-skewed":
        data = rng.exponential(10, n_points) + 20
    elif distribution == "Left-skewed":
        data = 80 - rng.exponential(10, n_points)
    else:  # Bimodal
        half = n_points // 2
        data = np.concatenate([rng.normal(35, 5, half), rng.normal(65, 5, n_points - half)])

    if add_outlier:
        data = np.append(data, [200])

    mean_val = np.mean(data)
    median_val = np.median(data)
    # Mode via histogram binning (no scipy)
    counts, bin_edges = np.histogram(data, bins=30)
    mode_bin = np.argmax(counts)
    mode_val = (bin_edges[mode_bin] + bin_edges[mode_bin + 1]) / 2

    with col_a:
        st.markdown("---")
        st.metric("Mean", f"{mean_val:.2f}")
        st.metric("Median", f"{median_val:.2f}")
        st.metric("Mode (approx)", f"{mode_val:.2f}")

    with col_b:
        fig1 = go.Figure()
        fig1.add_trace(go.Histogram(
            x=data, nbinsx=40,
            marker_color='rgba(58,117,196,0.6)',
            name='Data',
        ))
        fig1.add_vline(x=mean_val, line_dash="solid", line_color="cyan",
                       annotation_text="Mean", annotation_position="top left")
        fig1.add_vline(x=median_val, line_dash="dash", line_color="yellow",
                       annotation_text="Median", annotation_position="top right")
        fig1.add_vline(x=mode_val, line_dash="dot", line_color="lime",
                       annotation_text="Mode", annotation_position="bottom right")
        fig1.update_layout(
            title="Histogram with Central Tendency Measures",
            xaxis_title="Value", yaxis_title="Count",
            template="plotly_dark", height=420, showlegend=False,
        )
        st.plotly_chart(fig1, width='stretch')

    st.info(
        "**Notice:** When data is symmetric, mean ≈ median ≈ mode. "
        "When skewed, the mean gets pulled toward the tail. "
        "Toggle the outlier checkbox to see how an extreme value drags the mean "
        "while the median barely moves — this is why median is called *robust*."
    )

    # ── 2. Spread / Dispersion ───────────────────────────────
    st.markdown("""
    ---
    ## 2 · Spread — Variance & Standard Deviation

    Central tendency tells us *where* the data sits; **spread** tells us
    *how scattered* it is.
    """)

    st.latex(r"\sigma^2 = \frac{1}{N}\sum_{i=1}^{N}(x_i - \bar{x})^2 \qquad \sigma = \sqrt{\sigma^2}")

    st.markdown("""
    - **Variance** ($\\sigma^2$): average squared distance from the mean.
    - **Standard deviation** ($\\sigma$): square root of variance — same units as the data, much easier to interpret.

    > *A small σ means data clusters tightly around the mean; a large σ means it's spread out.*
    """)

    # ── Interactive: σ explorer ───────────────────────────────
    st.markdown("### Explore the effect of standard deviation")

    col_c, col_d = st.columns([1, 2])

    with col_c:
        mu = st.slider("Mean (μ)", -10.0, 10.0, 0.0, 0.1, key="sd_mu")
        sigma1 = st.slider("σ₁", 0.5, 8.0, 1.0, 0.1, key="sd_s1")
        sigma2 = st.slider("σ₂", 0.5, 8.0, 3.0, 0.1, key="sd_s2")

        st.markdown(f"""
        | | σ₁ | σ₂ |
        |---|---|---|
        | **Value** | {sigma1:.1f} | {sigma2:.1f} |
        | **Variance** | {sigma1**2:.2f} | {sigma2**2:.2f} |
        | **Peak height** | {normal_pdf(mu, mu, sigma1):.4f} | {normal_pdf(mu, mu, sigma2):.4f} |
        """)

    with col_d:
        # Fixed axis range so the curve visibly moves when μ changes
        x = np.linspace(-35, 35, 800)
        fig2 = go.Figure()
        # Ghost: default reference (μ=0, σ=1)
        fig2.add_trace(go.Scatter(
            x=x, y=normal_pdf(x, 0, 1),
            mode='lines', line=dict(color='rgba(255,255,255,0.15)', width=2, dash='dot'),
            name='Reference (μ=0, σ=1)',
        ))
        fig2.add_trace(go.Scatter(
            x=x, y=normal_pdf(x, mu, sigma1),
            mode='lines', line=dict(color='#3a75c4', width=3),
            fill='tozeroy', name=f'σ₁ = {sigma1:.1f}',
        ))
        fig2.add_trace(go.Scatter(
            x=x, y=normal_pdf(x, mu, sigma2),
            mode='lines', line=dict(color='#FF6B6B', width=3),
            fill='tozeroy', name=f'σ₂ = {sigma2:.1f}',
        ))
        fig2.update_layout(
            title="Normal Distributions — same mean, different σ",
            xaxis_title="x", yaxis_title="Probability Density",
            template="plotly_dark", height=420,
            xaxis_range=[-35, 35],
            yaxis_range=[0, 0.85],
            legend=dict(x=0.68, y=0.95),
        )
        st.plotly_chart(fig2, width='stretch')

    st.info(
        "**Key insight:** A larger σ makes the bell curve *wider and shorter* "
        "(the area must always equal 1). A smaller σ makes it *narrower and taller*."
    )

    # ── 3. The Normal Distribution ───────────────────────────
    st.markdown("""
    ---
    ## 3 · The Normal (Gaussian) Distribution

    The most important distribution in all of statistics. It arises naturally
    whenever many small, independent effects add up (the **Central Limit Theorem**).

    Heights, measurement errors, IQ scores, and thermal noise are all approximately normal.
    """)

    st.latex(
        r"f(x) = \frac{1}{\sigma\sqrt{2\pi}}"
        r"\;\exp\!\left[-\frac{(x-\mu)^2}{2\sigma^2}\right]"
    )

    st.markdown("""
    ### The 68-95-99.7 Rule (Empirical Rule)

    For a normal distribution:

    | Range | % of data |
    |-------|-----------|
    | μ ± 1σ | **68.27 %** |
    | μ ± 2σ | **95.45 %** |
    | μ ± 3σ | **99.73 %** |
    """)

    # ── Interactive: Empirical Rule Visualiser ────────────────
    st.markdown("### Visualise the empirical rule")

    col_e, col_f = st.columns([1, 2])

    with col_e:
        mu_n = st.slider("Mean (μ)", -5.0, 5.0, 0.0, 0.1, key="norm_mu")
        sigma_n = st.slider("Std Dev (σ)", 0.5, 5.0, 1.0, 0.1, key="norm_sigma")
        n_sigma = st.radio("Shade region", ["1σ (68.27 %)", "2σ (95.45 %)", "3σ (99.73 %)"],
                           key="norm_shade")
        k = int(n_sigma[0])  # 1, 2, or 3

        area_pct = {1: 68.27, 2: 95.45, 3: 99.73}[k]
        st.markdown(f"""
        **Shaded region:** μ ± {k}σ = [{mu_n - k * sigma_n:.2f}, {mu_n + k * sigma_n:.2f}]

        Contains **{area_pct} %** of the distribution.
        """)

    with col_f:
        # Fixed viewport so the curve visibly slides when μ changes
        x = np.linspace(-30, 30, 1000)
        y = normal_pdf(x, mu_n, sigma_n)

        # Shaded region
        x_shade = np.linspace(mu_n - k * sigma_n, mu_n + k * sigma_n, 500)
        y_shade = normal_pdf(x_shade, mu_n, sigma_n)

        fig3 = go.Figure()
        # Ghost reference at default (μ=0, σ=1)
        fig3.add_trace(go.Scatter(
            x=x, y=normal_pdf(x, 0, 1),
            mode='lines', line=dict(color='rgba(255,255,255,0.12)', width=2, dash='dot'),
            name='Default (μ=0, σ=1)',
        ))
        # Shaded area
        fig3.add_trace(go.Scatter(
            x=np.concatenate([x_shade, x_shade[::-1]]),
            y=np.concatenate([y_shade, np.zeros_like(y_shade)]),
            fill='toself',
            fillcolor='rgba(58,117,196,0.35)',
            line=dict(color='rgba(0,0,0,0)'),
            name=f'{k}σ region ({area_pct}%)',
        ))
        # Full curve
        fig3.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines', line=dict(color='#3a75c4', width=3),
            name='N(μ, σ²)',
        ))
        # σ boundary lines with labels
        for i in range(1, k + 1):
            fig3.add_vline(x=mu_n - i * sigma_n, line_dash="dot", line_color="rgba(255,255,255,0.4)")
            fig3.add_vline(x=mu_n + i * sigma_n, line_dash="dot", line_color="rgba(255,255,255,0.4)")
        # Mean marker
        fig3.add_vline(x=mu_n, line_dash="solid", line_color="cyan",
                       annotation_text=f"μ = {mu_n:.1f}", annotation_position="top left")

        fig3.update_layout(
            title=f"Normal Distribution — {k}σ region shaded",
            xaxis_title="x", yaxis_title="Probability Density",
            template="plotly_dark", height=450,
            xaxis_range=[-30, 30],
            yaxis_range=[0, 0.85],
            legend=dict(x=0.60, y=0.95),
        )
        st.plotly_chart(fig3, width='stretch')

    # ── 4. Z-score ───────────────────────────────────────────
    st.markdown("""
    ---
    ## 4 · Z-Scores — Standardising Data

    A **z-score** tells you how many standard deviations a value is from the mean:
    """)

    st.latex(r"z = \frac{x - \mu}{\sigma}")

    st.markdown("""
    - $z = 0$ → the value **equals** the mean
    - $z = +2$ → the value is **2σ above** the mean
    - $z = -1.5$ → the value is **1.5σ below** the mean

    Z-scores let you compare values from *different* distributions on the same
    scale.
    """)

    col_g, col_h = st.columns([1, 2])

    with col_g:
        st.subheader("Z-score calculator")
        x_val = st.number_input("Your value (x)", value=72.0, key="z_x")
        mu_z = st.number_input("Population mean (μ)", value=65.0, key="z_mu")
        sigma_z = st.number_input("Population σ", value=5.0, min_value=0.01, key="z_sigma")

        z = (x_val - mu_z) / sigma_z
        st.metric("Z-score", f"{z:.3f}")

        if abs(z) < 1:
            st.success("Within 1σ — very typical value.")
        elif abs(z) < 2:
            st.warning("Between 1σ and 2σ — somewhat unusual.")
        else:
            st.error("Beyond 2σ — quite rare / statistically significant.")

    with col_h:
        x_range = np.linspace(mu_z - 4 * sigma_z, mu_z + 4 * sigma_z, 800)
        y_range = normal_pdf(x_range, mu_z, sigma_z)

        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=x_range, y=y_range,
            mode='lines', fill='tozeroy',
            line=dict(color='#3a75c4', width=3),
            name='Distribution',
        ))
        fig4.add_vline(x=x_val, line_dash="solid", line_color="red",
                       annotation_text=f"x = {x_val}  (z = {z:.2f})",
                       annotation_position="top left",
                       annotation_font_color="red")
        fig4.update_layout(
            title="Where does your value fall?",
            xaxis_title="x", yaxis_title="Probability Density",
            template="plotly_dark", height=400, showlegend=False,
        )
        st.plotly_chart(fig4, width='stretch')

    # ── 5. Confidence Intervals ──────────────────────────────
    st.markdown("""
    ---
    ## 5 · Confidence Intervals

    A **confidence interval (CI)** gives a *range* of plausible values for a
    population parameter (e.g. the true mean) based on sample data.
    """)

    st.latex(r"\text{CI} = \bar{x} \;\pm\; z^* \,\frac{\sigma}{\sqrt{n}}")

    st.markdown("""
    | Confidence Level | $z^*$ |
    |-----------------|-------|
    | 90 % | 1.645 |
    | 95 % | 1.960 |
    | 99 % | 2.576 |

    - **Larger sample size** ($n$) → **narrower** interval (more precision).
    - **Higher confidence level** → **wider** interval (more certainty costs precision).
    """)

    st.markdown("### Build a confidence interval")

    col_i, col_j = st.columns([1, 2])

    z_star_map = {"90%": 1.645, "95%": 1.960, "99%": 2.576}

    with col_i:
        sample_mean = st.number_input("Sample mean (x̄)", value=100.0, key="ci_mean")
        pop_sigma = st.number_input("Population σ", value=15.0, min_value=0.01, key="ci_sigma")
        n = st.slider("Sample size (n)", 5, 500, 30, key="ci_n")
        conf_level = st.select_slider("Confidence level", options=["90%", "95%", "99%"],
                                      value="95%", key="ci_level")

        z_star = z_star_map[conf_level]
        margin = z_star * (pop_sigma / np.sqrt(n))
        ci_low = sample_mean - margin
        ci_high = sample_mean + margin

        st.markdown("---")
        st.metric("Margin of Error", f"± {margin:.2f}")
        st.metric("CI Lower", f"{ci_low:.2f}")
        st.metric("CI Upper", f"{ci_high:.2f}")

    with col_j:
        # Show CI shrinking with sample size
        ns = np.arange(5, 501)
        margins = z_star * (pop_sigma / np.sqrt(ns))

        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=ns, y=sample_mean + margins,
            mode='lines', line=dict(color='#FF6B6B', width=2, dash='dash'),
            name='Upper bound',
        ))
        fig5.add_trace(go.Scatter(
            x=ns, y=sample_mean - margins,
            mode='lines', line=dict(color='#FF6B6B', width=2, dash='dash'),
            fill='tonexty', fillcolor='rgba(58,117,196,0.15)',
            name='Lower bound',
        ))
        fig5.add_hline(y=sample_mean, line_color="cyan", line_dash="dot",
                       annotation_text="x̄", annotation_position="bottom right")
        # Current n marker
        fig5.add_trace(go.Scatter(
            x=[n, n], y=[ci_low, ci_high],
            mode='lines+markers',
            line=dict(color='lime', width=3),
            marker=dict(size=8),
            name=f'n = {n}',
        ))
        fig5.update_layout(
            title=f"{conf_level} Confidence Interval vs Sample Size",
            xaxis_title="Sample size (n)", yaxis_title="Value",
            template="plotly_dark", height=420,
            legend=dict(x=0.7, y=0.95),
        )
        st.plotly_chart(fig5, width='stretch')

    st.info(
        "**Key takeaway:** Doubling your sample size does *not* halve the margin of "
        "error — it shrinks by a factor of $\\sqrt{2}$ ≈ 1.41. Diminishing returns "
        "mean there's a practical limit to how precise you can get."
    )

    # ── 6. Putting It All Together ───────────────────────────
    st.markdown("""
    ---
    ## 6 · Interactive Playground — Generate & Analyse

    Generate a random sample and see every concept above computed in one place.
    """)

    col_k, col_l = st.columns([1, 2])

    with col_k:
        play_mu = st.slider("True μ", -50.0, 50.0, 0.0, 0.5, key="play_mu")
        play_sigma = st.slider("True σ", 1.0, 30.0, 10.0, 0.25, key="play_sigma")
        play_n = st.slider("Sample size", 20, 2000, 200, 5, key="play_n")

        rng2 = np.random.default_rng(int(play_mu * 100 + play_sigma * 10 + play_n))
        sample = rng2.normal(play_mu, play_sigma, play_n)

        s_mean = np.mean(sample)
        s_median = np.median(sample)
        s_std = np.std(sample, ddof=1)
        s_var = np.var(sample, ddof=1)
        se = s_std / np.sqrt(play_n)
        ci95 = (s_mean - 1.96 * se, s_mean + 1.96 * se)

        st.markdown("---")
        st.markdown("**Sample statistics:**")
        st.metric("Mean", f"{s_mean:.3f}")
        st.metric("Median", f"{s_median:.3f}")
        st.metric("Std Dev", f"{s_std:.3f}")
        st.metric("Variance", f"{s_var:.3f}")
        st.metric("95% CI", f"[{ci95[0]:.2f}, {ci95[1]:.2f}]")

    with col_l:
        fig6 = go.Figure()

        fig6.add_trace(go.Histogram(
            x=sample, nbinsx=40,
            marker_color='rgba(58,117,196,0.5)',
            name='Sample', histnorm='probability density',
        ))

        # Overlay the true distribution
        x_ov = np.linspace(play_mu - 4 * play_sigma, play_mu + 4 * play_sigma, 500)
        fig6.add_trace(go.Scatter(
            x=x_ov, y=normal_pdf(x_ov, play_mu, play_sigma),
            mode='lines', line=dict(color='#FF6B6B', width=2, dash='dash'),
            name='True N(μ, σ²)',
        ))

        fig6.add_vline(x=s_mean, line_color="cyan", line_dash="solid",
                       annotation_text=f"x̄ = {s_mean:.2f}")
        fig6.add_vline(x=play_mu, line_color="red", line_dash="dot",
                       annotation_text=f"μ = {play_mu:.1f}")

        # Fixed viewport so histogram visibly shifts
        fig6.update_layout(
            title="Sample Histogram vs True Distribution",
            xaxis_title="Value", yaxis_title="Density",
            template="plotly_dark", height=450,
            xaxis_range=[play_mu - 5 * play_sigma, play_mu + 5 * play_sigma],
            legend=dict(x=0.7, y=0.95),
        )
        st.plotly_chart(fig6, width='stretch')

    st.success(
        "As you increase the sample size, notice how the sample mean converges "
        "toward the true μ and the 95 % CI gets narrower. "
        "This is the **Law of Large Numbers** in action!"
    )

    # ── 7. Summary ───────────────────────────────────────────
    st.markdown("""
    ---
    ## Quick Reference

    | Concept | Symbol | What it tells you |
    |---------|--------|-------------------|
    | Mean | $\\bar{x}$ | Average value |
    | Median | — | Middle value (robust to outliers) |
    | Mode | — | Most common value |
    | Variance | $\\sigma^2$ | Average squared spread |
    | Std Deviation | $\\sigma$ | Spread in original units |
    | Z-score | $z$ | How many σ from the mean |
    | Confidence Interval | CI | Range likely containing the true parameter |

    ### Further Reading
    - [Khan Academy — Statistics](https://www.khanacademy.org/math/statistics-probability)
    - [3Blue1Brown — But what is a normal distribution?](https://www.youtube.com/watch?v=zeJD6dqJ5lo)
    - [Seeing Theory — Brown University](https://seeing-theory.brown.edu/)
    """)
