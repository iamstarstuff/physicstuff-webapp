"""
Server-side rate limiter for Streamlit.

Tracks interaction counts per IP address in a global (server-level)
store, so refreshing the page does NOT reset the counters.
This is a lightweight defence — not a replacement for Cloudflare/WAF,
but it stops the Streamlit backend from doing expensive recomputation
when someone hammers sliders.
"""

import time
import threading
from collections import defaultdict

import streamlit as st

# ── Configurable limits ──────────────────────────────────────
MAX_INTERACTIONS_PER_MINUTE = 20   # slider moves / button clicks
COOLDOWN_SECONDS = 1800             # pause enforced when limit is hit

# ── Server-level store (persists across page refreshes) ──────
_lock = threading.Lock()
_ip_timestamps: dict[str, list[float]] = defaultdict(list)
_ip_blocked_until: dict[str, float] = defaultdict(float)


def _get_client_ip() -> str:
    """Best-effort client IP from Streamlit's request headers."""
    try:
        headers = st.context.headers
        # Proxies (Cloudflare / Render) pass the real IP in these headers
        for hdr in ("x-forwarded-for", "x-real-ip", "cf-connecting-ip"):
            val = headers.get(hdr)
            if val:
                return val.split(",")[0].strip()  # first IP in chain
    except Exception:
        pass
    return "unknown"


def check_rate_limit() -> bool:
    """Call at the top of every interactive fragment / render().

    Returns True if the request is allowed, False if throttled.
    When throttled, displays a warning and stops execution.
    """
    ip = _get_client_ip()
    now = time.time()

    with _lock:
        # If currently in cooldown, block
        if now < _ip_blocked_until[ip]:
            remaining = int(_ip_blocked_until[ip] - now) + 1
            st.warning(
                f"⏳ Too many interactions — please wait **{remaining}s** "
                f"before changing parameters again.",
                icon="🛡️",
            )
            st.stop()
            return False

        # Prune timestamps older than 60 s
        window_start = now - 60
        _ip_timestamps[ip] = [
            t for t in _ip_timestamps[ip] if t > window_start
        ]

        # Record this interaction
        _ip_timestamps[ip].append(now)

        # Check if over limit
        if len(_ip_timestamps[ip]) > MAX_INTERACTIONS_PER_MINUTE:
            _ip_blocked_until[ip] = now + COOLDOWN_SECONDS
            st.warning(
                f"⏳ You've exceeded {MAX_INTERACTIONS_PER_MINUTE} interactions "
                f"per minute. Cooling down for {COOLDOWN_SECONDS}s.",
                icon="🛡️",
            )
            st.stop()
            return False

    return True
