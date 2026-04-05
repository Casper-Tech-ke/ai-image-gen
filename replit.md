# AI Imager

## Overview
A Flask-based web application for generating and manipulating images using free AI APIs from apis.xcasper.space (Casper Technology). No API key required.

## Features
- Text to Image generation (DeepAI engine)
- Magic Studio image generation (Casper Tech APIs, DeepAI fallback)
- Image + Mask editing
- Image Variations
- Image to Prompt (analyse uploaded image → extract colours/brightness/composition via PIL → generate creative AI prompt via Casper Gemini)
- Session-based generation history
- Interactive API documentation at `/docs`
- Branded JSON viewer for browser API access
- Professional dark-themed UI with gradient accents
- Legal pages: Terms, Privacy, Disclaimer

## Architecture
- **Backend**: Python 3.8+ + Flask 3.x
- **AI APIs**: Free APIs from apis.xcasper.space — `/api/ai/deepai` (text-to-image), `/api/ai/magicstudio` (Magic Studio)
- **No API key required** — all AI calls go through Casper Tech's free endpoints
- **Templates**: Jinja2 HTML in `contents/templates/`
- **Static Assets**: CSS, JS, images in `contents/static/`
- **Sessions**: Cookie-based (`id` cookie, 72hr TTL), history stored in `contents/configs/`

## Project Structure
```
ai_imager/
  __init__.py          - Package init, error handlers
  web_interface.py     - Flask routes (all pages + API endpoints)
  imager.py            - AI API integration (Casper Tech / DeepAI)
  common.py            - History, session utilities
contents/
  templates/
    base.html          - Base layout (nav, professional footer)
    index.html         - Landing page (hero + tool cards)
    form.html          - Image generation form
    docs.html          - Interactive API reference
    json_pretty.html   - Branded JSON response viewer
    legal/
      terms.html       - Terms of Service
      privacy.html     - Privacy Policy
      disclaimer.html  - Disclaimer
  static/
    css/style.css      - All styles (dark theme, footer, legal, docs, JSON viewer)
    javascript/        - Frontend JS (form submit, tab switcher, JSON colorizer)
    image/             - Favicon, static images
run.py                 - Entry point (Replit, port 5000, host 0.0.0.0)
requirements.txt       - Python dependencies
README.md              - Full documentation with deployment guides
CONTRIBUTING.md        - Contribution guide
SECURITY.md            - Security policy and vulnerability reporting
LICENSE                - GNU GPL v3.0
```

## Routes
| Path | Description |
|------|-------------|
| `/` | Landing page |
| `/v1/image/<action>` | Image generation form (prompt, bing, mask, variation) |
| `/v1/image/prompt/generate` | POST — Text to image |
| `/v1/image/bing/generate` | POST — Magic Studio |
| `/v1/image/mask/generate` | POST — Image + mask |
| `/v1/image/variation/generate` | POST — Image variation |
| `/v1/image/analyze` | GET — Image-to-Prompt form |
| `/v1/image/analyze/generate` | POST — Analyse image, return JSON `{prompt, palette, error}` |
| `/v1/history` | GET — Session history (browser: branded JSON viewer) |
| `/docs` | API reference page |
| `/terms` | Terms of Service |
| `/privacy` | Privacy Policy |
| `/disclaimer` | Disclaimer |

## Running
```bash
python run.py
```
App starts at http://localhost:5000

## No API Key Needed
The `openai` package (0.27.4) is installed only for its exception types. All actual image generation uses free Casper Tech APIs — no `OPENAI_API_KEY` required.

## Social / Branding Links
- Homepage: https://xcasper.space
- APIs: https://apis.xcasper.space
- GitHub: https://github.com/xcasper/ai-imager

> Update GitHub URLs in base.html, README.md, CONTRIBUTING.md, and legal pages if your actual GitHub username differs from `xcasper`.
