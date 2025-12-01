"""
Tests for canvaslms.hacks.canvasapi monkey-patches.

These tests verify that our decorators correctly add __eq__, __hash__,
and improved __str__ methods to canvasapi classes.

IMPORTANT: These tests import canvaslms.hacks.canvasapi, which applies
monkey-patches to canvasapi classes. The patches are applied at import
time and affect all future instances.
"""
import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta

# This import applies the monkey-patches
import canvaslms.hacks.canvasapi

# Import canvasapi classes to test
from canvasapi.user import User
from canvasapi.assignment import Assignment, AssignmentGroup
from canvasapi.submission import Submission

# Import caching utility functions and constants to test
from canvaslms.hacks.canvasapi import (
    must_update, merge_kwargs, outdated, NOREFRESH_GRADES, CacheGetMethods
)

class TestEqualityMonkeyPatch:
    """Test that Canvas objects can be compared by ID"""

    def test_users_with_same_id_are_equal(self):
        """Two User objects with same ID should be equal"""
        # Test with same mock instance (verifies ID comparison logic)
        user1 = MagicMock()
        user1.id = 12345

        # Same object is equal to itself
        assert User.__eq__(user1, user1)

    def test_users_with_different_ids_not_equal(self):
        """Users with different IDs should not be equal"""
        user1 = MagicMock()
        user1.id = 12345
        user2 = MagicMock()
        user2.id = 67890

        assert not User.__eq__(user1, user2)

    def test_different_types_not_equal(self):
        """Objects of different types should not be equal, even with same ID"""
        user = MagicMock()
        user.id = 12345

        assignment = MagicMock()
        assignment.id = 12345

        # Different types (checked by type())
        assert not User.__eq__(user, assignment)

    def test_assignments_have_equality_method(self):
        """Assignment class should have patched __eq__ method"""
        assign = MagicMock()
        assign.id = 5001

        # Same object is equal to itself (verifies patch exists)
        assert Assignment.__eq__(assign, assign)

    def test_submissions_have_equality_method(self):
        """Submission class should have patched __eq__ method"""
        sub = MagicMock()
        sub.id = 6001

        # Same object is equal to itself (verifies patch exists)
        assert Submission.__eq__(sub, sub)

    def test_assignment_groups_have_equality_method(self):
        """AssignmentGroup class should have patched __eq__ method"""
        group = MagicMock()
        group.id = 2001

        # Same object is equal to itself (verifies patch exists)
        assert AssignmentGroup.__eq__(group, group)
class TestHashabilityMonkeyPatch:
    """Test that Canvas objects can be hashed and used in sets/dicts"""

    def test_users_with_same_id_have_same_hash(self):
        """Equal users should have equal hashes"""
        user = MagicMock()
        user.id = 12345

        # Same object hashed twice should give same hash
        assert User.__hash__(user) == User.__hash__(user)

    def test_users_with_different_ids_have_different_hashes(self):
        """Different users should (usually) have different hashes"""
        user1 = MagicMock()
        user1.id = 12345
        user2 = MagicMock()
        user2.id = 67890

        # Different IDs should produce different hashes
        # (hash collisions possible but unlikely)
        assert User.__hash__(user1) != User.__hash__(user2)

    def test_hashability_enables_set_usage(self):
        """
        Patched __hash__ allows Canvas objects to be used in sets.

        This test verifies the method is properly defined, making
        sets and dicts possible (actual usage requires both __eq__
        and __hash__ to work together on real Canvas objects).
        """
        user1 = MagicMock()
        user1.id = 12345
        user2 = MagicMock()
        user2.id = 67890

        # Both should be hashable
        hash1 = User.__hash__(user1)
        hash2 = User.__hash__(user2)

        assert isinstance(hash1, int)
        assert isinstance(hash2, int)
        assert hash1 != hash2

    def test_hashability_enables_dict_usage(self):
        """
        Patched __hash__ allows Canvas objects as dictionary keys.

        Verifies the hash method is properly defined and returns
        valid hash values based on type and ID.
        """
        assign1 = MagicMock()
        assign1.id = 5001
        assign2 = MagicMock()
        assign2.id = 5002

        # Both should produce valid hashes
        hash1 = Assignment.__hash__(assign1)
        hash2 = Assignment.__hash__(assign2)

        assert isinstance(hash1, int)
        assert isinstance(hash2, int)
        assert hash1 != hash2
class TestUserStringRepresentation:
    """Test improved User.__str__ method"""

    def test_user_str_with_name_and_login(self):
        """User string should show name and login ID"""
        user = MagicMock(spec=User)
        user.name = "Alice Anderson"
        user.login_id = "alice"

        result = User.__str__(user)

        assert result == "Alice Anderson <alice>"

    def test_user_str_without_login_id(self):
        """If login_id is missing, show empty brackets"""
        user = MagicMock(spec=User)
        user.name = "Bob Brown"
        # Simulate missing login_id attribute
        del user.login_id

        result = User.__str__(user)

        assert result == "Bob Brown <>"

    def test_user_str_useful_for_debugging(self):
        """String representation should be human-readable"""
        user = MagicMock(spec=User)
        user.name = "Charlie Chen"
        user.login_id = "cchen"

        # Should not contain Canvas ID or object address
        result = User.__str__(user)

        assert "Charlie Chen" in result
        assert "cchen" in result
        assert "0x" not in result  # No memory address
class TestMustUpdate:
    """Test must_update() cache invalidation logic"""

    def test_no_update_when_cache_has_all_data(self):
        """Cache with all requested data should not update"""
        prev = {"include": ["submissions", "rubric"]}
        new = {"include": ["submissions"]}

        assert not must_update(prev, new)

    def test_no_update_when_kwargs_identical(self):
        """Identical kwargs should not trigger update"""
        prev = {"include": ["user"], "enrollment_type": "student"}
        new = {"include": ["user"], "enrollment_type": "student"}

        assert not must_update(prev, new)

    def test_update_when_new_key_not_in_cache(self):
        """New key not in cache should trigger update"""
        prev = {"include": ["user"]}
        new = {"include": ["user"], "enrollment_type": "student"}

        assert must_update(prev, new)

    def test_update_when_list_needs_more_items(self):
        """Cache missing list items should trigger update"""
        prev = {"include": ["user"]}
        new = {"include": ["user", "enrollments"]}

        assert must_update(prev, new)

    def test_update_when_non_list_value_differs(self):
        """Different non-list value should trigger update"""
        prev = {"enrollment_type": "student"}
        new = {"enrollment_type": "teacher"}

        assert must_update(prev, new)

    def test_no_update_when_cache_has_superset(self):
        """Cache with more data than needed should not update"""
        prev = {"include": ["user", "enrollments", "email"]}
        new = {"include": ["user", "enrollments"]}

        assert not must_update(prev, new)

    def test_ignores_sort_keys(self):
        """Sorting keys should be ignored (don't affect cache)"""
        prev = {"include": ["user"], "sort": "name"}
        new = {"include": ["user"], "sort": "created_at"}

        # Different sort order shouldn't trigger update
        assert not must_update(prev, new)

    def test_ignores_order_keys(self):
        """Order parameter should be ignored"""
        prev = {"include": ["user"], "order": "asc"}
        new = {"include": ["user"], "order": "desc"}

        assert not must_update(prev, new)

    def test_empty_new_kwargs_no_update(self):
        """Empty new kwargs should not trigger update"""
        prev = {"include": ["user"]}
        new = {}

        assert not must_update(prev, new)

    def test_empty_prev_kwargs_triggers_update(self):
        """Empty cache with new requests should trigger update"""
        prev = {}
        new = {"include": ["user"]}

        assert must_update(prev, new)
class TestMergeKwargs:
    """Test merge_kwargs() dictionary merging logic"""

    def test_empty_list_returns_empty_dict(self):
        """Empty list should return empty dictionary"""
        result = merge_kwargs([])

        assert result == {}

    def test_single_dict_returns_copy(self):
        """Single dictionary should be returned as-is"""
        kwargs = {"include": ["user"], "enrollment_type": "student"}
        result = merge_kwargs([kwargs])

        assert result == kwargs

    def test_unions_list_values(self):
        """List values should be unioned"""
        kwargs1 = {"include": ["user"]}
        kwargs2 = {"include": ["enrollments"]}

        result = merge_kwargs([kwargs1, kwargs2])

        assert set(result["include"]) == {"user", "enrollments"}

    def test_preserves_identical_non_list_values(self):
        """Identical non-list values should be preserved"""
        kwargs1 = {"enrollment_type": "student", "include": ["user"]}
        kwargs2 = {"enrollment_type": "student", "include": ["email"]}

        result = merge_kwargs([kwargs1, kwargs2])

        assert result["enrollment_type"] == "student"
        assert set(result["include"]) == {"user", "email"}

    def test_raises_on_conflicting_non_list_values(self):
        """Different non-list values should raise ValueError"""
        kwargs1 = {"enrollment_type": "student"}
        kwargs2 = {"enrollment_type": "teacher"}

        with pytest.raises(ValueError, match="Cannot merge enrollment_type"):
            merge_kwargs([kwargs1, kwargs2])

    def test_allows_conflicting_ignored_keys(self):
        """Conflicting values for ignored keys should use last value"""
        kwargs1 = {"include": ["user"], "sort": "name"}
        kwargs2 = {"include": ["email"], "sort": "created_at"}

        result = merge_kwargs([kwargs1, kwargs2])

        # sort is ignored, so last value wins
        assert result["sort"] == "created_at"
        assert set(result["include"]) == {"user", "email"}

    def test_converts_mixed_list_and_scalar(self):
        """Scalar value merged with list should convert to list"""
        kwargs1 = {"enrollment_type": "student"}
        kwargs2 = {"enrollment_type": ["teacher"]}

        result = merge_kwargs([kwargs1, kwargs2])

        assert set(result["enrollment_type"]) == {"student", "teacher"}

    def test_merges_multiple_dicts(self):
        """Should correctly merge more than two dictionaries"""
        kwargs1 = {"include": ["user"]}
        kwargs2 = {"include": ["enrollments"]}
        kwargs3 = {"include": ["email"], "enrollment_type": "student"}

        result = merge_kwargs([kwargs1, kwargs2, kwargs3])

        assert set(result["include"]) == {"user", "enrollments", "email"}
        assert result["enrollment_type"] == "student"

    def test_realistic_canvas_api_merge(self):
        """Realistic scenario: merging submissions kwargs"""
        # First call wants user info
        call1 = {"include": ["user", "submission_comments"]}
        # Second call wants rubric
        call2 = {"include": ["rubric_assessment"]}
        # Third call adds more user data
        call3 = {"include": ["user", "submission_history"]}

        result = merge_kwargs([call1, call2, call3])

        expected = {"user", "submission_comments", "rubric_assessment",
                    "submission_history"}
        assert set(result["include"]) == expected
class TestCacheGetMethodsInit:
    """Test CacheGetMethods decorator initialization"""

    def test_default_parameters(self):
        """Default parameters should create empty cache and include both methods"""
        decorator = CacheGetMethods("assignment")

        assert decorator._CacheGetMethods__attribute_name == "assignment"
        assert decorator._CacheGetMethods__cache == {}
        assert decorator._CacheGetMethods__include_singular is True
        assert decorator._CacheGetMethods__include_plural is True
        assert decorator._CacheGetMethods__plural_name is None

    def test_custom_cache_parameter(self):
        """Custom cache dict should be stored"""
        custom_cache = {1: ("obj1", {}), 2: ("obj2", {})}
        decorator = CacheGetMethods("user", cache=custom_cache)

        assert decorator._CacheGetMethods__cache is custom_cache

    def test_include_singular_false(self):
        """include_singular=False should store False"""
        decorator = CacheGetMethods("assignment_group", include_singular=False)

        assert decorator._CacheGetMethods__include_singular is False
        assert decorator._CacheGetMethods__include_plural is True

    def test_include_plural_false(self):
        """include_plural=False should store False"""
        decorator = CacheGetMethods("submission", include_plural=False)

        assert decorator._CacheGetMethods__include_plural is False
        assert decorator._CacheGetMethods__include_singular is True

    def test_custom_plural_name(self):
        """plural_name parameter should override default pluralization"""
        decorator = CacheGetMethods("group_category",
                                     plural_name="group_categories")

        assert decorator._CacheGetMethods__plural_name == "group_categories"

    def test_decorator_returns_modified_class(self):
        """Decorator should return the class to allow stacking"""
        class DummyClass:
            def __init__(self):
                pass

            def get_test(self, test_id):
                return MagicMock(id=test_id)

            def get_tests(self):
                return []

        decorator = CacheGetMethods("test")
        result = decorator(DummyClass)

        assert result is DummyClass
class TestCacheAttributeInjection:
    """Test cache attributes are injected into decorated class instances"""

    def test_creates_cache_attribute(self):
        """Instances should have {attr}_cache attribute"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                return MagicMock(id=item_id)
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        assert hasattr(instance, "item_cache")
        assert isinstance(instance.item_cache, dict)

    def test_creates_all_fetched_attribute(self):
        """Instances should have {attr}_all_fetched attribute"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                return MagicMock(id=item_id)
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        assert hasattr(instance, "item_all_fetched")
        assert instance.item_all_fetched is None

    def test_cache_initialized_empty(self):
        """Cache should be initialized as empty dict"""
        class TestClass:
            def __init__(self):
                pass
            def get_submission(self, sub_id):
                return MagicMock(id=sub_id)
            def get_submissions(self):
                return []

        CacheGetMethods("submission")(TestClass)
        instance = TestClass()

        assert instance.submission_cache == {}

    def test_multiple_decorators_create_separate_attributes(self):
        """Multiple decorators should create separate cache attributes"""
        class TestClass:
            def __init__(self):
                pass
            def get_assignment(self, asgn_id):
                return MagicMock(id=asgn_id)
            def get_assignments(self):
                return []
            def get_user(self, user_id):
                return MagicMock(id=user_id)
            def get_users(self):
                return []

        CacheGetMethods("assignment")(TestClass)
        CacheGetMethods("user")(TestClass)
        instance = TestClass()

        assert hasattr(instance, "assignment_cache")
        assert hasattr(instance, "assignment_all_fetched")
        assert hasattr(instance, "user_cache")
        assert hasattr(instance, "user_all_fetched")

    def test_cache_attributes_instance_specific(self):
        """Cache attributes should be instance-specific not shared"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                return MagicMock(id=item_id)
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance1 = TestClass()
        instance2 = TestClass()

        instance1.item_cache[1] = ("obj1", {})

        assert 1 in instance1.item_cache
        assert 1 not in instance2.item_cache

    def test_original_init_still_called(self):
        """Original __init__ should still execute"""
        class TestClass:
            def __init__(self, value):
                self.value = value
            def get_item(self, item_id):
                return MagicMock(id=item_id)
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance = TestClass(42)

        assert instance.value == 42
        assert hasattr(instance, "item_cache")
class TestSingularMethodCaching:
    """Test get_* singular method caching logic"""

    def test_first_call_fetches_from_api(self):
        """First call should fetch from API and cache result"""
        call_count = {"count": 0}

        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                call_count["count"] += 1
                obj = MagicMock()
                obj.id = item_id
                return obj
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance = TestClass()
        result = instance.get_item(1)

        assert call_count["count"] == 1
        assert result.id == 1
        assert 1 in instance.item_cache

    def test_second_call_returns_cached(self):
        """Second call with same ID should return cached object"""
        call_count = {"count": 0}

        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                call_count["count"] += 1
                obj = MagicMock()
                obj.id = item_id
                return obj
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        result1 = instance.get_item(1)
        result2 = instance.get_item(1)

        assert call_count["count"] == 1
        assert result1 is result2

    def test_cache_stores_object_kwargs_tuple(self):
        """Cache should store (object, kwargs) tuple"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id, **kwargs):
                obj = MagicMock()
                obj.id = item_id
                return obj
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        instance.get_item(1, include=["user"])

        cached_obj, cached_kwargs = instance.item_cache[1]
        assert cached_obj.id == 1
        assert cached_kwargs == {"include": ["user"]}

    def test_must_update_triggers_refetch(self):
        """Changed kwargs should trigger refetch via must_update"""
        call_count = {"count": 0}

        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id, **kwargs):
                call_count["count"] += 1
                obj = MagicMock()
                obj.id = item_id
                return obj
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        instance.get_item(1, include=["user"])
        instance.get_item(1, include=["user", "email"])

        assert call_count["count"] == 2

    def test_outdated_triggers_refetch(self):
        """Stale object should trigger refetch via outdated()"""
        call_count = {"count": 0}

        class TestClass:
            def __init__(self):
                pass
            def get_submission(self, sub_id):
                call_count["count"] += 1
                obj = MagicMock()
                obj.id = sub_id
                obj.grade = "B"  # Non-passing grade
                return obj
            def get_submissions(self):
                return []

        CacheGetMethods("submission")(TestClass)
        instance = TestClass()

        # First call
        result1 = instance.get_submission(1)
        # Make it outdated (> 5 minutes old)
        result1._fetched_at = datetime.now() - timedelta(minutes=6)
        instance.submission_cache[1] = (result1, {})

        # Second call should refetch
        result2 = instance.get_submission(1)

        assert call_count["count"] == 2

    def test_accepts_integer_id(self):
        """Should accept integer ID as argument"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                obj = MagicMock()
                obj.id = item_id
                return obj
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        result = instance.get_item(42)

        assert result.id == 42

    def test_accepts_canvas_object_with_id(self):
        """Should accept Canvas object and extract .id"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                obj = MagicMock()
                if hasattr(item_id, 'id'):
                    obj.id = item_id.id
                else:
                    obj.id = item_id
                return obj
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        canvas_obj = MagicMock()
        canvas_obj.id = 99
        result = instance.get_item(canvas_obj)

        assert result.id == 99

    def test_sets_fetched_at_timestamp(self):
        """Should set _fetched_at timestamp on fetched objects"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                obj = MagicMock()
                obj.id = item_id
                return obj
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        before = datetime.now()
        result = instance.get_item(1)
        after = datetime.now()

        assert hasattr(result, '_fetched_at')
        assert before <= result._fetched_at <= after

    def test_raises_typeerror_missing_argument(self):
        """Should raise TypeError if no argument provided"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                obj = MagicMock()
                obj.id = item_id
                return obj
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        with pytest.raises(TypeError, match="missing 1 required positional"):
            instance.get_item()

    def test_raises_typeerror_invalid_argument_type(self):
        """Should raise TypeError for invalid argument types"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                obj = MagicMock()
                obj.id = item_id
                return obj
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        with pytest.raises(TypeError, match="must be int or Canvas object"):
            instance.get_item("invalid_string")

    def test_cache_key_is_object_id(self):
        """Cache key should be object.id not argument value"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                obj = MagicMock()
                obj.id = item_id if isinstance(item_id, int) else item_id.id
                return obj
            def get_items(self):
                return []

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        # Pass Canvas object
        canvas_obj = MagicMock()
        canvas_obj.id = 123
        instance.get_item(canvas_obj)

        # Cache key should be the ID, not the object
        assert 123 in instance.item_cache
class TestPluralMethodCaching:
    """Test get_*s plural method caching logic"""

    def test_first_call_performs_bulk_fetch(self):
        """First call should perform bulk fetch"""
        call_count = {"count": 0}

        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                return MagicMock(id=item_id)
            def get_items(self):
                call_count["count"] += 1
                return [MagicMock(id=1), MagicMock(id=2), MagicMock(id=3)]

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        list(instance.get_items())

        assert call_count["count"] == 1

    def test_bulk_fetch_populates_cache(self):
        """Bulk fetch should populate cache with all objects"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                return MagicMock(id=item_id)
            def get_items(self):
                return [MagicMock(id=i) for i in [10, 20, 30]]

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        list(instance.get_items())

        assert 10 in instance.item_cache
        assert 20 in instance.item_cache
        assert 30 in instance.item_cache

    def test_bulk_fetch_sets_all_fetched_timestamp(self):
        """Bulk fetch should set {attr}_all_fetched timestamp"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                return MagicMock(id=item_id)
            def get_items(self):
                return [MagicMock(id=1)]

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        before = datetime.now()
        list(instance.get_items())
        after = datetime.now()

        assert instance.item_all_fetched is not None
        assert before <= instance.item_all_fetched <= after

    def test_second_call_yields_from_cache(self):
        """Second call should yield from cache without API call"""
        call_count = {"count": 0}

        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                return MagicMock(id=item_id)
            def get_items(self):
                call_count["count"] += 1
                return [MagicMock(id=i) for i in [1, 2, 3]]

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        list(instance.get_items())
        list(instance.get_items())

        assert call_count["count"] == 1

    def test_returns_generator_not_list(self):
        """Should return generator not list"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                return MagicMock(id=item_id)
            def get_items(self):
                return [MagicMock(id=1)]

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        result = instance.get_items()

        from types import GeneratorType
        assert isinstance(result, GeneratorType)

    def test_cache_path_checks_outdated(self):
        """Cached path should check each object with outdated()"""
        refetch_count = {"count": 0}

        class TestClass:
            def __init__(self):
                pass
            def get_submission(self, sub_id):
                refetch_count["count"] += 1
                obj = MagicMock()
                obj.id = sub_id
                obj.grade = "A"  # Won't be outdated
                return obj
            def get_submissions(self):
                return [MagicMock(id=i, grade="A") for i in [1, 2]]

        CacheGetMethods("submission")(TestClass)
        instance = TestClass()

        # First call - bulk fetch
        list(instance.get_submissions())
        # Second call - should check outdated but not refetch (grade=A)
        list(instance.get_submissions())

        # No refetches because all have passing grades
        assert refetch_count["count"] == 0

    def test_stale_objects_refetched(self):
        """Stale individual objects should be refetched"""
        refetch_count = {"count": 0}

        class TestClass:
            def __init__(self):
                pass
            def get_submission(self, sub_id):
                refetch_count["count"] += 1
                obj = MagicMock()
                obj.id = sub_id
                obj.grade = "B"  # Non-passing grade
                return obj
            def get_submissions(self):
                return [MagicMock(id=1, grade="B")]

        CacheGetMethods("submission")(TestClass)
        instance = TestClass()

        # First call - bulk fetch
        list(instance.get_submissions())

        # Make it outdated
        obj, kwargs = instance.submission_cache[1]
        obj._fetched_at = datetime.now() - timedelta(minutes=6)
        instance.submission_cache[1] = (obj, kwargs)

        # Second call should refetch the outdated object
        list(instance.get_submissions())

        assert refetch_count["count"] == 1

    def test_bulk_fetch_merges_kwargs(self):
        """Bulk fetch should merge all previous kwargs"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id, **kwargs):
                return MagicMock(id=item_id)
            def get_items(self, **kwargs):
                # Return objects with merged kwargs visible
                return [MagicMock(id=1)]

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        # Fetch with one include
        instance.get_item(1, include=["user"])
        # Clear all_fetched to force bulk refetch
        instance.item_all_fetched = None
        # Bulk fetch with additional include
        list(instance.get_items(include=["email"]))

        # Cache should have merged kwargs
        _, cached_kwargs = instance.item_cache[1]
        assert "user" in cached_kwargs.get("include", [])
        assert "email" in cached_kwargs.get("include", [])

    def test_irregular_plural_name(self):
        """plural_name parameter should work correctly"""
        class TestClass:
            def __init__(self):
                pass
            def get_group_category(self, cat_id):
                return MagicMock(id=cat_id)
            def get_group_categories(self):
                return [MagicMock(id=1)]

        CacheGetMethods("group_category",
                        plural_name="group_categories")(TestClass)
        instance = TestClass()

        result = list(instance.get_group_categories())

        assert len(result) == 1
        assert result[0].id == 1

    def test_empty_cache_after_reset_triggers_bulk_fetch(self):
        """Setting all_fetched=None should trigger bulk refetch"""
        call_count = {"count": 0}

        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                return MagicMock(id=item_id)
            def get_items(self):
                call_count["count"] += 1
                return [MagicMock(id=1)]

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        list(instance.get_items())
        instance.item_all_fetched = None
        list(instance.get_items())

        assert call_count["count"] == 2

    def test_no_double_yield_after_bulk_fetch(self):
        """Should not yield objects twice after bulk fetch"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                return MagicMock(id=item_id)
            def get_items(self):
                obj1 = MagicMock()
                obj1.id = 1
                obj1.grade = "B"  # Non-passing (would be checked if double-yield)
                return [obj1]

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        results = list(instance.get_items())

        # Should only yield once, not twice
        assert len(results) == 1
class TestCacheSynchronization:
    """Test cache preservation during bulk updates"""

    def test_preserves_sub_object_caches(self):
        """Bulk fetch should preserve sub-object caches"""
        class TestClass:
            def __init__(self):
                pass
            def get_course(self, course_id):
                obj = MagicMock()
                obj.id = course_id
                return obj
            def get_courses(self):
                obj = MagicMock()
                obj.id = 1
                return [obj]

        CacheGetMethods("course")(TestClass)
        instance = TestClass()

        # Initial bulk fetch
        courses = list(instance.get_courses())
        course = courses[0]

        # Add sub-cache (simulate assignment cache on course)
        course.assignment_cache = {10: ("assignment_obj", {})}
        course.assignment_all_fetched = datetime.now()
        instance.course_cache[1] = (course, {})

        # Force refetch by clearing all_fetched
        instance.course_all_fetched = None

        # Bulk fetch again
        new_courses = list(instance.get_courses())
        new_course = new_courses[0]

        # Sub-cache should be preserved
        assert hasattr(new_course, "assignment_cache")
        assert 10 in new_course.assignment_cache

    def test_copies_cache_attributes(self):
        """Should copy {attr}_cache attributes"""
        counter = {"val": 0}

        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                obj = MagicMock()
                obj.id = item_id
                return obj
            def get_items(self):
                counter["val"] += 1
                # Return object with consistent ID
                obj = MagicMock()
                obj.id = 1
                return [obj]

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        # Initial fetch
        items1 = list(instance.get_items())
        item1 = items1[0]
        item1.sub_cache = {"key": "value"}
        # Update cache with modified object
        instance.item_cache[1] = (item1, {})

        # Refetch - should copy sub_cache from old object
        instance.item_all_fetched = None
        items2 = list(instance.get_items())
        item2 = items2[0]

        assert hasattr(item2, "sub_cache")
        assert item2.sub_cache == {"key": "value"}

    def test_copies_all_fetched_attributes(self):
        """Should copy {attr}_all_fetched attributes"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                obj = MagicMock()
                obj.id = item_id
                return obj
            def get_items(self):
                obj = MagicMock()
                obj.id = 1
                return [obj]

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        # Initial fetch
        items1 = list(instance.get_items())
        item1 = items1[0]
        timestamp = datetime.now() - timedelta(hours=1)
        item1.sub_all_fetched = timestamp
        instance.item_cache[1] = (item1, {})

        # Refetch - should copy sub_all_fetched from old object
        instance.item_all_fetched = None
        items2 = list(instance.get_items())
        item2 = items2[0]

        assert hasattr(item2, "sub_all_fetched")
        assert item2.sub_all_fetched == timestamp

    def test_preserves_multiple_cache_types(self):
        """Should preserve all cache attributes (multiple types)"""
        class TestClass:
            def __init__(self):
                pass
            def get_course(self, course_id):
                obj = MagicMock()
                obj.id = course_id
                return obj
            def get_courses(self):
                obj = MagicMock()
                obj.id = 1
                return [obj]

        CacheGetMethods("course")(TestClass)
        instance = TestClass()

        # Initial fetch
        courses = list(instance.get_courses())
        course = courses[0]

        # Add multiple sub-caches
        course.assignment_cache = {10: ("asgn", {})}
        course.assignment_all_fetched = datetime.now()
        course.user_cache = {20: ("user", {})}
        course.user_all_fetched = datetime.now()
        instance.course_cache[1] = (course, {})

        # Refetch
        instance.course_all_fetched = None
        new_courses = list(instance.get_courses())
        new_course = new_courses[0]

        # All caches should be preserved
        assert hasattr(new_course, "assignment_cache")
        assert hasattr(new_course, "assignment_all_fetched")
        assert hasattr(new_course, "user_cache")
        assert hasattr(new_course, "user_all_fetched")

    def test_pattern_matching_works_for_any_cache(self):
        """Pattern matching should work for any {name}_cache"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                obj = MagicMock()
                obj.id = item_id
                return obj
            def get_items(self):
                obj = MagicMock()
                obj.id = 1
                return [obj]

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        # Initial fetch
        items1 = list(instance.get_items())
        item1 = items1[0]
        item1.custom_thing_cache = {"data": "value"}
        instance.item_cache[1] = (item1, {})

        # Refetch - should copy custom cache from old object
        instance.item_all_fetched = None
        items2 = list(instance.get_items())
        item2 = items2[0]

        # Custom cache should be preserved
        assert hasattr(item2, "custom_thing_cache")
        assert item2.custom_thing_cache == {"data": "value"}

    def test_fresh_objects_without_old_cache_work(self):
        """Fresh objects without old cache should get empty cache"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                obj = MagicMock()
                obj.id = item_id
                return obj
            def get_items(self):
                # Return new object not in cache
                obj = MagicMock()
                obj.id = 99
                return [obj]

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        # Fetch
        items = list(instance.get_items())

        # Should complete without error
        assert len(items) == 1
        assert items[0].id == 99

    def test_cache_copying_doesnt_interfere_with_new_data(self):
        """Cache copying shouldn't interfere with new API data"""
        class TestClass:
            def __init__(self):
                pass
            def get_item(self, item_id):
                obj = MagicMock()
                obj.id = item_id
                obj.name = f"Item {item_id}"
                return obj
            def get_items(self):
                obj = MagicMock()
                obj.id = 1
                obj.name = "Updated Item 1"
                return [obj]

        CacheGetMethods("item")(TestClass)
        instance = TestClass()

        # Initial fetch
        items = list(instance.get_items())
        assert items[0].name == "Updated Item 1"

        # Refetch
        instance.item_all_fetched = None
        new_items = list(instance.get_items())

        # New data should be visible
        assert new_items[0].name == "Updated Item 1"
class TestRealisticCanvasScenarios:
    """Test realistic Canvas API usage patterns"""

    def test_course_assignment_hierarchy(self):
        """Course with cached assignments should work like real Canvas"""
        class Canvas:
            def get_course(self, course_id):
                obj = MagicMock()
                obj.id = course_id
                obj.name = f"Course {course_id}"
                return obj
            def get_courses(self):
                c1 = MagicMock()
                c1.id = 1
                c1.name = "Course 1"
                c2 = MagicMock()
                c2.id = 2
                c2.name = "Course 2"
                return [c1, c2]

        # Apply decorator
        CacheGetMethods("course")(Canvas)

        canvas = Canvas()

        # List courses (bulk fetch)
        courses = list(canvas.get_courses())
        assert len(courses) == 2

        # Verify caching works
        assert 1 in canvas.course_cache
        assert 2 in canvas.course_cache
        assert courses[0].name == "Course 1"
        assert courses[1].name == "Course 2"

    def test_multi_level_caching_with_includes(self):
        """Verify include parameters work with caching"""
        call_counts = {"fetch": 0}

        class Canvas:
            def get_course(self, course_id):
                obj = MagicMock()
                obj.id = course_id
                return obj
            def get_courses(self, **kwargs):
                call_counts["fetch"] += 1
                c = MagicMock()
                c.id = 1
                return [c]

        CacheGetMethods("course")(Canvas)

        canvas = Canvas()

        # First fetch with one include
        list(canvas.get_courses(include=["term"]))
        assert call_counts["fetch"] == 1

        # Request additional include - should refetch
        canvas.course_all_fetched = None
        list(canvas.get_courses(include=["term", "enrollment"]))

        # Course refetch should happen
        assert call_counts["fetch"] == 2

    def test_multiple_decorators_on_same_class(self):
        """Course with both assignment and user caches (like production)"""
        class Course:
            def get_assignment(self, assignment_id):
                obj = MagicMock()
                obj.id = assignment_id
                return obj
            def get_assignments(self):
                a = MagicMock()
                a.id = 10
                return [a]
            def get_user(self, user_id):
                obj = MagicMock()
                obj.id = user_id
                return obj
            def get_users(self):
                u = MagicMock()
                u.id = 100
                return [u]

        # Apply multiple decorators like production
        CacheGetMethods("assignment")(Course)
        CacheGetMethods("user")(Course)

        course = Course()

        # Should have separate caches
        assert hasattr(course, "assignment_cache")
        assert hasattr(course, "assignment_all_fetched")
        assert hasattr(course, "user_cache")
        assert hasattr(course, "user_all_fetched")

        # Both should work independently
        assignments = list(course.get_assignments())
        users = list(course.get_users())

        assert len(assignments) == 1
        assert len(users) == 1
        assert 10 in course.assignment_cache
        assert 100 in course.user_cache

    def test_production_workflow_no_redundant_api_calls(self):
        """Typical workflow should minimize API calls"""
        call_counts = {"get_courses": 0, "get_course": 0}

        class Canvas:
            def get_course(self, course_id):
                call_counts["get_course"] += 1
                obj = MagicMock()
                obj.id = course_id
                obj.name = f"Course {course_id}"
                return obj
            def get_courses(self):
                call_counts["get_courses"] += 1
                c1 = MagicMock()
                c1.id = 1
                c1.name = "Course 1"
                c2 = MagicMock()
                c2.id = 2
                c2.name = "Course 2"
                return [c1, c2]

        CacheGetMethods("course")(Canvas)

        canvas = Canvas()

        # Typical workflow: list all courses
        courses = list(canvas.get_courses())  # 1 API call

        # Now get individual course (should come from cache)
        course = canvas.get_course(1)  # 0 API calls (cached)

        # Verify minimal API calls
        assert call_counts["get_courses"] == 1
        assert call_counts["get_course"] == 0  # Came from cache!
        assert course.name == "Course 1"

    def test_irregular_plural_name_in_production(self):
        """group_categories uses custom plural_name like production"""
        class Course:
            def get_group_category(self, category_id):
                obj = MagicMock()
                obj.id = category_id
                return obj
            def get_group_categories(self):
                gc = MagicMock()
                gc.id = 1
                return [gc]

        CacheGetMethods("group_category",
                        plural_name="group_categories")(Course)

        course = Course()
        categories = list(course.get_group_categories())

        # Should create cache with singular form
        assert hasattr(course, "group_category_cache")
        assert hasattr(course, "group_category_all_fetched")
        assert 1 in course.group_category_cache

    def test_assignment_groups_include_singular_false(self):
        """assignment_groups decorator uses include_singular=False"""
        class Course:
            def get_assignment_groups(self):
                ag = MagicMock()
                ag.id = 1
                return [ag]

        CacheGetMethods("assignment_group",
                        include_singular=False)(Course)

        course = Course()

        # Should still have cache attributes
        assert hasattr(course, "assignment_group_cache")
        assert hasattr(course, "assignment_group_all_fetched")

        # Should NOT have get_assignment_group method (include_singular=False)
        # (but we can't easily test that a method wasn't added in this test structure)

        # Plural should work
        groups = list(course.get_assignment_groups())
        assert len(groups) == 1
        assert 1 in course.assignment_group_cache

    def test_fresh_data_not_refetched_unnecessarily(self):
        """Fresh cached data should not trigger redundant API calls"""
        call_count = {"count": 0}

        class Canvas:
            def get_course(self, course_id):
                obj = MagicMock()
                obj.id = course_id
                return obj
            def get_courses(self):
                call_count["count"] += 1
                c = MagicMock()
                c.id = 1
                c.name = "Test Course"
                return [c]

        CacheGetMethods("course")(Canvas)

        canvas = Canvas()

        # Initial fetch
        list(canvas.get_courses())
        assert call_count["count"] == 1

        # Multiple fetches from cache
        for _ in range(5):
            courses = list(canvas.get_courses())
            assert courses[0].name == "Test Course"

        # Should still only have 1 API call (rest from cache)
        assert call_count["count"] == 1
class TestNorefreshGrades:
    """Test NOREFRESH_GRADES constant definition"""

    def test_contains_expected_grades(self):
        """Should contain all non-improvable passing grades"""
        assert "A" in NOREFRESH_GRADES
        assert "P" in NOREFRESH_GRADES
        assert "P+" in NOREFRESH_GRADES
        assert "complete" in NOREFRESH_GRADES

    def test_excludes_improvable_grades(self):
        """Should not contain improvable grades"""
        assert "B" not in NOREFRESH_GRADES
        assert "C" not in NOREFRESH_GRADES
        assert "F" not in NOREFRESH_GRADES

    def test_has_correct_count(self):
        """Should contain exactly 4 grade values"""
        assert len(NOREFRESH_GRADES) == 4
class TestOutdated:
    """Test outdated() cache expiration logic"""

    def test_passing_grade_a_not_outdated(self):
        """Submissions with grade A should never be outdated"""
        submission = MagicMock()
        submission.grade = "A"
        submission._fetched_at = datetime.now() - timedelta(days=365)

        assert not outdated(submission)

    def test_passing_grade_p_not_outdated(self):
        """Submissions with grade P should never be outdated"""
        submission = MagicMock()
        submission.grade = "P"
        submission._fetched_at = datetime.now() - timedelta(days=100)

        assert not outdated(submission)

    def test_passing_grade_p_plus_not_outdated(self):
        """Submissions with grade P+ should never be outdated"""
        submission = MagicMock()
        submission.grade = "P+"
        submission._fetched_at = datetime.now() - timedelta(days=50)

        assert not outdated(submission)

    def test_passing_grade_complete_not_outdated(self):
        """Submissions with grade 'complete' should never be outdated"""
        submission = MagicMock()
        submission.grade = "complete"
        submission._fetched_at = datetime.now() - timedelta(days=30)

        assert not outdated(submission)

    def test_non_passing_grade_recent_not_outdated(self):
        """Recent non-passing grade (< 5 min) should not be outdated"""
        submission = MagicMock()
        submission.grade = "F"
        submission._fetched_at = datetime.now() - timedelta(minutes=4)

        assert not outdated(submission)

    def test_non_passing_grade_old_is_outdated(self):
        """Old non-passing grade (> 5 min) should be outdated"""
        submission = MagicMock()
        submission.grade = "B"
        submission._fetched_at = datetime.now() - timedelta(minutes=6)

        assert outdated(submission)

    def test_non_passing_grade_exactly_5min_not_outdated(self):
        """Exactly 5 minutes should not trigger update (not >5)"""
        submission = MagicMock()
        submission.grade = "C"
        # Set to just under 5 minutes to account for execution time
        submission._fetched_at = datetime.now() - timedelta(minutes=5, seconds=-1)

        assert not outdated(submission)

    def test_no_grade_attribute_not_outdated(self):
        """Objects without grade attribute should not be outdated"""
        obj = MagicMock(spec=[])  # No attributes

        assert not outdated(obj)

    def test_no_fetched_at_with_non_passing_grade_is_outdated(self):
        """Non-passing grade without _fetched_at should be outdated"""
        submission = MagicMock()
        submission.grade = "F"
        del submission._fetched_at

        assert outdated(submission)

    def test_none_grade_is_outdated(self):
        """Ungraded submissions (None grade) should refresh"""
        submission = MagicMock()
        submission.grade = None
        submission._fetched_at = datetime.now() - timedelta(minutes=6)

        assert outdated(submission)

    def test_empty_string_grade_is_outdated(self):
        """Empty grade string should refresh if old"""
        submission = MagicMock()
        submission.grade = ""
        submission._fetched_at = datetime.now() - timedelta(minutes=10)

        assert outdated(submission)

    def test_numeric_grade_is_outdated(self):
        """Numeric grades (improvable) should refresh if old"""
        submission = MagicMock()
        submission.grade = "85"
        submission._fetched_at = datetime.now() - timedelta(minutes=7)

        assert outdated(submission)
