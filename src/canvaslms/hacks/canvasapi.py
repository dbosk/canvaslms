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
