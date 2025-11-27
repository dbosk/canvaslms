"""
Tests for canvaslms.cli.utils time formatting functions.

These tests demonstrate expected behavior using variation theory:
we vary inputs (None, different formats, timezones) while the
conversion logic stays constant.
"""
import pytest
from datetime import datetime, timezone
from freezegun import freeze_time
import arrow

from canvaslms.cli.utils import (
    format_local_time,
    format_canvas_time,
    parse_date
)

class TestFormatLocalTime:
    """Test format_local_time() with various inputs"""

    def test_none_returns_na(self):
        """None input should return 'N/A' for display"""
        assert format_local_time(None) == "N/A"

    def test_empty_string_returns_na(self):
        """Empty string should return 'N/A'"""
        assert format_local_time("") == "N/A"

    @freeze_time("2023-12-15 14:30:00")
    def test_formats_utc_to_local(self):
        """
        Should convert UTC timestamp to local time.

        Frozen at 2023-12-15 14:30 CET (UTC+1, Europe/Stockholm winter time).
        Input: 2023-12-15 13:30:00 UTC
        Expected output in local time (CET): 2023-12-15 14:30
        """
        utc_time = "2023-12-15T13:30:00Z"
        result = format_local_time(utc_time)
        assert result == "2023-12-15 14:30"

    def test_invalid_format_returns_original(self):
        """If parsing fails, return the original string"""
        invalid = "not-a-timestamp"
        result = format_local_time(invalid)
        assert result == invalid
class TestFormatCanvasTime:
    """Test format_canvas_time() with various input types"""

    def test_none_returns_none(self):
        """None input should return None"""
        assert format_canvas_time(None) == None

    def test_empty_string_returns_none(self):
        """Empty string should return None"""
        assert format_canvas_time("") == None

    @freeze_time("2023-12-15 10:00:00")
    def test_datetime_with_timezone(self):
        """
        Should convert timezone-aware datetime to Canvas UTC format.

        Input: datetime with timezone
        Output: UTC ISO string ending with 'Z'
        """
        dt = datetime(2023, 12, 15, 10, 0, 0, tzinfo=timezone.utc)
        result = format_canvas_time(dt)
        assert result.endswith("Z")
        assert "2023-12-15" in result

    @freeze_time("2023-12-15 10:00:00")
    def test_datetime_without_timezone_assumes_local(self):
        """
        Naive datetime (no timezone) should be interpreted as local time.

        Frozen at 2023-12-15 10:00 CET (UTC+1, Europe/Stockholm winter time).
        Input: naive datetime 2023-12-15 10:00
        Output: Should interpret as local (CET) and convert to UTC
        """
        dt = datetime(2023, 12, 15, 10, 0, 0)
        result = format_canvas_time(dt)
        # Should be converted from CET to UTC (subtract 1 hour)
        assert result.endswith("Z")
        assert "2023-12-15T09:00:00Z" == result

    @freeze_time("2023-12-15 10:00:00")
    def test_date_object_start_of_day(self):
        """
        Date (not datetime) should be interpreted as start of day in local time.

        Frozen at 2023-12-15 10:00 CET (UTC+1, Europe/Stockholm winter time).
        Input: date(2023, 12, 15)
        Output: 2023-12-15 00:00 local → converted to UTC
        """
        from datetime import date
        d = date(2023, 12, 15)
        result = format_canvas_time(d)
        assert result.endswith("Z")
        # Start of day in CET (00:00) = 23:00 UTC previous day
        assert "2023-12-14T23:00:00Z" == result

    def test_arrow_object(self):
        """Arrow objects should be converted to Canvas format"""
        arr = arrow.get("2023-12-15T10:00:00Z")
        result = format_canvas_time(arr)
        assert result == "2023-12-15T10:00:00Z"

    @freeze_time("2023-12-15 10:00:00")
    def test_string_iso_format(self):
        """ISO string should be parsed as local time and converted to UTC"""
        iso_str = "2023-12-15T10:00:00"
        result = format_canvas_time(iso_str)
        assert result.endswith("Z")
        # 10:00 local (CET) = 09:00 UTC
        assert "2023-12-15T09:00:00Z" == result

    def test_invalid_string_raises_error(self):
        """Invalid date string should raise ValueError"""
        with pytest.raises(ValueError, match="Invalid date/time format"):
            format_canvas_time("not a date")
class TestParseDate:
    """Test parse_date() with various date formats"""

    def test_none_returns_none(self):
        """None should return None"""
        assert parse_date(None) == None

    def test_none_string_returns_none(self):
        """String 'none' should return None"""
        assert parse_date("none") == None
        assert parse_date("None") == None

    def test_clear_returns_none(self):
        """String 'clear' should return None (for clearing dates)"""
        assert parse_date("clear") == None

    def test_empty_string_returns_none(self):
        """Empty string should return None"""
        assert parse_date("") == None

    @freeze_time("2023-12-15 10:00:00")
    def test_iso_format(self):
        """ISO format: YYYY-MM-DD"""
        result = parse_date("2023-12-15")
        assert result.endswith("Z")
        # Date interpreted as start of day local time (00:00 CET)
        # 2023-12-15 00:00 CET (UTC+1) = 2023-12-14 23:00 UTC
        assert "2023-12-14T23:00:00Z" == result

    @freeze_time("2023-12-15 10:00:00")
    def test_iso_with_time(self):
        """ISO format with time: YYYY-MM-DD HH:mm"""
        result = parse_date("2023-12-15 14:30")
        assert result.endswith("Z")
        # parse_date interprets naive strings as local time (CET)
        # 14:30 CET (UTC+1) = 13:30 UTC
        assert "2023-12-15T13:30:00Z" == result

    @freeze_time("2023-12-15 10:00:00")
    def test_explicit_timezone_preserved(self):
        """Explicit timezone info should be preserved, not reinterpreted"""
        # UTC explicit
        result = parse_date("2023-12-15T14:30:00Z")
        assert result == "2023-12-15T14:30:00Z"

        # Positive offset
        result = parse_date("2023-12-15T14:30:00+02:00")
        assert result == "2023-12-15T12:30:00Z"  # 14:30+02:00 = 12:30 UTC

        # Negative offset
        result = parse_date("2023-12-15T14:30:00-05:00")
        assert result == "2023-12-15T19:30:00Z"  # 14:30-05:00 = 19:30 UTC

    @freeze_time("2023-12-15 10:00:00")
    def test_slash_format(self):
        """US format: MM/DD/YYYY"""
        result = parse_date("12/15/2023")
        assert result.endswith("Z")
        # Date interpreted as start of day local time (00:00 CET)
        # 2023-12-15 00:00 CET (UTC+1) = 2023-12-14 23:00 UTC
        assert "2023-12-14T23:00:00Z" == result

    @freeze_time("2023-12-15 10:00:00")
    def test_month_name_format(self):
        """Month name format: Dec 15 2023"""
        result = parse_date("Dec 15 2023")
        assert result.endswith("Z")
        # Date interpreted as start of day local time (00:00 CET)
        # 2023-12-15 00:00 CET (UTC+1) = 2023-12-14 23:00 UTC
        assert "2023-12-14T23:00:00Z" == result

    def test_invalid_format_raises_error(self):
        """Completely invalid string should raise ValueError"""
        with pytest.raises(ValueError, match="Could not parse date"):
            parse_date("not-a-valid-date-xyz123")
