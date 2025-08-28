import mimetypes
import os
from user import user_db
from helper import rename_episode, normalize_season_folder, admin_required
from datetime import timedelta
from flask import Flask, request, redirect, render_template, session, g, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from user.models import db, User
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "08ba28b7f1e56669a92e1963aa2dfd87"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

PICTURE_TYPES = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'}
VIDEO_TYPES = {'.mp4', '.mov', '.mkv', '.avi', '.flv', '.wmv', '.webm', '.3gp', '.m4v'}

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/')

@app.before_request
def set_user_paths():
    if current_user.is_authenticated:
        if current_user.username == "Arnika":
            g.upload_folder = '/media/felix/server'
            g.pictures_folder = '/media/felix/server/Arnikas Photos'
            g.videos_folder = '/media/felix/server/Arnikas Videos'
            g.movie_folder = '/media/felix/server/Movies'
            g.series_folder = '/media/felix/server/Series'
            g.shared_pictures_folder = '/media/felix/server/Shared Photos'
            g.shared_videos_folder = '/media/felix/server/Shared Videos'
        else:
            g.upload_folder = '/media/felix/server'
            g.pictures_folder = '/media/felix/server/Photos'
            g.videos_folder = '/media/felix/server/Videos'
            g.movie_folder = '/media/felix/server/Movies'
            g.series_folder = '/media/felix/server/Series'
            g.shared_pictures_folder = '/media/felix/server/Shared Photos'
            g.shared_videos_folder = '/media/felix/server/Shared Videos'
    else:
        g.upload_folder = None
        g.pictures_folder = None
        g.videos_folder = None
        g.movie_folder = None
        g.series_folder = None


@login_manager.user_loader
def load_user(user_id):
    return user_db.get_user_by_id(user_id)

# landing page
@app.route('/')
def landing():
    return render_template('landing_page.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = user_db.get_user(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            session.permanent = True
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        # GET-Anfrage: Login-Seite anzeigen
        return render_template('login.html')


# return to Landing after Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# Upload of single picture
@app.route('/upload/photos', methods=['GET', 'POST'])
@login_required
def upload_picture():

    if request.method == 'POST':
        shared = request.form.get('shared') == 'on'
        base_folder = g.shared_pictures_folder if shared else g.pictures_folder

        files = request.files.getlist('picture')
        directory = request.form['directory']
        if directory == "__new__":
            new_dir_name = request.form.get('new_directory', '').strip()
            if not new_dir_name:
                return "Kein neuer Ordnername angegeben", 400
            directory = new_dir_name

        destination = os.path.join(base_folder, directory)
        os.makedirs(destination, exist_ok=True)

        for picture in files:
            destination_path = os.path.join(destination, picture.filename)
            picture.save(destination_path)
        return '', 200
    else:
        personal_dirs = [d for d in os.listdir(g.pictures_folder) if os.path.isdir(os.path.join(g.pictures_folder, d))]
        shared_dirs = [d for d in os.listdir(g.shared_pictures_folder) if os.path.isdir(os.path.join(g.shared_pictures_folder, d))]

        return render_template('picture_upload.html', personal_dirs=personal_dirs, shared_dirs=shared_dirs)


# Video upload
@app.route('/upload/video', methods=['GET', 'POST'])
@login_required
def upload_video():
    videos = g.videos_folder
    shared_videos_dir = g.shared_videos_folder
    if request.method == 'POST':
        files = request.files.getlist('video')
        directory = request.form['directory']
        shared = request.form.get('shared') == 'on'

        if directory == "__new__":
            new_dir_name = request.form.get('new_directory', '').strip()
            if not new_dir_name:
                return "Kein neuer Ordnername angegeben", 400
            directory = new_dir_name

        base_folder = shared_videos_dir if shared else videos
        destination = os.path.join(base_folder, directory)
        os.makedirs(destination, exist_ok=True)

        for video in files:
            destination_path = os.path.join(destination, video.filename)
            video.save(destination_path)
        return '', 200

    else:
        personal_dirs = [d for d in os.listdir(videos) if os.path.isdir(os.path.join(videos, d))]
        shared_dirs = [d for d in os.listdir(shared_videos_dir) if os.path.isdir(os.path.join(shared_videos_dir, d))]
        return render_template('video_uploads.html', personal_dirs=personal_dirs, shared_dirs=shared_dirs)

# Movie Uploads
@app.route('/upload/movie', methods=['GET', 'POST'])
@login_required
def upload_movie():
    movies = g.movie_folder
    if request.method == 'POST':
        movie = request.files['movie']
        directory = request.form['directory']
        new_dir_name = request.form.get('new_directory', '').strip()

        # Wenn ein neuer Ordnername angegeben wurde, nutze diesen als directory
        if new_dir_name:
            directory = new_dir_name

        # Erstelle kompletten Zielpfad
        destination = os.path.join(movies, directory)
        os.makedirs(destination, exist_ok=True)

        destination_path = os.path.join(destination, movie.filename)

        # Prüfe ob Datei bereits existiert
        if os.path.exists(destination_path):
            return 'OK: Datei existiert bereits', 200

        movie.save(destination_path)
        return '', 200

    else:
        dir_list = [d for d in os.listdir(movies) if os.path.isdir(os.path.join(movies, d))]
        return render_template('movie_upload.html', directories=dir_list)

# Series upload
@app.route('/upload/series', methods=['GET', 'POST'])
@login_required
def upload_series():
    skipped_files = []
    base_dir = g.series_folder
    os.makedirs(base_dir, exist_ok=True)

    if request.method == 'POST':
        files = request.files.getlist('file')
        if not files:
            return 'No files uploaded', 400

        # Nur der erste Ordner im relativen Pfad als Serienordnername
        first_file_path = files[0].filename.replace('\\', '/')
        series_folder_name = first_file_path.split('/')

        for file in files:
            rel_path = file.filename.replace('\\', '/')
            parts = rel_path.split('/')

            if len(parts) < 2:
                # Ungültiger Pfad, überspringen
                continue

            # Erster Teil ist Serienname (Ordner)
            series_folder_name = parts[0]

            if len(parts) == 2:
                # Staffel fehlt, Standard 'Season 01' verwenden
                season_folder_name = "Season 01"
                sub_path_parts = []
            else:
                # Staffelname aus zweitem Teil extrahieren und normalisieren
                season_folder_name = normalize_season_folder(parts[1])
                sub_path_parts = parts[2:-1]

            orig_filename = parts[-1]
            new_filename = rename_episode(orig_filename, series_folder_name, season_folder_name)

            target_dir = os.path.join(base_dir, series_folder_name, season_folder_name, *sub_path_parts)
            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, new_filename)

            if os.path.exists(target_path):
                skipped_files.append(new_filename)
                continue

            try:
                file.save(target_path)
                print(f"Saved file to: {target_path}")
            except Exception as e:
                print(f"Error saving file {target_path}: {e}")

        return '', 200

    else:
        dir_list = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
        return render_template('series_upload.html', directories=dir_list)


# Picture directory upload
@app.route('/upload/directory', methods=['GET', 'POST'])
@login_required
def upload_directory():
    pictures_dir = g.pictures_folder
    videos_dir = g.videos_folder
    shared_pictures_dir = g.shared_pictures_folder
    shared_videos_dir = g.shared_videos_folder

    if request.method == 'POST':
        files = request.files.getlist('file')
        shared = request.form.get('shared') == 'on'

        for file in files:

            # Keep relative path for subdirectory support
            filename = file.filename.replace('\\', '/')

            mime_type, _ = mimetypes.guess_type(filename)

            if mime_type is None:
                continue
            elif mime_type.startswith('image/'):
                base_folder = shared_pictures_dir if shared else pictures_dir
            elif mime_type.startswith('video/'):
                base_folder = shared_videos_dir if shared else videos_dir
            else:
                continue

            sub_path = filename
            target_dir = os.path.join(base_folder, os.path.dirname(sub_path))
            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, os.path.basename(filename))
            file.save(target_path)

        return '', 200
    else:
        return render_template('directory_upload.html')


@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = user_db.get_all_users()
    return render_template('admin_user_list.html', users=users)

@app.route('/admin/users/new', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_new_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin_checked = request.form.get('is_admin') == "1"

        if not username or not password:
            flash("Username or password is required")
            return redirect('/admin/new_user')

        password_hash = generate_password_hash(password)
        role = "admin" if is_admin_checked else "user"

        new_user = User(username=username, password=password_hash, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash(f" New user {username}, with role {role} has been created!")
        return redirect('/admin/users')
    return render_template('admin_new_user.html')

@app.route('/admin/users/delete/<userid>', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(userid):
    user_db.delete_user(userid)
    return redirect('/admin/users')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
