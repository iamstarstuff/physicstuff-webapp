"""
Simple in-app rate limiter for Streamlit.

Tracks interaction counts per session and blocks excessive use.
This is a lightweight defence — not a replacement for Cloudflare/WAF,
but it stops the Streamlit backend from doing expensive recomputation
when someone hammers sliders.
"""

import time
import streamlit as st

# ── Configurable limits ──────────────────────────────────────
MAX_INTERACTIONS_PER_MINUTE = 30   # slider moves / button clicks
COOLDOWN_SECONDS = 15              # pause enforced when limit is hit


def _init_rate_state():
    """Initialise per-session rate-limit counters."""
    if "_rl_timestamps" not in st.session_state:
        st.session_state._rl_timestamps = []
    if "_rl_blocked_until" not in st.session_state:
        st.session_state._rl_blocked_until = 0.0


def check_rate_limit() -> bool:
    """Call at the top of every interactive fragment / render().

    Returns True if the request is allowed, False if throttled.
    When throttled, displays a warning and stops execution.
    """
    _init_rate_state()
    now = time.time()

    # If currently in cooldown, block
    if now < st.session_state._rl_blocked_until:
        remaining = int(st.session_state._rl_blocked_until - now) + 1
        st.warning(
            f"⏳ Too many interactions — please wait **{remaining}s** "
            f"before changing parameters again.",
            icon="🛡️",
        )
        st.stop()
        return False

    # Prune timestamps older than 60 s
    window_start = now - 60
    st.session_state._rl_timestamps = [
        t for t in st.session_state._rl_timestamps if t > window_start
    ]

    # Record this interaction
    st.session_state._rl_timestamps.append(now)

    # Check if over limit
    if len(st.session_state._rl_timestamps) > MAX_INTERACTIONS_PER_MINUTE:
        st.session_state._rl_blocked_until = now + COOLDOWN_SECONDS
        st.warning(
            f"⏳ You've exceeded {MAX_INTERACTIONS_PER_MINUTE} interactions "
            f"per minute. Cooling down for {COOLDOWN_SECONDS}s.",
            icon="🛡️",
        )
        st.stop()
        return False

    return True
