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
    print("Error: Either provide -m/--message or use -i/--interactive mode", file=sys.stderr)
    sys.exit(1)
  
  if not message.strip():
    print("Error: Message cannot be empty", file=sys.stderr)
    sys.exit(1)
  
  # Show courses that will receive the announcement
  print(f"Will post announcement '{args.title}' to {len(course_list)} course(s):", file=sys.stderr)
  for course in course_list:
    print(f"  - {course.course_code}: {course.name}", file=sys.stderr)
  
  # Confirm before posting
  confirm = input("Continue? (y/N): ")
  if confirm.lower() not in ['y', 'yes']:
    print("Cancelled.", file=sys.stderr)
    sys.exit(0)
  
  # Post announcements
  success_count = 0
  failed_count = 0
  for course in course_list:
    try:
      discussion_topic = course.create_discussion_topic(
        title=args.title,
        message=message,
        is_announcement=True,
        published=True
      )
      success_count += 1
    except Exception as e:
      print(f"Failed to post to {course.course_code}: {course.name} - {str(e)}", file=sys.stderr)
      failed_count += 1
  
  # Only output result if there were failures
  if failed_count > 0:
    print(f"Posted to {success_count}/{len(course_list)} courses.", file=sys.stderr)
    sys.exit(1)
def list_command(config, canvas, args):
  """Lists discussions or announcements from matching courses"""
  
  # Get list of matching courses
  course_list = list(canvaslms.cli.courses.filter_courses(canvas, args.course))
  
  if not course_list:
    print(f"No courses found matching pattern: {args.course}", file=sys.stderr)
    sys.exit(1)
  
  # List discussions/announcements for each course
  for course in course_list:
    try:
      if args.type == "announcements":
        announcements = course.get_discussion_topics(only_announcements=True)
        for announcement in announcements:
          # Output in tab-delimited format for UNIX tools
          print(f"{course.course_code}\t{announcement.id}\t{announcement.title}\t{announcement.created_at}")
      else:  # discussions
        discussions = course.get_discussion_topics()
        for discussion in discussions:
          # Skip announcements when listing discussions
          if not getattr(discussion, 'is_announcement', False):
            # Output in tab-delimited format for UNIX tools
            print(f"{course.course_code}\t{discussion.id}\t{discussion.title}\t{discussion.created_at}")
    except Exception as e:
      print(f"Error accessing {course.course_code}: {str(e)}", file=sys.stderr)
      sys.exit(1)
def get_message_from_editor():
  """Opens the user's preferred editor to write the announcement message"""
  editor = os.environ.get('EDITOR', 'nano')
  
  with tempfile.NamedTemporaryFile(mode='w+', suffix='.md', delete=False) as temp_file:
    temp_file.write("# Write your announcement message here\n")
    temp_file.write("# Lines starting with # are comments and will be removed\n")
    temp_file.write("# You can use Markdown formatting\n\n")
    temp_file_path = temp_file.name
  
  try:
    # Open editor
    subprocess.run([editor, temp_file_path], check=True)
    
    # Read the content back
    with open(temp_file_path, 'r') as temp_file:
      content = temp_file.read()
    
    # Remove comment lines and strip whitespace
    lines = []
    for line in content.split('\n'):
      if not line.strip().startswith('#'):
        lines.append(line)
    
    return '\n'.join(lines).strip()
    
  finally:
    # Clean up temporary file
    try:
      os.unlink(temp_file_path)
    except OSError:
      pass

def add_command(subp):
  """Adds the discussions command with subcommands to argparse parser"""
  discussions_parser = subp.add_parser("discussions",
    help="Manage course discussions and announcements",
    description="Manage discussions and announcements in Canvas courses.")
  
  discussions_subp = discussions_parser.add_subparsers(
    title="discussions commands",
    dest="discussions_command",
    required=True)
  
  add_announce_command(discussions_subp)
  add_list_command(discussions_subp)

def add_announce_command(subp):
  """Adds the announce subcommand"""
  announce_parser = subp.add_parser("announce",
    help="Post announcements to courses",
    description="Post announcements to one or more courses matching a regex pattern. "
                "The announcement can be provided via command line or interactively using an editor.")
  announce_parser.set_defaults(func=announce_command)
  announce_parser.add_argument("title",
    help="Title of the announcement")
  announce_parser.add_argument("-c", "--course", required=True,
    help="Regex matching courses on title, course code or Canvas ID")
  announce_parser.add_argument("-m", "--message",
    help="Message content of the announcement (use -i for interactive mode)")
  announce_parser.add_argument("-i", "--interactive",
    action="store_true", default=False,
    help="Interactive mode: open editor to write announcement message in Markdown")

def add_list_command(subp):
  """Adds the list subcommand"""
  list_parser = subp.add_parser("list",
    help="List discussions and announcements",
    description="List discussions or announcements from courses.")
  list_parser.set_defaults(func=list_command)
  list_parser.add_argument("type",
    choices=["announcements", "discussions"],
    help="Type of content to list")
  list_parser.add_argument("-c", "--course", required=True,
    help="Regex matching courses on title, course code or Canvas ID")
