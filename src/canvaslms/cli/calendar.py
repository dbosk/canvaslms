import argparse
import canvasapi.exceptions
import canvaslms.cli
import canvaslms.cli.courses as courses
import csv
import datetime
import sys
import arrow


def add_calendar_list_command(subp):
    """Adds the calendar list subcommand and its options to argparse subparser subp"""
    calendar_list_parser = subp.add_parser(
        "calendar-list",
        help="Lists calendar events",
        description="Lists calendar events. Output, CSV-format: "
        "<event-id> <title> <start-time> <end-time> <context-type> <context-name>",
    )
    calendar_list_parser.set_defaults(func=calendar_list_command)
    courses.add_course_option(calendar_list_parser)
    calendar_list_parser.add_argument(
        "--start-date", help="Start date for event filter (YYYY-MM-DD format)"
    )
    calendar_list_parser.add_argument(
        "--end-date", help="End date for event filter (YYYY-MM-DD format)"
    )
    calendar_list_parser.add_argument(
        "--type", choices=["event", "assignment"], help="Filter by event type"
    )


def calendar_list_command(config, canvas, args):
    """Lists calendar events in CSV format to stdout"""
    output = csv.writer(sys.stdout, delimiter=args.delimiter)

    context_codes = []
    if hasattr(args, "course") and args.course:
        course_list = courses.process_course_option(canvas, args)
        context_codes = [f"course_{course.id}" for course in course_list]
    try:
        # Prepare parameters for API call
        params = {}
        if context_codes:
            params["context_codes"] = context_codes
        if args.start_date:
            params["start_date"] = args.start_date
        if args.end_date:
            params["end_date"] = args.end_date
        if args.type:
            params["type"] = args.type

        events = canvas.get_calendar_events(**params)

        for event in events:
            # Get context information
            context_type = getattr(event, "context_type", "")
            context_name = getattr(event, "context_name", "")

            # Format dates
            start_at = getattr(event, "start_at", "")
            end_at = getattr(event, "end_at", "")

            row = [
                getattr(event, "id", ""),
                getattr(event, "title", ""),
                start_at,
                end_at,
                context_type,
                context_name,
            ]
            output.writerow(row)

    except canvasapi.exceptions.CanvasException as e:
        canvaslms.cli.err(1, f"Failed to get calendar events: {e}")


def add_calendar_show_command(subp):
    """Adds the calendar show subcommand and its options to argparse subparser subp"""
    calendar_show_parser = subp.add_parser(
        "calendar-show",
        help="Shows details of a specific calendar event",
        description="Shows details of a specific calendar event",
    )
    calendar_show_parser.set_defaults(func=calendar_show_command)
    calendar_show_parser.add_argument(
        "event_id", help="The ID of the calendar event to show"
    )


def calendar_show_command(config, canvas, args):
    """Shows details of a specific calendar event"""
    try:
        event = canvas.get_calendar_event(args.event_id)

        print(f"Event ID: {event.id}")
        print(f"Title: {getattr(event, 'title', 'N/A')}")
        print(f"Description: {getattr(event, 'description', 'N/A')}")
        print(f"Start: {getattr(event, 'start_at', 'N/A')}")
        print(f"End: {getattr(event, 'end_at', 'N/A')}")
        print(f"Location: {getattr(event, 'location_name', 'N/A')}")
        print(
            f"Context: {getattr(event, 'context_type', 'N/A')} - {getattr(event, 'context_name', 'N/A')}"
        )
        print(f"URL: {getattr(event, 'html_url', 'N/A')}")

    except canvasapi.exceptions.CanvasException as e:
        canvaslms.cli.err(1, f"Failed to get calendar event: {e}")


def add_calendar_create_command(subp):
    """Adds the calendar create subcommand and its options to argparse subparser subp"""
    calendar_create_parser = subp.add_parser(
        "calendar-create",
        help="Creates a new calendar event",
        description="Creates a new calendar event",
    )
    calendar_create_parser.set_defaults(func=calendar_create_command)
    courses.add_course_option(calendar_create_parser)
    calendar_create_parser.add_argument("title", help="Title of the calendar event")
    calendar_create_parser.add_argument(
        "--start-time",
        required=True,
        help="Start time (ISO format: YYYY-MM-DDTHH:MM:SS)",
    )
    calendar_create_parser.add_argument(
        "--end-time", help="End time (ISO format: YYYY-MM-DDTHH:MM:SS)"
    )
    calendar_create_parser.add_argument(
        "--description", help="Description of the event"
    )
    calendar_create_parser.add_argument("--location", help="Location of the event")


def calendar_create_command(config, canvas, args):
    """Creates a new calendar event"""
    try:
        # Prepare event parameters
        params = {
            "calendar_event": {
                "title": args.title,
                "start_at": args.start_time,
            }
        }

        if args.end_time:
            params["calendar_event"]["end_at"] = args.end_time
        if args.description:
            params["calendar_event"]["description"] = args.description
        if args.location:
            params["calendar_event"]["location_name"] = args.location

        # Set context if course is specified
        if hasattr(args, "course") and args.course:
            course_list = courses.process_course_option(canvas, args)
            if course_list:
                course = list(course_list)[0]  # Use first course if multiple
                params["calendar_event"]["context_code"] = f"course_{course.id}"

        event = canvas.create_calendar_event(**params)

        print(f"Created calendar event with ID: {event.id}")
        print(f"Title: {event.title}")
        print(f"Start: {getattr(event, 'start_at', 'N/A')}")
        if hasattr(event, "end_at") and event.end_at:
            print(f"End: {event.end_at}")

    except canvasapi.exceptions.CanvasException as e:
        canvaslms.cli.err(1, f"Failed to create calendar event: {e}")


def add_command(subp):
    """Adds the calendar subcommands to argparse subparser subp"""
    add_calendar_list_command(subp)
    add_calendar_show_command(subp)
    add_calendar_create_command(subp)
