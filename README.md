# PhysicStuff — Interactive Physics Blog 

An interactive physics blog built with Streamlit + Plotly.
Posts are modular: drop a new `.py` file in `posts/` and it appears automatically.

---

## Project Structure

```
PhysicStuff_Streamlit/
├── app.py                        # Main router (auto-discovers posts)
├── posts/                        # ← each file = one blog post
│   ├── __init__.py               #   post discovery logic
│   ├── _template.py              #   copy this to make a new post
│   ├── projectile_motion.py
│   ├── lissajous_figures.py
│   ├── lorenz_attractor.py
│   ├── maxwell_velocity.py
│   ├── wave_packets.py
│   ├── electric_field.py
│   └── fourier_synthesis.py
├── notebooks/                    # Jupyter notebooks (prototyping)
├── .streamlit/config.toml        # Theme & server config
├── requirements.txt
├── render.yaml                   # Render.com deployment
├── Procfile
└── README.md
```

---

## How to Add a New Blog Post

### Step 1 — Prototype in Jupyter (optional)

Write your physics simulation in a Jupyter notebook under `notebooks/`.
Get your Plotly plots and math working the way you like.

### Step 2 — Create the post file

```bash
cp posts/_template.py posts/my_new_topic.py
```

### Step 3 — Fill in metadata + render()

Edit `posts/my_new_topic.py`:

```python
TITLE       = "My New Topic"
ICON        = "🔭"
DATE        = "2026-03-01"          # newest-first sorting
DESCRIPTION = "One-liner for the home-page card"
TAGS        = ["astrophysics", "simulation"]

def render():
    st.title(f"{ICON} {TITLE}")
    st.markdown("Your intro text ...")

    col1, col2 = st.columns([1, 2])
    with col1:
        param = st.slider("Param", 0, 100, 50)
    with col2:
        fig = go.Figure(...)
        st.plotly_chart(fig, use_container_width=True)
```

### Step 4 — Done!

Restart the app. Your post appears in the sidebar and home page automatically.

---

## Local Development

```bash
conda activate codeastro
cd PhysicStuff_Streamlit
streamlit run app.py
```

Open http://localhost:8501

---

## Deploy to Render.com

1. Push to GitHub
2. On [render.com](https://render.com) → **New+ → Web Service** → connect the repo
3. Settings:
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
   - **Plan:** Free
4. Deploy — live at `https://your-app.onrender.com`

Or use the included `render.yaml` for Blueprint deploys.

---

## Tech Stack

| Layer       | Tool     |
|-------------|----------|
| Framework   | Streamlit |
| Plots       | Plotly    |
| Numerics    | NumPy     |
| Language    | Python 3.10+ |

---

© 2026 PhysicStuff
