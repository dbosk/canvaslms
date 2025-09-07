import os
import re
import subprocess
import sys
import tempfile
import canvaslms.cli.courses


def announce_command(config, canvas, args):
    """Posts announcements to matching courses"""

    # Get list of matching courses
    course_list = list(canvaslms.cli.courses.filter_courses(canvas, args.course))

    if not course_list:
        print(f"No courses found matching pattern: {args.course}", file=sys.stderr)
        sys.exit(1)

    # Get the message content
    if args.interactive:
        message = get_message_from_editor()
    elif args.message:
        message = args.message
    else:
        print(
            "Error: Either provide -m/--message or use -i/--interactive mode",
            file=sys.stderr,
        )
        sys.exit(1)

    if not message.strip():
        print("Error: Message cannot be empty", file=sys.stderr)
        sys.exit(1)

    # Show courses that will receive the announcement
    print(f"Will post announcement '{args.title}' to {len(course_list)} course(s):")
    for course in course_list:
        print(f"  - {course.course_code}: {course.name}")

    # Confirm before posting
    confirm = input("Continue? (y/N): ")
    if confirm.lower() not in ["y", "yes"]:
        print("Cancelled.")
        sys.exit(0)

    # Post announcements
    success_count = 0
    for course in course_list:
        try:
            discussion_topic = course.create_discussion_topic(
                title=args.title, message=message, is_announcement=True, published=True
            )
            success_count += 1
            print(f"✓ Posted to {course.course_code}: {course.name}")
        except Exception as e:
            print(
                f"✗ Failed to post to {course.course_code}: {course.name} - {str(e)}",
                file=sys.stderr,
            )

    print(f"Successfully posted to {success_count}/{len(course_list)} courses.")


def get_message_from_editor():
    """Opens the user's preferred editor to write the announcement message"""
    editor = os.environ.get("EDITOR", "nano")

    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".md", delete=False
    ) as temp_file:
        temp_file.write("# Write your announcement message here\n")
        temp_file.write("# Lines starting with # are comments and will be removed\n")
        temp_file.write("# You can use Markdown formatting\n\n")
        temp_file_path = temp_file.name

    try:
        # Open editor
        subprocess.run([editor, temp_file_path], check=True)

        # Read the content back
        with open(temp_file_path, "r") as temp_file:
            content = temp_file.read()

        # Remove comment lines and strip whitespace
        lines = []
        for line in content.split("\n"):
            if not line.strip().startswith("#"):
                lines.append(line)

        return "\n".join(lines).strip()

    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_file_path)
        except OSError:
            pass


def add_command(subp):
    """Adds the announce command to argparse parser"""
    announce_parser = subp.add_parser(
        "announce",
        help="Post announcements to courses",
        description="Post announcements to one or more courses matching a regex pattern. "
        "The announcement can be provided via command line or interactively using an editor.",
    )
    announce_parser.set_defaults(func=announce_command)
    announce_parser.add_argument("title", help="Title of the announcement")
    announce_parser.add_argument(
        "-c",
        "--course",
        required=True,
        help="Regex matching courses on title, course code or Canvas ID",
    )
    announce_parser.add_argument(
        "-m",
        "--message",
        help="Message content of the announcement (use -i for interactive mode)",
    )
    announce_parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        default=False,
        help="Interactive mode: open editor to write announcement message in Markdown",
    )
