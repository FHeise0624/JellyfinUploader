"""Integration tests for Flask routes."""
import pytest
from unittest.mock import patch


# ── Public routes ────────────────────────────────────────────────────────────

def test_landing_page(client):
    r = client.get('/')
    assert r.status_code == 200
    assert b'Jellyfin' in r.data


def test_login_page_get(client):
    r = client.get('/login')
    assert r.status_code == 200
    assert b'Sign in' in r.data or b'Login' in r.data


def test_login_valid_credentials(client):
    r = client.post('/login', data={'username': 'admin', 'password': 'adminpass'},
                    follow_redirects=True)
    assert r.status_code == 200
    assert b'Upload' in r.data  # dashboard


def test_login_invalid_credentials(client):
    r = client.post('/login', data={'username': 'admin', 'password': 'wrong'},
                    follow_redirects=True)
    assert r.status_code == 200
    assert b'Invalid' in r.data


def test_logout_redirects(admin_client):
    r = admin_client.get('/logout', follow_redirects=True)
    assert r.status_code == 200
    # Should land back on landing page
    assert b'Jellyfin' in r.data


# ── Auth protection ───────────────────────────────────────────────────────────

@pytest.mark.parametrize('url', [
    '/dashboard',
    '/upload/video',
    '/upload/movie',
    '/upload/series',
    '/upload/directory',
    '/upload/youtube',
])
def test_protected_routes_redirect_unauthenticated(client, url):
    r = client.get(url)
    assert r.status_code in (302, 308)
    assert '/' in r.headers.get('Location', '/')


# ── Dashboard ─────────────────────────────────────────────────────────────────

def test_dashboard_authenticated(admin_client):
    r = admin_client.get('/dashboard')
    assert r.status_code == 200
    assert b'Upload' in r.data


def test_dashboard_shows_admin_card_for_admin(admin_client, app):
    # Admin card is only shown when current_user.is_admin is truthy.
    # The template uses {% if current_user.is_authenticated and current_user.is_admin %}
    r = admin_client.get('/dashboard')
    assert r.status_code == 200


def test_dashboard_hides_photos_card_when_disabled(admin_client, app):
    app.config['PHOTOS_UPLOAD_ENABLED'] = False
    r = admin_client.get('/dashboard')
    assert r.status_code == 200
    assert b'/upload/photos' not in r.data


def test_dashboard_shows_photos_card_when_enabled(admin_client, app):
    app.config['PHOTOS_UPLOAD_ENABLED'] = True
    r = admin_client.get('/dashboard')
    assert r.status_code == 200
    assert b'/upload/photos' in r.data


# ── Feature flag: photos ──────────────────────────────────────────────────────

def test_photos_disabled_get_redirects(admin_client, app):
    app.config['PHOTOS_UPLOAD_ENABLED'] = False
    r = admin_client.get('/upload/photos')
    assert r.status_code in (302, 308)


def test_photos_disabled_post_redirects(admin_client, app):
    app.config['PHOTOS_UPLOAD_ENABLED'] = False
    r = admin_client.post('/upload/photos', data={})
    assert r.status_code in (302, 308)


def test_photos_enabled_get(admin_client, app):
    app.config['PHOTOS_UPLOAD_ENABLED'] = True
    with patch('os.listdir', return_value=[]):
        r = admin_client.get('/upload/photos')
    assert r.status_code == 200


# ── Upload route smoke tests ──────────────────────────────────────────────────

def test_movie_upload_get(admin_client):
    with patch('os.listdir', return_value=['TestMovie']):
        r = admin_client.get('/upload/movie')
    assert r.status_code == 200
    assert b'Movie' in r.data


def test_series_upload_get(admin_client):
    with patch('os.listdir', return_value=['Breaking Bad']):
        r = admin_client.get('/upload/series')
    assert r.status_code == 200
    assert b'Series' in r.data


def test_video_upload_get(admin_client):
    with patch('os.listdir', return_value=[]):
        r = admin_client.get('/upload/video')
    assert r.status_code == 200


def test_directory_upload_get(admin_client):
    r = admin_client.get('/upload/directory')
    assert r.status_code == 200


def test_youtube_upload_get(admin_client):
    with patch('os.makedirs', return_value=None):
        r = admin_client.get('/upload/youtube')
    assert r.status_code == 200
    assert b'YouTube' in r.data


# ── Admin routes ──────────────────────────────────────────────────────────────

def test_admin_users_accessible_by_admin(admin_client):
    r = admin_client.get('/admin/users')
    assert r.status_code == 200
    assert b'admin' in r.data


def test_admin_users_forbidden_for_regular_user(user_client):
    r = user_client.get('/admin/users')
    assert r.status_code == 403


def test_admin_new_user_get(admin_client):
    r = admin_client.get('/admin/users/new')
    assert r.status_code == 200


def test_admin_create_user(admin_client):
    r = admin_client.post('/admin/users/new',
                          data={'username': 'newuser', 'password': 'pass123'},
                          follow_redirects=True)
    assert r.status_code == 200
    assert b'newuser' in r.data
