import argparse
import canvasapi
import canvaslms.cli.courses as courses
import csv
import re
import sys


def modules_command(config, canvas, args):
    output = csv.writer(sys.stdout, delimiter=args.delimiter)
    course_list = courses.process_course_option(canvas, args)

    for course in course_list:
        modules = filter_modules(course, args.regex)
        for module in modules:
            # Get module items count
            try:
                items = list(module.get_module_items())
                item_count = len(items)
            except:
                item_count = 0

            output.writerow(
                [
                    course.course_code,
                    module.name,
                    module.id,
                    module.unlock_at if hasattr(module, "unlock_at") else None,
                    (
                        module.require_sequential_progress
                        if hasattr(module, "require_sequential_progress")
                        else False
                    ),
                    item_count,
                ]
            )


def add_module_option(parser, required=False):
    """Adds module selection option to parser"""
    try:
        courses.add_course_option(parser, required=required)
    except argparse.ArgumentError:
        pass

    parser.add_argument(
        "-M",
        "--module",
        required=required,
        default="" if not required else None,
        help="Regex matching module title or Canvas identifier.",
    )


def process_module_option(canvas, args):
    """Processes module selection from command line args"""
    course_list = courses.process_course_option(canvas, args)
    modules_list = []

    for course in course_list:
        try:
            module_regex = args.module
        except AttributeError:
            module_regex = ".*"

        if module_regex:
            modules = filter_modules(course, module_regex)
            modules_list.extend(modules)

    return modules_list


def filter_modules(course, regex):
    """Returns all modules of course whose name matches regex"""
    name = re.compile(regex)
    return filter(
        lambda module: name.search(module.name) or name.search(str(module.id)),
        course.get_modules(),
    )


def filter_assignments_by_module(module, assignments):
    """Returns elements in assignments that are part of module"""
    # Get all module items that are assignments
    assignment_ids = set()
    try:
        for item in module.get_module_items():
            if hasattr(item, "type") and item.type == "Assignment":
                assignment_ids.add(item.content_id)
    except AttributeError:
        # Handle cases where module items don't have expected attributes
        pass

    for assignment in assignments:
        if assignment.id in assignment_ids:
            yield assignment


def add_command(subp):
    """Adds the subcommand and its options to argparse subparser subp"""
    modules_parser = subp.add_parser(
        "modules",
        help="Lists modules of a course",
        description="Lists modules of a course. Output, CSV-format: "
        "'course, module name, module id, unlock at, require sequential progress, item count'",
    )
    modules_parser.set_defaults(func=modules_command)
    modules_parser.add_argument(
        "regex",
        default=".*",
        nargs="?",
        help="Regex for filtering modules, default: '.*'",
    )
    courses.add_course_option(modules_parser, required=True)
