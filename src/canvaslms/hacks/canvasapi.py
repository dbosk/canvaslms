"""A module that modifies the classes of the canvasapi package"""

import cachetools
import canvasapi.assignment
from canvasapi.user import User
from datetime import datetime, timedelta
import functools
import importlib
import inspect
import sys

NOREFRESH_GRADES = ["A", "P", "P+", "complete"]


def make_classes_comparable():
    """Improves the classes by adding __eq__ and __hash__ methods"""

    def canvas_comparable(cls):
        def is_equal(self, other):
            """Tests if Canvas objects self and other refer to the same object"""
            return type(self) == type(other) and self.id == other.id

        cls.__eq__ = is_equal
        return cls

    def canvas_hashable(cls):
        def canvas_hash(self):
            """Returns a hash suitable for Canvas objects"""
            return hash(type(self)) ^ hash(self.id)

        cls.__hash__ = canvas_hash
        return cls

    # classes to improve in each module
    CANVASAPI_CLASSES = {
        "assignment": ["Assignment", "AssignmentGroup"],
        "submission": ["Submission"],
        "user": ["User"],
    }
    canvasapi_modules = {}

    # import all modules
    for module_name in CANVASAPI_CLASSES:
        canvasapi_modules[module_name] = importlib.import_module(
            f"canvasapi.{module_name}"
        )
    for module_name, module in canvasapi_modules.items():
        module_members = inspect.getmembers(module)
        for obj_name, obj in module_members:
            if obj_name in CANVASAPI_CLASSES[module_name]:
                canvas_comparable(obj)
                canvas_hashable(obj)


def make_useful_user_dunder_str():
    """Improves the user class by changing __str__"""

    def name_and_login(self):
        try:
            return f"{self.name} <{self.login_id}>"
        except AttributeError as err:
            return f"{self.name} <>"

    import canvasapi.user

    canvasapi.user.User.__str__ = name_and_login


def must_update(prev_kwargs, new_kwargs, ignore_keys=["sort", "order", "order_by"]):
    """
    Returns True if we must update the cache (refetch).

    By default, we ignore the keys

      "sort",
      "order",
      "order_by"

    as they don't affect the caching.
    """
    for key, value in new_kwargs.items():
        if key not in prev_kwargs:
            return True
        elif isinstance(value, list):
            if set(value) > set(prev_kwargs[key]):
                return True
        elif value != prev_kwargs[key]:
            return True

    return False


def merge_kwargs(kwargs_list, ignore_keys=["sort", "order", "order_by"]):
    """
    Merges a list of keyword arguments dictionaries. Lists are unioned.
    All non-list keys (usually strings) must be the same in all dictionaries.

    By default, we ignore the keys

      "sort",
      "order",
      "order_by"

    as they don't affect the caching.
    """
    new_kwargs = dict()

    for kwargs in kwargs_list:
        for key, value in kwargs.items():
            if key not in new_kwargs:
                new_kwargs[key] = value
            elif isinstance(kwargs[key], list):
                new_kwargs[key] = list(set(value) | set(new_kwargs[key]))
            else:
                if key in ignore_keys:
                    new_kwargs[key] = value
                elif value != new_kwargs[key]:
                    raise ValueError(
                        f"Cannot merge {key} with " f"{value} and {new_kwargs[key]}"
                    )

    return new_kwargs


class CacheGetMethods:
    """
    General class decorator to add caching to get_*{,s} methods.

    We assume that the first positional argument is the ID of the object to fetch.
    This must be the same as the `.id` attribute of an object (`obj.id`).
    """

    def __init__(self, attribute_name, cache=None, include_plural=True):
        """No parameters required"""
        self.__attribute_name = attribute_name
        self.__include_plural = include_plural
        self.__cache = cache if cache else {}

    def __call__(self, cls):
        """Applies the decorator to the class cls"""
        init = cls.__init__
        cache = self.__cache
        attr_name = self.__attribute_name

        @functools.wraps(init)
        def new_init(*args, **kwargs):
            self = args[0]
            self.attr_name = attr_name
            setattr(self, f"{self.attr_name}_cache", cache)
            setattr(self, f"{self.attr_name}_all_fetched", None)
            init(*args, **kwargs)

        cls.__init__ = new_init

        singular_name = f"get_{self.__attribute_name}"
        get_attr = getattr(cls, singular_name)

        @functools.wraps(get_attr)
        def new_get_attr(self, *args, **kwargs):
            attr_cache = getattr(self, f"{self.attr_name}_cache")

            try:
                obj = args[0]
                id = obj.id
            except IndexError:
                raise TypeError(
                    f"{singular_name}() missing 1 required positional "
                    f"argument: 'id'"
                )
            except AttributeError:
                if isinstance(obj, int):
                    id = obj
                else:
                    raise TypeError(
                        f"{singular_name}() argument 1 must be int or "
                        f"Canvas object, not {type(obj)}"
                    )

            try:
                obj, prev_kwargs = attr_cache[id]
            except KeyError:
                obj = None
                prev_kwargs = {}

            if obj and (must_update(prev_kwargs, kwargs) or outdated(obj)):
                obj = None

            if not obj:
                obj = get_attr(self, *args, **kwargs)
                attr_cache[obj.id] = (obj, kwargs)

            return obj

        setattr(cls, singular_name, new_get_attr)

        if self.__include_plural:
            plural_name = f"get_{self.__attribute_name}s"
            get_attrs = getattr(cls, plural_name)

            @functools.wraps(get_attrs)
            def new_get_attrs(self, *args, **kwargs):
                attr_cache = getattr(self, f"{self.attr_name}_cache")
                attr_all_fetched = getattr(self, f"{self.attr_name}_all_fetched")

                if attr_all_fetched:
                    for _, prev_kwargs in attr_cache.values():
                        if must_update(prev_kwargs, kwargs):
                            attr_all_fetched = None
                            break

                if not attr_all_fetched:
                    union_kwargs = merge_kwargs(
                        [kwargs for _, kwargs in attr_cache.values()] + [kwargs]
                    )

                    for obj in get_attrs(self, *args, **union_kwargs):
                        old_obj = attr_cache.get(obj.id, None)
                        for attr_name in dir(old_obj):
                            if attr_name.endswith("_cache") or attr_name.endswith(
                                "_all_fetched"
                            ):
                                setattr(obj, attr_name, getattr(old_obj, attr_name))
                        attr_cache[obj.id] = (obj, union_kwargs)

                    setattr(self, f"{self.attr_name}_all_fetched", datetime.now())
                    attr_all_fetched = getattr(self, f"{self.attr_name}_all_fetched")
                    for obj, _ in attr_cache.values():
                        yield obj

                for obj, obj_kwargs in attr_cache.values():
                    if outdated(obj):
                        obj = get_attr(self, obj.id, **obj_kwargs)
                    yield obj

            setattr(cls, plural_name, new_get_attrs)
        return cls


def outdated(obj):
    """Returns True if the object obj is outdated"""
    try:
        if obj.grade not in NOREFRESH_GRADES:
            return True
    except AttributeError:
        pass
    for attr_name in dir(obj):
        if attr_name == "user_all_fetched":
            if datetime.now() - getattr(obj, attr_name) > timedelta(days=2):
                setattr(obj, attr_name, None)
        elif attr_name.endswith("_all_fetched"):
            if not getattr(obj, attr_name):
                continue
            elif datetime.now() - getattr(obj, attr_name) > timedelta(days=7):
                setattr(obj, attr_name, None)
    return False


def make_canvas_courses_cacheable():
    import canvasapi.canvas

    canvasapi.canvas.Canvas = CacheGetMethods("course")(canvasapi.canvas.Canvas)


def make_course_contents_cacheable():
    import canvasapi.course

    canvasapi.course.Course = CacheGetMethods("assignment")(canvasapi.course.Course)
    canvasapi.course.Course = CacheGetMethods("user")(canvasapi.course.Course)


def make_assignment_submissions_cacheable():
    def cache_submissions(cls):
        """Class decorator for cacheable get_submission, get_submissions methods"""
        old_constructor = cls.__init__

        @functools.wraps(cls.__init__)
        def new_init(*args, **kwargs):
            args[0].__cache = {}
            args[0].__all_fetched = False
            old_constructor(*args, **kwargs)

        cls.__init__ = new_init

        get_submission = cls.get_submission

        @functools.wraps(cls.get_submission)
        def new_get_submission(self, user, **kwargs):
            if isinstance(user, User):
                uid = user.id
            elif isinstance(user, int):
                uid = user
            else:
                raise TypeError(f"user must be User or int")

            submission = None

            if "include" in kwargs:
                to_include = set(kwargs["include"])
            else:
                to_include = set()

            if uid in self.__cache:
                submission, included = self.__cache[uid]
                if not to_include.issubset(set(included)):
                    submission = None
                    to_include |= set(included)

            if not submission or submission.grade not in NOREFRESH_GRADES:
                submission = get_submission(self, user, include=list(to_include))
                self.__cache[uid] = (submission, to_include)

            return submission

        cls.get_submission = new_get_submission

        get_submissions = cls.get_submissions

        @functools.wraps(cls.get_submissions)
        def new_get_submissions(self, **kwargs):
            if "include" in kwargs:
                to_include = set(kwargs["include"])
            else:
                to_include = set()

            if self.__all_fetched:
                for submission, included in self.__cache.values():
                    if (
                        not to_include.issubset(included)
                        or submission.grade not in NOREFRESH_GRADES
                    ):
                        self.get_submission(
                            submission.user_id, include=list(to_include)
                        )
            else:
                for _, included in self.__cache.values():
                    to_include |= included

                for submission in get_submissions(self, **kwargs):
                    self.__cache[submission.user_id] = (submission, to_include)

            return [submission for submission, _ in self.__cache.values()]

        cls.get_submissions = new_get_submissions
        return cls

    canvasapi.assignment.Assignment = cache_submissions(canvasapi.assignment.Assignment)


# Loads all hacks
this_module = sys.modules[__name__]

# automatically execute all functions in this module
for _, function in inspect.getmembers(this_module, inspect.isfunction):
    function()
