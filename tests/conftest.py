"""
Shared pytest fixtures for testing canvaslms.

This file provides mock Canvas API objects that tests can use
instead of making real API calls. Each fixture returns a MagicMock
configured to behave like the corresponding Canvas API object.
"""
import pytest
from unittest.mock import MagicMock, Mock
from datetime import datetime, timezone
import arrow

@pytest.fixture
def mock_canvas():
    """
    Mock Canvas API instance.

    Provides get_courses() method that returns a list of mock courses.
    Tests can customize the return value to simulate different scenarios.
    """
    canvas = MagicMock()
    canvas.get_courses.return_value = []
    return canvas
@pytest.fixture
def mock_course():
    """
    Mock Canvas Course object with realistic attributes.

    Attributes:
        id: Course ID (12345)
        name: Course name ("Test Course")
        course_code: Short code ("TEST101")
        term: Dict with term info

    Methods:
        get_assignments(): Returns empty list (override in tests)
        get_users(): Returns empty list (override in tests)
    """
    course = MagicMock()
    course.id = 12345
    course.name = "Test Course"
    course.course_code = "TEST101"
    course.term = {"name": "Fall 2023"}

    # Mock methods that return lists
    course.get_assignments.return_value = []
    course.get_users.return_value = []

    return course


@pytest.fixture
def mock_courses():
    """
    Returns a list of three mock courses with different names.

    Useful for testing filtering and selection logic.
    Uses variation theory: three courses with same structure,
    different data (names, codes, IDs).
    """
    course1 = MagicMock()
    course1.id = 1001
    course1.name = "Introduction to Programming"
    course1.course_code = "CS101"
    course1.term = {"name": "Fall 2023"}
    course1.get_assignments.return_value = []
    course1.get_users.return_value = []

    course2 = MagicMock()
    course2.id = 1002
    course2.name = "Advanced Algorithms"
    course2.course_code = "CS201"
    course2.term = {"name": "Fall 2023"}
    course2.get_assignments.return_value = []
    course2.get_users.return_value = []

    course3 = MagicMock()
    course3.id = 1003
    course3.name = "Data Structures"
    course3.course_code = "CS102"
    course3.term = {"name": "Spring 2024"}
    course3.get_assignments.return_value = []
    course3.get_users.return_value = []

    return [course1, course2, course3]
@pytest.fixture
def mock_assignment():
    """
    Mock Canvas Assignment object.

    Attributes:
        id: Assignment ID
        name: Assignment name
        due_at: ISO 8601 due date string (or None)
        points_possible: Maximum points
        published: Whether assignment is published
        assignment_group_id: ID of assignment group
        submission_types: List of allowed submission types

    Methods:
        get_submissions(): Returns empty list (override in tests)
    """
    assignment = MagicMock()
    assignment.id = 5001
    assignment.name = "Homework 1"
    assignment.due_at = "2023-12-15T23:59:00Z"
    assignment.points_possible = 100.0
    assignment.published = True
    assignment.assignment_group_id = 2001
    assignment.submission_types = ["online_text_entry", "online_upload"]
    assignment.get_submissions.return_value = []

    return assignment


@pytest.fixture
def mock_assignment_group():
    """
    Mock Canvas AssignmentGroup object.

    Assignment groups categorize assignments (e.g., "Homeworks", "Exams").

    Attributes:
        id: Group ID
        name: Group name
        position: Sort order
        group_weight: Percentage of final grade
    """
    group = MagicMock()
    group.id = 2001
    group.name = "Homeworks"
    group.position = 1
    group.group_weight = 40.0

    return group
@pytest.fixture
def mock_user():
    """
    Mock Canvas User object.

    Attributes:
        id: User ID
        name: Full name
        sortable_name: "Last, First" format
        login_id: Username
        email: Email address (may be None due to privacy settings)
    """
    user = MagicMock()
    user.id = 3001
    user.name = "Alice Anderson"
    user.sortable_name = "Anderson, Alice"
    user.login_id = "alice"
    user.email = "alice@example.edu"

    return user


@pytest.fixture
def mock_group():
    """
    Mock Canvas Group object.

    Groups are collections of users for collaborative assignments.

    Attributes:
        id: Group ID
        name: Group name
        members_count: Number of members

    Methods:
        get_users(): Returns list of mock users
    """
    group = MagicMock()
    group.id = 4001
    group.name = "Project Team Alpha"
    group.members_count = 3
    group.get_users.return_value = []

    return group
@pytest.fixture
def mock_submission():
    """
    Mock Canvas Submission object.

    Submissions represent student work. They have states (submitted, graded,
    unsubmitted) and may include scores, comments, and timestamps.

    Attributes:
        id: Submission ID
        user_id: ID of student who submitted
        assignment_id: ID of assignment
        workflow_state: State (submitted, graded, unsubmitted, pending_review)
        grade: Current grade (may be None)
        score: Numeric score (may be None)
        submitted_at: ISO 8601 submission time (or None)
        graded_at: ISO 8601 grading time (or None)
        late: Whether submission was late
        missing: Whether submission is missing
        excused: Whether student is excused
    """
    submission = MagicMock()
    submission.id = 6001
    submission.user_id = 3001
    submission.assignment_id = 5001
    submission.workflow_state = "submitted"
    submission.grade = "A"
    submission.score = 95.0
    submission.submitted_at = "2023-12-14T18:30:00Z"
    submission.graded_at = "2023-12-16T10:00:00Z"
    submission.late = False
    submission.missing = False
    submission.excused = False

    return submission
@pytest.fixture
def mock_config():
    """
    Mock configuration dictionary.

    Provides minimal configuration needed for most commands.
    Tests can override values as needed.

    Keys:
        canvas_server: Canvas instance URL
        course_id: Default course ID (optional)
        assignment: Default assignment filter (optional)
    """
    return {
        "canvas_server": "https://canvas.example.edu",
        "course_id": None,
        "assignment": None,
    }
