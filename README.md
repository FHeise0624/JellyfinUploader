# JellyfinUploader **v1.1.0**
[📥 Download latest](https://github.com/FHeise0624/JellyfinUploader/releases/latest)

**Flask media uploader** for **Jellyfin** with **smart series organization** (`S01E01` auto-naming), role-based folders, and a modern dark UI. Raspberry Pi optimised.

**Stack**: Flask 3.1.1 · SQLAlchemy 2.0 · Docker ready

---

## ✨ Features

- **Smart Series**: `Breaking Bad/E01.mkv` → `Breaking Bad S01E01.mkv`
- **Role-based folders**: per-user paths + shared folders
- **5 upload types**: Videos / Movies / Series / Directory / Photos (disabled by default)
- **Modern UI**: dark theme, Inter font, shared CSS via `static/style.css`
- **Docker**: `Dockerfile` + `docker-compose.yml` included
- **Feature flags**: enable/disable upload types without code changes
- **User management**: admin dashboard, role support (`admin` / `user` / `child`)
- **Secure auth**: Flask-Login + werkzeug password hashing

---

## 🚀 Quick Start

### Native

```bash
git clone https://github.com/FHeise0624/JellyfinUploader.git
cd JellyfinUploader
pip install -r requirements.txt
python create_admin.py   # run once
python app.py
```

Open `http://localhost:5005` and log in with the admin credentials.

### Docker

```bash
docker compose up -d
docker compose exec jellyfin-uploader python create_admin.py  # run once
```

The SQLite database is persisted via a volume mount at `./instance`.

---

## 🗂️ Upload Types

| Type | Endpoint | Notes |
|------|----------|-------|
| Videos | `/upload/video` | Personal or shared folder |
| Movies | `/upload/movie` | Skips duplicates |
| Series | `/upload/series` | Auto S01E01 + Season 01 naming |
| Directory | `/upload/directory` | Auto-sorted by media type |
| Photos | `/upload/photos` | **Disabled by default** (see Feature Flags) |

---

## 🚩 Feature Flags

Upload types can be toggled without touching routes or templates. Flags live at the top of `app.py`:

```python
app.config['PHOTOS_UPLOAD_ENABLED'] = False  # set True to re-enable
```

When disabled, the card is hidden from the dashboard and direct URL access redirects back.

---

## 👥 Role-Based Paths

```
Arnika (special):              Regular user:
├── Arnikas Photos/            ├── Photos/
├── Arnikas Videos/            ├── Videos/
├── Movies/                    ├── Movies/
├── Series/                    └── Series/
└── Shared Photos/             └── Shared Photos/
```

Paths are configured in `app.py` → `set_user_paths()`.

---

## 👑 Admin Panel (`/admin/users`)

- List, create, and delete users
- Assign roles: `admin`, `user`, `child`
- Passwords hashed with `werkzeug.security`

---

## 🎨 Frontend

All shared styles are in `static/style.css`. Templates use Jinja2 inheritance via `templates/base.html` — no duplicated CSS per page.

To customize the theme, edit the CSS variables at the top of `style.css`:

```css
:root {
  --accent: #7c5cfc;
  --bg: #0d0b1a;
  /* ... */
}
```

---

## 📦 Production

```bash
# Gunicorn (native)
pip install gunicorn
gunicorn -w 2 --bind 0.0.0.0:5005 app:app

# Docker (recommended)
docker compose up -d
```

---

## 📁 Structure

```
├── app.py                  # Flask app, routes, feature flags
├── helper.py               # Series renaming logic
├── create_admin.py         # One-time admin setup
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── static/
│   └── style.css           # Shared design system
├── templates/
│   ├── base.html           # Base layout (all pages extend this)
│   ├── dashboard.html
│   ├── login.html
│   ├── landing_page.html
│   ├── movie_upload.html
│   ├── series_upload.html
│   ├── video_uploads.html
│   ├── picture_upload.html
│   ├── directory_upload.html
│   ├── admin_user_list.html
│   └── admin_new_user.html
└── user/
    ├── models.py           # SQLAlchemy User model
    └── user_db.py          # CRUD helpers
```

---

## 🛣️ Roadmap

| Version | Feature | Status |
|---------|---------|--------|
| v1.0.0 | 5 upload types + series AI | ✅ |
| **v1.1.0** | Docker · modern UI · feature flags | ✅ |
| v1.2.0 | Jellyfin API integration | 🔄 Next |
| v2.0.0 | FastAPI async rewrite | 🏗️ Planned |

---

## 📄 License

[![License](https://img.shields.io/github/license/FHeise0624/JellyfinUploader)](LICENSE)  
**MIT License** — see [LICENSE](LICENSE) © Felix Heise
