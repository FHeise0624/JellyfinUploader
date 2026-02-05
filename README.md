# JellyfinUploader **v1.0.0 Pre-release** 
[📥 Download v1.0.0](https://github.com/FHeise0624/JellyfinUploader/releases/latest)


**Flask media uploader** for **Jellyfin** with **AI-powered series organization** (`S01E01` auto-naming) + **role-based folders**. **Production-ready** Flask app.

**Current status**: Flask 3.1.1 + SQLAlchemy 2.0. **Raspberry Pi optimised**.

**🚨 PRE-RELEASE**: `python create_admin.py` → `http://localhost:5005`

## ✨ Features
- **🤖 Smart Series**: `Breaking Bad/E01.mkv` → `Breaking Bad S01E01.mkv`
- **📁 Role Folders**: User vs OtherUser (`Photos` vs `Other Users Photos`)
- **5 Upload Types**: Photos/Videos/**Movies/Series/Directory**
- **🔐 User Management**: Admin dashboard + `werkzeug` hashing
- **Production SQLite**: Auto `instance/users.db`
- **Secure Auth**: Flask-Login + session management

## 🚀 Quick Start (3 Commands)

### **Install & Run**
```
git clone https://github.com/FHeise0624/JellyfinUploader.git
cd JellyfinUploader
pip install -r requirements.txt
```

### 🚨 Create Admin (Run ONCE)

```
python create_admin.py
# Creates: admin / secure_hash / admin role
```

### Start Server
```
python app.py
```

**Login**: `http://localhost:5005` → `admin` / `your_password`

## 🗂️ Smart Upload Types

| Type | Endpoint | Auto Magic |
|------|----------|------------|
| Photos | `/upload/photos` | Personal/Shared folders |
| Videos | `/upload/video` | Personal/Shared |
| Movies | `/upload/movie` | Skip duplicates |
| Series | `/upload/series` | **S01E01 + Season 01** |
| Directory | `/upload/directory` | Full folder structure |


## 👥 Role-Based Paths (app.py)
```
Other User (special):           Regular User:
├── Other User Photos/         ├── Photos/
├── Other User Videos/         ├── Videos/
├── Movies/                    ├── Movies/
├── Series/                    └── Series/
└── Shared Photos/             └── Shared Photos/
```

## 👑 Admin Panel (/admin/users)
```
✅ List users: user_db.get_all_users()
✅ Create: new_user(username, hash, role) 
✅ Delete: delete_user(userid)
✅ Secure: werkzeug.security hash
```

## 📦 Production Stack (requirements.txt)
```
Flask==3.1.1          # Latest Flask
Flask-Login==0.6.3    # Secure auth
Flask-SQLAlchemy==3.1.1 # ORM
SQLAlchemy==2.0.43    # Latest DB
Werkzeug==3.1.3       # Security

```

## 🚀 Raspberry Pi Production
```
pip install gunicorn
gunicorn -w 2 --bind 0.0.0.0:5005 app:app
```

## Customize paths (app.py ~line 70):
```
g.upload_folder = '/YOUR_MEDIA/server'
```

## 🛣️ Roadmap

| Version | Feature | Status |
|---------|---------|--------|
| **v1.0.0** | 5 Uploads + series AI | ✅ [Download](https://github.com/FHeise0624/JellyfinUploader/releases/tag/v1.0.0) |
| v1.1.0 | Jellyfin API | 🔄 Next |
| v2.0.0 | FastAPI async | 🏗️ Planned |

## 🛠️ Tech Highlights

```
🤖 helper.py: rename_episode(), normalize_season_folder()
🔐 user_db.py: Secure CRUD + werkzeug hash
⚙️ app.py: Flask port 5005 + role paths
🗄️ models.py: SQLAlchemy User (admin/user/child)
🔧 create_admin.py: Idempotent admin setup

```

## 📁 Structure
```
├── app.py # Flask main (5005)
├── helper.py # 🤖 Series AI
├── user_db
```

## 📄 License

[![License](https://img.shields.io/github/license/FHeise0624/JellyfinUploader)](LICENSE)  
**MIT License** - see [LICENSE](LICENSE) © Felix Heise
