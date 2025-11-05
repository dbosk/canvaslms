import argparse
import canvasapi
import canvaslms.cli.courses as courses
import csv
import re
import sys


def modules_list_command(config, canvas, args):
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

            sequential = (
                module.require_sequential_progress
                if hasattr(module, "require_sequential_progress")
                else False
            )
            progress_mode = "sequential" if sequential else "any-order"

            output.writerow(
                [
                    course.course_code,
                    module.name,
                    module.unlock_at if hasattr(module, "unlock_at") else None,
                    progress_mode,
                    item_count,
                ]
            )


def modules_show_command(config, canvas, args):
    output = csv.writer(sys.stdout, delimiter=args.delimiter)
    course_list = courses.process_course_option(canvas, args)

    for course in course_list:
        modules = filter_modules(course, args.regex)
        for module in modules:
            try:
                items = list(module.get_module_items())
                if not items:
                    # Show module even if it has no items
                    row = [course.course_code, module.name, "No items", ""]
                    if args.show_id:
                        row.append("")
                    row.append("")
                    output.writerow(row)
                else:
                    for item in items:
                        completion_req = ""
                        if (
                            hasattr(item, "completion_requirement")
                            and item.completion_requirement
                        ):
                            req = item.completion_requirement
                            if "type" in req:
                                completion_req = req["type"]
                                if "min_score" in req:
                                    completion_req += (
                                        f" (min score: {req['min_score']})"
                                    )
                        row = [
                            course.course_code,
                            module.name,
                            item.type if hasattr(item, "type") else "Unknown",
                            item.title if hasattr(item, "title") else "No title",
                        ]

                        if args.show_id:
                            row.append(
                                item.content_id
                                if hasattr(item, "content_id")
                                else item.id if hasattr(item, "id") else ""
                            )

                        row.append(completion_req)
                        output.writerow(row)
            except:
                # If we can't get items, show the module with error
                row = [course.course_code, module.name, "Error loading items", ""]
                if args.show_id:
                    row.append("")
                row.append("")
                output.writerow(row)


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


def filter_assignments_by_module_list(modules, assignments):
    """Returns elements in assignments that belong to any of the modules.
    Used for AND filtering with other criteria."""
    # Collect all assignment IDs from all modules
    all_assignment_ids = set()
    for module in modules:
        try:
            for item in module.get_module_items():
                if hasattr(item, "type") and item.type == "Assignment":
                    all_assignment_ids.add(item.content_id)
        except AttributeError:
            pass

    for assignment in assignments:
        if assignment.id in all_assignment_ids:
            yield assignment


def add_command(subp):
    """Adds the subcommand and its options to argparse subparser subp"""
    modules_parser = subp.add_parser("modules", help="Work with Canvas modules")
    modules_subp = modules_parser.add_subparsers(
        dest="modules_command", help="Available module commands"
    )

    # Add 'list' subcommand
    list_parser = modules_subp.add_parser(
        "list",
        help="Lists modules of a course",
        description="Lists modules of a course. Output: course, module name, unlock at, require sequential progress, item count",
    )
    list_parser.set_defaults(func=modules_list_command)
    list_parser.add_argument(
        "regex",
        default=".*",
        nargs="?",
        help="Regex for filtering modules, default: '.*'",
    )
    courses.add_course_option(list_parser, required=True)

    # Add 'show' subcommand
    show_parser = modules_subp.add_parser(
        "show",
        help="Shows modules and their contents",
        description="Shows modules and their contents. Output: course, module name, item type, item name, [item id], completion requirement",
    )
    show_parser.set_defaults(func=modules_show_command)
    show_parser.add_argument(
        "regex",
        default=".*",
        nargs="?",
        help="Regex for filtering modules, default: '.*'",
    )
    courses.add_course_option(show_parser, required=True)
    show_parser.add_argument(
        "--show-id", action="store_true", help="Include Canvas IDs in output"
    )
