<h1 align="center">AI Imager</h1>

<p align="center">
  <img width="80" height="80" src="https://github.com/xcasper/ai-imager/raw/main/contents/static/image/favicon.svg" alt="AI Imager Logo"/>
  <br><br>
  <a href="https://github.com/xcasper/ai-imager"><img src="https://img.shields.io/badge/GitHub-ai--imager-181717?logo=github&style=flat-square" alt="GitHub"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-yellow?style=flat-square" alt="License"/></a>
  <a href="https://apis.xcasper.space"><img src="https://img.shields.io/badge/Powered_by-Casper_Tech_APIs-7c3aed?style=flat-square" alt="Casper Tech APIs"/></a>
  <a href="https://xcasper.space"><img src="https://img.shields.io/badge/Homepage-xcasper.space-06b6d4?style=flat-square" alt="Homepage"/></a>
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white&style=flat-square" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-3.x-000000?logo=flask&style=flat-square" alt="Flask"/>
  <img src="https://img.shields.io/badge/No_API_Key-Required-22c55e?style=flat-square" alt="No API Key"/>
</p>

<p align="center">
  A modern, open-source web application for generating and manipulating images using free AI APIs — <strong>no API key required</strong>.
</p>

---

## Features

- **Text to Image** — Generate images from any text prompt using the DeepAI engine
- **Magic Studio** — High-quality image generation via Casper Tech APIs
- **Image + Mask** — Edit specific regions of an image using a text prompt and mask
- **Image Variations** — Generate creative variations from a reference image
- **Generation History** — Session-based history of all generated images
- **API Reference** — Built-in interactive documentation at `/docs`
- **Branded JSON Viewer** — Visit any API endpoint in a browser for a pretty-printed response
- **No API Key Required** — Powered by free APIs from [apis.xcasper.space](https://apis.xcasper.space)
- **Professional Dark UI** — Glassmorphism navbar, gradient accents, responsive layout

---

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Run Locally

```bash
git clone https://github.com/xcasper/ai-imager.git
cd ai-imager
pip install -r requirements.txt
python run.py
```

Open your browser at **http://localhost:5000**.

---

## Deployment

### Render *(Recommended — Free Tier)*

1. Fork this repo to your GitHub account.
2. [Create a new Web Service on Render](https://dashboard.render.com/select-repo) and connect your fork.
3. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run.py`
   - **Environment:** Python 3
4. Click **Deploy** — Render auto-deploys on every push.

---

### Heroku

```bash
# Login and create app
heroku login
heroku create your-app-name

# Add Procfile
echo "web: python run.py" > Procfile
git add Procfile && git commit -m "chore: add Procfile"

# Deploy
git push heroku main
```

The `run.py` already reads `PORT` from the environment, so no changes are needed.

---

### Vercel

Create a `vercel.json` at the project root:

```json
{
  "builds": [{ "src": "run.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "run.py" }]
}
```

Then deploy:

```bash
npm i -g vercel
vercel --prod
```

> **Note:** Vercel's Python runtime is serverless. For file uploads and persistent sessions, use Render or Koyeb.

---

### Koyeb *(Free Tier — No Cold Starts)*

1. Go to [app.koyeb.com](https://app.koyeb.com) → **Create App** → **GitHub**.
2. Connect your fork.
3. Set:
   - **Build command:** `pip install -r requirements.txt`
   - **Run command:** `python run.py`
   - **Port:** `5000`
4. Click **Deploy**.

---

### Railway

1. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub Repo**.
2. Select your fork — Railway auto-detects Python.
3. Add environment variable `PORT=5000` if required.
4. Click **Deploy**.

---

### VPS (Ubuntu / Debian)

```bash
# Install dependencies
sudo apt update && sudo apt install python3 python3-pip git nginx -y

# Clone and install
git clone https://github.com/xcasper/ai-imager.git
cd ai-imager
pip3 install -r requirements.txt gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

**Nginx reverse proxy** (`/etc/nginx/sites-available/ai-imager`):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/ai-imager /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# HTTPS via Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

**Systemd service** (`/etc/systemd/system/ai-imager.service`):

```ini
[Unit]
Description=AI Imager
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-imager
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ai-imager
```

---

## API Reference

Visit `/docs` in the browser for the full interactive API reference.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/image/prompt/generate` | Text to image |
| `POST` | `/v1/image/bing/generate` | Magic Studio |
| `POST` | `/v1/image/mask/generate` | Image + mask edit |
| `POST` | `/v1/image/variation/generate` | Image variation |
| `GET`  | `/v1/history` | Session history |

All endpoints accept `multipart/form-data` and return JSON. No authentication required.

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.
For security issues, see [SECURITY.md](SECURITY.md).

---

## Legal

- [Terms of Service](/terms)
- [Privacy Policy](/privacy)
- [Disclaimer](/disclaimer)

---

## License

[GNU General Public License v3.0](LICENSE) — Free to use, modify, and distribute.

---

## Acknowledgements

- [Casper Technology](https://xcasper.space) — Free AI APIs via [apis.xcasper.space](https://apis.xcasper.space)
- [LawrenceKimutai](https://github.com/LawrenceKimutai) — Early contributions
- [Simatwa](https://github.com/Simatwa) — Original project foundation

---

<p align="center">
  <a href="https://xcasper.space">xcasper.space</a> · <a href="https://apis.xcasper.space">Free AI APIs</a> · <a href="https://github.com/xcasper/ai-imager">GitHub</a>
</p>
