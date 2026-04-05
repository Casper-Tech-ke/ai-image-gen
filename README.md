<h1 align="center">AI Image Gen</h1>

<p align="center">
  <img width="80" height="80" src="https://github.com/Casper-Tech-ke/ai-image-gen/raw/main/contents/static/image/favicon.svg" alt="AI Image Gen Logo"/>
  <br><br>
  <a href="https://github.com/Casper-Tech-ke/ai-image-gen"><img src="https://img.shields.io/badge/GitHub-ai--image--gen-181717?logo=github&style=flat-square" alt="GitHub"/></a>
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

## Screenshots

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/Casper-Tech-ke/ai-image-gen/raw/main/assets/screenshots/homepage.jpg" alt="Homepage" width="420"/>
      <br/><sub><b>Homepage — Tool Gallery</b></sub>
    </td>
    <td align="center">
      <img src="https://github.com/Casper-Tech-ke/ai-image-gen/raw/main/assets/screenshots/text_to_image.jpg" alt="Text to Image" width="420"/>
      <br/><sub><b>Text to Image</b></sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://github.com/Casper-Tech-ke/ai-image-gen/raw/main/assets/screenshots/image_to_prompt.jpg" alt="Image to Prompt" width="420"/>
      <br/><sub><b>Image to Prompt</b></sub>
    </td>
    <td align="center">
      <img src="https://github.com/Casper-Tech-ke/ai-image-gen/raw/main/assets/screenshots/api_docs.jpg" alt="API Docs" width="420"/>
      <br/><sub><b>Interactive API Docs</b></sub>
    </td>
  </tr>
</table>

---

## Features

- **Text to Image** — Generate images from any text prompt using the DeepAI engine
- **Magic Studio** — High-quality image generation via Casper Tech APIs
- **Image + Mask** — Edit specific regions of an image using a text prompt and mask
- **Image Variations** — Generate creative variations from a reference image
- **Image to Prompt** — Upload any image; AI extracts its colours, lighting & composition to craft a generation prompt
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
git clone https://github.com/Casper-Tech-ke/ai-image-gen.git
cd ai-image-gen
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
2. Select your repo — Railway auto-detects Python.
3. Add environment variable `PORT=5000` if required.
4. Click **Deploy**.

---

### VPS (Ubuntu / Debian)

```bash
# Install dependencies
sudo apt update && sudo apt install python3 python3-pip git nginx -y

# Clone and install
git clone https://github.com/Casper-Tech-ke/ai-image-gen.git
cd ai-image-gen
pip3 install -r requirements.txt gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

**Nginx reverse proxy** (`/etc/nginx/sites-available/ai-image-gen`):

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
sudo ln -s /etc/nginx/sites-available/ai-image-gen /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# HTTPS via Let's Encrypt
sudo certbot --nginx -d your-domain.com
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
| `GET`  | `/v1/image/analyze` | Image-to-Prompt form |
| `POST` | `/v1/image/analyze/generate` | Analyse image → returns `{prompt, palette}` |
| `GET`  | `/v1/history` | Session history |

All endpoints accept `multipart/form-data` and return JSON. No authentication required.

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.
For security issues, see [SECURITY.md](SECURITY.md).

---

## License

[GNU General Public License v3.0](LICENSE) — Free to use, modify, and distribute.

---

## Acknowledgements

- [Casper Technology](https://xcasper.space) — Free AI APIs via [apis.xcasper.space](https://apis.xcasper.space)

---

<p align="center">
  <a href="https://xcasper.space">xcasper.space</a> · <a href="https://apis.xcasper.space">Free AI APIs</a> · <a href="https://github.com/Casper-Tech-ke/ai-image-gen">GitHub</a>
</p>
