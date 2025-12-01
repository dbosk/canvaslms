"""
Tests for canvaslms.cli.courses filtering and selection functions.

These tests verify the core course filtering logic used throughout
the canvaslms tool. The add_course_option/process_course_option
pattern is fundamental to many commands.
"""
import pytest
import re
from unittest.mock import MagicMock

from canvaslms.cli import EmptyListError
from canvaslms.cli.courses import (
    filter_courses,
    process_course_option
)

class TestFilterCourses:
    """Test filter_courses() with various regex patterns"""

    def test_matches_course_name(self, mock_canvas, mock_courses):
        """Should match courses by name"""
        mock_canvas.get_courses.return_value = mock_courses

        # Regex that matches "Programming" in course name
        result = list(filter_courses(mock_canvas, "Programming"))

        assert len(result) == 1
        assert result[0].name == "Introduction to Programming"

    def test_matches_course_code(self, mock_canvas, mock_courses):
        """Should match courses by course code"""
        mock_canvas.get_courses.return_value = mock_courses

        # Regex that matches "CS101" in course code
        result = list(filter_courses(mock_canvas, "CS101"))

        assert len(result) == 1
        assert result[0].course_code == "CS101"

    def test_matches_course_id(self, mock_canvas, mock_courses):
        """Should match courses by Canvas ID"""
        mock_canvas.get_courses.return_value = mock_courses

        # Regex that matches ID 1002
        result = list(filter_courses(mock_canvas, "1002"))

        assert len(result) == 1
        assert result[0].id == 1002

    def test_matches_multiple_courses(self, mock_canvas, mock_courses):
        """Should return multiple matches when regex matches multiple courses"""
        mock_canvas.get_courses.return_value = mock_courses

        # Regex that matches "CS" in course codes
        result = list(filter_courses(mock_canvas, "CS"))

        # Should match CS101, CS201, CS102
        assert len(result) == 3

    def test_match_all_pattern(self, mock_canvas, mock_courses):
        """Regex '.*' should match all courses"""
        mock_canvas.get_courses.return_value = mock_courses

        result = list(filter_courses(mock_canvas, ".*"))

        assert len(result) == 3

    def test_no_matches_empty_list(self, mock_canvas, mock_courses):
        """Should return empty list when no courses match"""
        mock_canvas.get_courses.return_value = mock_courses

        result = list(filter_courses(mock_canvas, "NoMatchingCourse"))

        assert len(result) == 0

    def test_case_sensitive_matching(self, mock_canvas, mock_courses):
        """Regex matching is case-sensitive by default"""
        mock_canvas.get_courses.return_value = mock_courses

        # Lowercase "programming" should not match "Programming"
        result = list(filter_courses(mock_canvas, "programming"))

        assert len(result) == 0

        # Uppercase should match
        result = list(filter_courses(mock_canvas, "Programming"))
        assert len(result) == 1

    def test_special_regex_characters(self, mock_canvas):
        """Should handle special regex characters properly"""
        # Create course with special characters in name
        course = MagicMock()
        course.id = 9999
        course.name = "C++ Programming (Advanced)"
        course.course_code = "CS301"
        mock_canvas.get_courses.return_value = [course]

        # Parentheses need escaping in regex
        result = list(filter_courses(mock_canvas, r"C\+\+"))

        assert len(result) == 1
        assert result[0].name == "C++ Programming (Advanced)"
class TestProcessCourseOption:
    """Test process_course_option() error handling and integration"""

    def test_returns_matching_courses(self, mock_canvas, mock_courses):
        """Should return list of matching courses"""
        mock_canvas.get_courses.return_value = mock_courses

        args = MagicMock()
        args.course = "CS"

        result = process_course_option(mock_canvas, args)

        assert len(result) == 3
        assert all(course.course_code.startswith("CS") for course in result)

    def test_raises_empty_list_error_no_matches(self, mock_canvas, mock_courses):
        """Should raise EmptyListError when no courses match"""
        mock_canvas.get_courses.return_value = mock_courses

        args = MagicMock()
        args.course = "NoSuchCourse"

        with pytest.raises(EmptyListError, match="No courses found"):
            process_course_option(mock_canvas, args)

    def test_default_regex_matches_all(self, mock_canvas, mock_courses):
        """Default regex '.*' should match all courses"""
        mock_canvas.get_courses.return_value = mock_courses

        args = MagicMock()
        args.course = ".*"

        result = process_course_option(mock_canvas, args)

        assert len(result) == 3

    def test_single_course_match(self, mock_canvas, mock_courses):
        """Should handle single course match correctly"""
        mock_canvas.get_courses.return_value = mock_courses

        args = MagicMock()
        args.course = "^Introduction"  # Anchor to match only one

        result = process_course_option(mock_canvas, args)

        assert len(result) == 1
        assert result[0].name == "Introduction to Programming"

    def test_empty_canvas_courses_raises_error(self, mock_canvas):
        """Should raise EmptyListError when Canvas returns no courses"""
        mock_canvas.get_courses.return_value = []

        args = MagicMock()
        args.course = ".*"

        with pytest.raises(EmptyListError):
            process_course_option(mock_canvas, args)
