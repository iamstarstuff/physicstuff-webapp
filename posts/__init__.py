# Post registry - auto-discovers all post modules in this directory
import importlib
import pkgutil
import os

import streamlit as st


@st.cache_resource
def get_all_posts():
    """
    Scans the posts/ directory for Python modules that define blog posts.
    Each module must have: TITLE, ICON, DATE, DESCRIPTION, TAGS, render()
    Returns a dict of {title: module} sorted newest-first.
    Cached so module import happens only once per server lifetime.
    """
    posts = {}
    package_dir = os.path.dirname(__file__)

    for _, module_name, _ in pkgutil.iter_modules([package_dir]):
        if module_name.startswith("_"):
            continue  # skip __init__, _template, etc.

        try:
            module = importlib.import_module(f".{module_name}", package="posts")

            # Validate the module has required attributes
            required = ["TITLE", "ICON", "DATE", "DESCRIPTION", "TAGS", "render"]
            if all(hasattr(module, attr) for attr in required):
                module.SLUG = module_name  # e.g. "lorenz_attractor"
                posts[module.TITLE] = module
        except Exception as e:
            print(f"Warning: Could not load post module '{module_name}': {e}")

    # Sort by date (newest first)
    posts = dict(sorted(posts.items(), key=lambda x: x[1].DATE, reverse=True))
    return posts


def get_subjects(posts=None):
    """Group posts by primary subject (first tag, title-cased)."""
    if posts is None:
        posts = get_all_posts()
    subjects = {}
    for title, mod in posts.items():
        subject = mod.TAGS[0].title() if mod.TAGS else "Other"
        subjects.setdefault(subject, []).append(mod)
    # Sort posts within each subject by date (newest first)
    for subj in subjects:
        subjects[subj].sort(key=lambda m: m.DATE, reverse=True)
    return dict(sorted(subjects.items()))


def get_posts_by_slug(posts=None):
    """Return a dict mapping slug → module for URL-based lookup."""
    if posts is None:
        posts = get_all_posts()
    return {mod.SLUG: mod for mod in posts.values()}
