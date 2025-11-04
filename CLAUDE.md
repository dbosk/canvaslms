# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`canvaslms` is a command-line interface for Canvas LMS that provides POSIX-friendly, scriptable access to Canvas operations. It follows a Git-like subcommand structure and emphasizes integration with shell pipelines.

## Literate Programming Architecture

**CRITICAL**: This project uses literate programming with noweb. Source code is written in `.nw` files that combine documentation and code.

- **Never edit `.py` files directly** - they are generated from `.nw` sources
- To modify code, edit the corresponding `.nw` file in the same directory
- Python files are regenerated during the build process
- Use `<<code_chunk>>` syntax for code organization in `.nw` files

## Build System

### Core Build Commands

```bash
# Generate Python files from .nw sources and build package
make all           # Runs compile + generates doc/canvaslms.pdf

# Generate Python from .nw sources only
make compile       # Tangles .nw files and runs poetry build

# Install locally for development
make install       # Installs with pip -e and sets up bash completion

# Clean generated files
make distclean     # Removes build/, dist/, *.egg-info
```

### Module-level Builds

Each module directory (`src/canvaslms/cli/`, `src/canvaslms/grades/`) has its own Makefile:

```bash
# Regenerate Python from .nw in a specific module
cd src/canvaslms/cli
make all           # Generates all .py and .tex files from .nw sources
make clean         # Removes generated files
```

### Build System Details

- Uses Make with custom makefiles from `makefiles/` directory
- `noweb.mk` provides suffix rules for weaving (.nw → .tex) and tangling (.nw → .py)
- Each module's Makefile lists files in `MODULES` variable
- `cli/__init__.py` is generated from `cli.nw` via intermediate `cli.py`

## Code Structure

### Directory Layout

```
src/canvaslms/
├── cli/              # CLI subcommands (.nw sources)
│   ├── cli.nw        # Main entry point (generates __init__.py)
│   ├── login.nw      # Authentication
│   ├── courses.nw    # Course management
│   ├── users.nw      # User listing
│   ├── assignments.nw
│   ├── submissions.nw
│   ├── grade.nw      # Grading functionality
│   ├── results.nw    # Results processing
│   ├── calendar.nw   # Calendar events
│   ├── discussions.nw # Discussion boards
│   ├── quizzes.nw    # Quiz/survey analysis
│   ├── fbf.nw        # Feedback functionality
│   └── utils.nw      # Shared utilities
├── grades/           # Grading algorithms (.nw sources)
└── hacks/            # Canvas API extensions
```

### CLI Module Pattern

Every CLI subcommand module follows this pattern:

```python
def add_command(subp):
    """Adds the subcommand to argparse parser subp"""
    parser = subp.add_parser("commandname", help="Description")
    # Add arguments
    parser.set_defaults(func=command_function)

def command_function(config, canvas, args):
    """Implementation receives config dict, Canvas API instance, and args"""
    # Command logic here
```

### Shared Utility Pattern

Modules provide reusable functions for adding options and processing them:

```python
# Pattern used by courses.py, assignments.py, etc.
def add_XXX_option(parser, required=False):
    """Adds -X option to parser"""
    parser.add_argument("-X", "--xxx", ...)

def process_XXX_option(canvas, args):
    """Processes -X option, returns filtered list"""
    # Returns list or raises EmptyListError
```

This enables consistent option handling across commands (e.g., `add_course_option()` + `process_course_option()`).

## Adding a New Subcommand

1. Create `src/canvaslms/cli/newcommand.nw` with literate programming structure
2. Implement `add_command(subp)` and command function(s)
3. Add to `src/canvaslms/cli/Makefile` in `MODULES` variable:
   ```makefile
   MODULES+= newcommand.py newcommand.tex
   ```
4. Import and register in `cli.nw`:
   ```python
   import canvaslms.cli.newcommand
   # ... in main():
   canvaslms.cli.newcommand.add_command(subp)
   ```
5. Run `make all` from project root to regenerate Python files

## Configuration and Authentication

- Config stored in platform-specific location via `appdirs` (usually `~/.config/canvaslms/config.json`)
- Credentials stored securely via `keyring` library
- Environment variables: `CANVAS_SERVER`, `CANVAS_TOKEN` override config
- First-time setup: `canvaslms login`

## Canvas API Integration

### Core Patterns

```python
import canvaslms.cli.courses as courses
import canvaslms.cli.assignments as assignments

def example_command(config, canvas, args):
    # canvas is pre-initialized Canvas API instance
    course_list = courses.process_course_option(canvas, args)

    for course in course_list:
        assignments_list = assignments.filter_assignments(course, args.assignment)
        # Process assignments...
```

### API Objects Hierarchy

- `canvas.get_courses()` → Course objects
- `course.get_assignments()` → Assignment objects
- `course.get_users()` → User objects
- `assignment.get_submissions()` → Submission objects

### Error Handling

- Raise `canvaslms.cli.EmptyListError` when no results match filters
- Main CLI catches this and exits with code 1 (suppressed if `-q/--quiet`)

## Output Conventions

- Default: tab-separated values (TSV) for Unix pipeline compatibility
- Use `csv.writer` with `args.delimiter` for structured output
- Rich library for human-readable formatting (see `quizzes.py`)
- Support both machine-readable and human-readable modes where appropriate

## Dependencies

### Core Runtime
- Python 3.8+
- `canvasapi>=3.3.0` - Canvas LMS API client
- `argcomplete>=2,<4` - Bash completion
- `rich>=13,<15` - Terminal formatting
- `pypandoc>=1.11` - Document conversion
- `arrow>=1.2.3` - Date/time handling
- `keyring>=24.2,<26.0` - Credential storage

### Optional
- `canvaslms[llm]` - AI summaries for quiz analysis (Python 3.9+)
- `pandoc` - System package required by some subcommands

## Testing and Development

### Running Commands for Testing

- Use `poetry run canvaslms <subcommand>` to test commands in the Poetry environment
- This ensures you're testing against the current development version with all dependencies
- Example: `poetry run canvaslms quizzes analyse -c <course> -a <assignment>`

### Development Workflow

- No pytest framework currently in place
- Use `make install` for local development with editable install (requires sudo for bash completion)
- Poetry manages dependencies and builds
- Use `pdbpp` for debugging (included in dev dependencies)

## GitHub Copilot Context

This repository includes:
- `.github/copilot-instructions.md` - Detailed project context and patterns
- `.copilotignore` - Files excluded from Copilot context

Key principles from Copilot instructions:
- Follow literate programming conventions
- Maintain POSIX-compatible output
- Use existing module patterns for consistency
- Document complex logic in TeX portion of `.nw` files
