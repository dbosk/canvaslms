"""A module that modifies the classes of the canvasapi package"""

import importlib
import inspect
import sys


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


# Loads all hacks
this_module = sys.modules[__name__]

# automatically execute all functions in this module
for _, function in inspect.getmembers(this_module, inspect.isfunction):
    function()
