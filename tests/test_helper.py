"""Unit tests for helper.py – no Flask context needed."""
import pytest
from helper import rename_episode, normalize_season_folder, sanitize_name


class TestSanitizeName:
    def test_removes_invalid_chars(self):
        # Invalid chars are removed (not replaced with spaces)
        assert sanitize_name('Hello/World!') == 'HelloWorld'

    def test_replaces_underscores_with_spaces(self):
        assert sanitize_name('breaking_bad') == 'breaking bad'

    def test_strips_whitespace(self):
        assert sanitize_name('  name  ') == 'name'

    def test_allows_hyphens_and_dots(self):
        result = sanitize_name('Show-Name 1.0')
        assert 'Show' in result and 'Name' in result


class TestNormalizeSeasonFolder:
    def test_season_word(self):
        assert normalize_season_folder('Season 1') == 'Season 01'

    def test_season_word_no_space(self):
        assert normalize_season_folder('Season1') == 'Season 01'

    def test_season_padded(self):
        assert normalize_season_folder('Season 3') == 'Season 03'

    def test_season_double_digit(self):
        assert normalize_season_folder('Season 12') == 'Season 12'

    def test_short_code_s01(self):
        assert normalize_season_folder('S01') == 'Season 01'

    def test_short_code_s1(self):
        assert normalize_season_folder('S1') == 'Season 01'

    def test_case_insensitive(self):
        assert normalize_season_folder('season 2') == 'Season 02'

    def test_unknown_format_sanitized(self):
        result = normalize_season_folder('Extras')
        assert isinstance(result, str)
        assert len(result) > 0


class TestRenameEpisode:
    def test_full_sxxexx_code_in_filename(self):
        result = rename_episode('S01E05.mkv', 'Breaking Bad', 'Season 01')
        assert result == 'Breaking Bad S01E05.mkv'

    def test_full_code_with_title(self):
        result = rename_episode('S02E03 - Pilot.mkv', 'Breaking Bad', 'Season 02')
        assert 'S02E03' in result
        assert 'Breaking Bad' in result

    def test_episode_only_uses_season_folder(self):
        result = rename_episode('E05.mkv', 'Breaking Bad', 'Season 01')
        assert 'S01E05' in result
        assert 'Breaking Bad' in result

    def test_no_episode_code_uses_filename(self):
        result = rename_episode('pilot.mkv', 'Breaking Bad', None)
        assert 'Breaking Bad' in result
        assert result.endswith('.mkv')

    def test_extension_preserved(self):
        result = rename_episode('S01E01.mp4', 'My Show', 'Season 01')
        assert result.endswith('.mp4')

    def test_underscore_in_series_name_replaced(self):
        result = rename_episode('S01E01.mkv', 'My_Show', 'Season 01')
        assert '_' not in result

    def test_uppercase_episode_code(self):
        result = rename_episode('s01e02.mkv', 'My Show', 'Season 01')
        assert 'S01E02' in result
