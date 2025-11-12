# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`canvaslms` is a command-line interface for Canvas LMS that provides POSIX-friendly, scriptable access to Canvas operations. It follows a Git-like subcommand structure and emphasizes integration with shell pipelines.

## Literate Programming Architecture

**CRITICAL**: This project uses literate programming with noweb. Source code is written in `.nw` files that combine documentation and code.

### Core Principles

This project follows Donald Knuth's literate programming philosophy:
- **Explain to humans what we want computers to do** - Write for human readers, not compilers
- **Present concepts in pedagogical order** - Organize by best learning sequence, not execution order
- **Document the "why" not just the "what"** - Explain design decisions, trade-offs, and rationale

The literate source (`.nw` files) is the single source of truth. Generated Python files are build artifacts.

### Essential Rules

**ALWAYS** activate the `literate-programming` skill BEFORE editing any `.nw` file:
```
User: "Can you fix the bug in assignments.nw?"
You: [Activate literate-programming skill FIRST, then proceed]
```

**NEVER** edit `.py` files directly - they are generated from `.nw` sources and will be overwritten.

### Workflow for Modifying .nw Files

1. **Activate skill**: Use the `literate-programming` skill command
2. **Read the file**: Understand the current narrative and structure
3. **Plan changes**: Consider pedagogical order and narrative flow
4. **Write documentation first**: Explain the problem, approach, and design decisions
5. **Write code chunks**: Create well-named chunks that support the narrative
6. **Regenerate**: Run `make` to tangle .nw → .py

### Chunk Naming Conventions

Chunk names should be meaningful and describe purpose (like pseudocode), not syntax:

**Good chunk names** (what/why):
- `<<process user options>>`
- `<<filter submissions by group>>`
- `<<compute speedgrader URL>>`

**Bad chunk names** (syntactic):
- `<<for loop>>`
- `<<function definition>>`
- `<<if statement>>`

Chunk names should be 2-5 words summarizing the chunk's purpose.

### Writing Style

This project uses **variation theory** to structure explanations:
- **Contrast**: Show different approaches, explain why one was chosen
- **Separation**: Present the whole first, then decompose into parts
- **Generalization**: Show patterns across similar code
- **Fusion**: Bring parts back together to show the complete picture

Example structure:
```noweb
\section{The submissions command}

We want to list submissions for assignments. This requires:
\begin{itemize}
\item Getting the assignment list
\item Fetching submissions for each assignment
\item Filtering by user/group if specified
\item Formatting the output
\end{itemize}

<<submission command>>=
def submission_command(config, canvas, args):
    assignment_list = <<get assignments>>
    submissions = <<get submissions for assignments>>
    <<filter submissions if needed>>
    <<format and print output>>
@

\subsection{Getting submissions}

Canvas provides two APIs: one for all submissions, one for ungraded only.
We use the ungraded API when the user specifies --ungraded to reduce load.

<<get submissions for assignments>>=
if args.ungraded:
    submissions = list_ungraded_submissions(assignment_list)
else:
    submissions = list_submissions(assignment_list)
@
```

### Quality Checklist for Literate Programs

When writing or reviewing `.nw` files, ensure:

**Narrative Quality:**
- [ ] Introduction explains the problem and motivation
- [ ] Design decisions are explained with rationale
- [ ] Concepts are presented in pedagogical order (not execution order)
- [ ] The "why" is documented, not just the "what"
- [ ] Complex algorithms have worked examples
- [ ] Trade-offs between alternatives are discussed
- [ ] Edge cases and limitations are documented

**Code Organization:**
- [ ] Chunk names are meaningful and describe purpose
- [ ] Each chunk represents a single coherent concept
- [ ] Chunks are appropriately sized (not too large or small)
- [ ] Helper functions are used instead of excessive chunk decomposition
- [ ] Code references use `[[code]]` notation properly
- [ ] No unused chunks (verify with `noroots`)

**Technical Quality:**
- [ ] Code is correct and follows project patterns
- [ ] Generated Python follows project style (use `black` formatter)
- [ ] Documentation uses proper LaTeX formatting
- [ ] Cross-references and labels are used where helpful
- [ ] Margin notes credit sources where applicable

**Project-Specific:**
- [ ] CLI commands follow the `add_command()` pattern
- [ ] Utility functions follow the `add_XXX_option()` / `process_XXX_option()` pattern
- [ ] Error handling uses `EmptyListError` appropriately
- [ ] Output follows TSV conventions or uses `csv.writer`

### Common Patterns in This Project

**Section structure for CLI commands:**
```noweb
\section{The [[command]] subcommand}

<<explanation of what the command does>>

<<command.py>>=
import canvaslms.cli.module
<<imports>>
<<functions>>

def add_command(subp):
    <<add command to subp>>

def command_function(config, canvas, args):
    <<implementation>>
@
```

**Processing options pattern:**
```noweb
\subsection{The [[-X]] option}

<<explanation of what the option does and why>>

<<functions>>=
def add_XXX_option(parser, required=False):
    """Adds -X option to parser"""
    parser.add_argument("-X", "--xxx", <<arguments>>)

def process_XXX_option(canvas, args):
    """Processes -X option, returns filtered list"""
    <<get items from canvas>>
    <<filter based on args>>
    return filtered_list
@
```

**Error handling pattern:**
```noweb
If no results match the criteria, we raise [[EmptyListError]].
The main CLI catches this and exits gracefully.

<<check for empty results>>=
if not result_list:
    raise canvaslms.cli.EmptyListError("No items found matching criteria")
@
```

### Reviewing Existing Literate Programs

When asked to review literate quality of a `.nw` file, evaluate:

1. **Pedagogical Order**: Could a newcomer understand this by reading start to finish?
2. **Motivation**: Is it clear why this code exists and why it's designed this way?
3. **Narrative Flow**: Does the prose tell a coherent story?
4. **Chunk Quality**: Are chunks well-named, appropriately sized, and focused?
5. **Completeness**: Are design decisions, trade-offs, and limitations documented?
6. **Examples**: Are there concrete examples showing the code in action?
7. **Variation Theory**: Are contrasts used to highlight key concepts?

Provide specific, actionable improvements with rationale.

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

When adding a new CLI subcommand, follow these steps with literate programming principles:

### 1. Activate the literate-programming skill

Before creating the `.nw` file, activate the skill to ensure proper guidance.

### 2. Plan the narrative structure

Before writing any code, outline:
- **What problem does this command solve?** (motivation)
- **What design decisions are involved?** (rationale)
- **What are the key concepts?** (pedagogical order)
- **What examples illustrate the usage?** (concrete instances)

### 3. Create the .nw file with documentation first

Create `src/canvaslms/cli/newcommand.nw` following this structure:

```noweb
\chapter{The [[newcommand]] command}

<<introduction explaining what the command does and why>>

\section{Command overview}

<<high-level explanation of the approach>>

<<newcommand.py>>=
import canvasapi
import canvaslms.cli
<<additional imports>>

<<functions>>

def add_command(subp):
    """Adds newcommand to argparse parser subp"""
    <<add command to subp>>

def newcommand_function(config, canvas, args):
    """Implementation of newcommand"""
    <<process options>>
    <<main logic>>
    <<format and output results>>
@

\section{Command-line options}

<<explain each option and why it's needed>>

\section{Implementation}

<<explain the algorithm, design decisions, edge cases>>
```

### 4. Write code chunks that support the narrative

- Use meaningful chunk names that describe purpose
- Decompose by concept, not syntax
- Explain the "why" in prose, not in code comments
- Follow project patterns (`add_command()`, `process_XXX_option()`)

### 5. Integrate into the build system

Add to `src/canvaslms/cli/Makefile`:
```makefile
MODULES+= newcommand.py newcommand.tex
```

### 6. Register the command

Import and register in `cli.nw`:
```python
import canvaslms.cli.newcommand
# ... in main():
canvaslms.cli.newcommand.add_command(subp)
```

### 7. Build and test

```bash
cd src/canvaslms/cli
make all                    # Generate .py and .tex
cd ../../..
make install                # Install for testing
canvaslms newcommand --help # Verify it works
```

### 8. Review literate quality

Before considering the task complete, verify:
- [ ] Documentation explains "why" not just "what"
- [ ] Concepts are in pedagogical order
- [ ] Chunk names are meaningful
- [ ] Design decisions are documented
- [ ] Examples are provided
- [ ] Edge cases are discussed

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

- No pytest framework currently in place
- Use `make install` for local development with editable install
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
