import re
import os
from functools import wraps
from flask import abort
from flask_login import current_user


def sanitize_name(name):
    # Remove invalid characters, replace underscores with spaces
    return re.sub(r'[^\w\-_\. ]', '', name).replace('_', ' ').strip()

def rename_episode(filename, series_folder_name, season_folder_name=None):
    # Extract episode number only (e.g., E01)
    ep_match = re.search(r'[eE](\d{2})', filename)
    season_code = None

    # Extract season from folder name, e.g. "Season 01" or "Season01"
    if season_folder_name:
        m = re.match(r'Season\s*(\d{1,2})', season_folder_name, re.IGNORECASE)
        if m:
            season_code = f"S{int(m.group(1)):02d}"

    ext = os.path.splitext(filename)[1]
    base_name = os.path.splitext(filename)[0]

    # Check for full season-episode code, e.g. S01E01
    full_match = re.search(r'([sS]\d{2}[eE]\d{2})', filename)

    if full_match:
        se_str = full_match.group(1).upper()
        # Take everything after the season-episode code for additional title info
        post_str = filename[full_match.end():].strip(' -_')
        # Strip the file extension from post_str before sanitizing
        if post_str.lower().endswith(ext.lower()):
            post_str = post_str[:-len(ext)]
        post_str_clean = sanitize_name(post_str.strip())

        if post_str_clean:
            return f"{sanitize_name(series_folder_name)} {se_str} {post_str_clean}{ext}"
        else:
            return f"{sanitize_name(series_folder_name)} {se_str}{ext}"

    elif season_code and ep_match:
        # Compose full season-episode code from season folder + episode from filename
        se_str = f"{season_code}E{ep_match.group(1)}"
        # Remove the episode code from base_name if present to avoid duplication
        title_part = re.sub(r'^[eE]\d{2}', '', base_name).strip(' -_')
        title_clean = sanitize_name(title_part)

        if title_clean:
            return f"{sanitize_name(series_folder_name)} {se_str} {title_clean}{ext}"
        else:
            return f"{sanitize_name(series_folder_name)} {se_str}{ext}"

    else:
        # No recognizable season or episode code, just prepend series folder name sanitized
        clean_base = sanitize_name(base_name)
        return f"{sanitize_name(series_folder_name)} {clean_base}{ext}"

def normalize_season_folder(name):
    # Versuche, "season X" zu matchen
    m = re.match(r'season\s*(\d+)', name, re.IGNORECASE)
    if m:
        season_num = int(m.group(1))
        return f"Season {season_num:02d}"
    # Versuche, "SXX" zu matchen (z.B. S00, S01, etc.)
    m = re.match(r's(\d{1,2})', name, re.IGNORECASE)
    if m:
        season_num = int(m.group(1))
        return f"Season {season_num:02d}"
    # Falls nichts passt, Name sanitisieren (vorhandene Funktion)
    return sanitize_name(name)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated