# GitHub Copilot Instructions for canvaslms

## Project Overview

This is `canvaslms`, a command-line interface (CLI) tool for Canvas LMS that provides a POSIX-friendly interface for automating Canvas operations. The tool follows a Git-like subcommand structure and emphasizes scriptability and integration with shell pipelines.

## Architecture & Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Poetry**: Dependency management and packaging
- **Literate Programming**: Source code written in noweb (.nw) files
- **Canvas API**: Integration via `canvasapi` library

### Key Dependencies
- `canvasapi>=3.2.0`: Canvas LMS REST API client
- `argcomplete>=2,<4`: Bash completion support
- `rich>=13,<15`: Rich terminal output and formatting
- `pypandoc>=1.11`: Document conversion
- `appdirs>=1.4.4`: Platform-specific directory paths
- `keyring>=24.2,<26.0`: Secure credential storage
- `arrow>=1.2.3`: Date/time handling

## Code Structure & Patterns

### Directory Layout
```
src/canvaslms/
├── cli/           # CLI subcommand implementations (.nw files)
├── grades/        # Grading functionality (.nw files)
└── hacks/         # Canvas API extensions
```

### Literate Programming Approach
- Source code is written in noweb (.nw) files using literate programming
- Python files are generated from .nw files during build process
- Use `<<code_chunk>>` syntax for code organization
- Documentation and code are interleaved for better maintainability

### CLI Design Patterns
- **Subcommand Structure**: Each major functionality is a subcommand (login, users, assignments, etc.)
- **Module Pattern**: Each subcommand module must have an `add_command(subp)` function
- **POSIX Output**: Commands output tab-separated values suitable for shell pipelines
- **Configuration**: Uses `appdirs` for platform-specific config file locations

### Common Code Patterns

#### CLI Module Structure
```python
def add_command(subp):
    """Adds the subcommand to argparse parser subp"""
    parser = subp.add_parser("commandname", help="Description")
    # Add arguments
    parser.set_defaults(func=command_function)

def command_function(args):
    """Implementation of the command"""
    # Command logic here
```

#### Canvas API Usage
```python
import canvasapi
import canvaslms.cli.courses as courses

def get_canvas_and_course(args):
    """Standard pattern for getting Canvas instance and course"""
    canvas = Canvas(args.canvas_url, args.canvas_token)
    course = courses.get_course(canvas, args.course)
    return canvas, course
```

#### Output Formatting
- Use tab-separated values for structured output
- Use Rich library for human-readable formatting when appropriate
- Support both machine-readable and human-readable output modes

## Canvas LMS Domain Knowledge

### Key Concepts
- **Courses**: Container for assignments, users, and content
- **Assignments**: Tasks assigned to students, can be grouped
- **Users**: Students, teachers, and other course participants  
- **Submissions**: Student work submitted for assignments
- **Grades**: Scores and feedback for submissions
- **Assignment Groups**: Collections of related assignments

### API Patterns
- Most operations require course context
- Use pagination for large result sets
- Handle rate limiting appropriately
- Canvas IDs are integers, but often passed as strings

## Development Guidelines

### When Writing Code
1. **Follow existing patterns**: Look at existing subcommands for structure
2. **POSIX compatibility**: Ensure output works well with Unix tools
3. **Error handling**: Provide clear error messages for common failures
4. **Documentation**: Include docstrings and inline comments for complex logic
5. **Testing**: Consider edge cases like missing courses, invalid IDs, etc.

### Naming Conventions
- Use snake_case for Python functions and variables
- CLI commands use lowercase with hyphens (e.g., `canvas-lms`)
- Module names match their primary command

### Canvas API Best Practices
- Always validate course and assignment IDs
- Handle missing resources gracefully
- Use Canvas API pagination for large datasets
- Cache course and user lookups when appropriate

## Build System

The project uses a Make-based build system:
- `make compile`: Generate Python files from .nw sources
- `make install`: Install the package locally
- `poetry build`: Create distribution packages

Generated Python files should not be edited directly - modify the .nw sources instead.

## Common Tasks

### Adding a New Subcommand
1. Create a new .nw file in `src/canvaslms/cli/`
2. Implement the `add_command(subp)` function
3. Add the module import to cli.nw
4. Follow existing patterns for argument parsing and Canvas API usage

### Canvas Data Retrieval
- Use course.get_assignments() for assignment lists
- Use course.get_users() for user lists  
- Use assignment.get_submissions() for submission data
- Always handle API exceptions and rate limits