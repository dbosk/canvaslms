# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`canvaslms` is a command-line interface for Canvas LMS that provides POSIX-friendly, scriptable access to Canvas operations. It follows a Git-like subcommand structure and emphasizes integration with shell pipelines.

## Literate Programming Architecture

**CRITICAL**: This project uses literate programming with noweb. Source code is written in `.nw` files that combine documentation and code.

### Essential Literate Programming Workflow

**When working with .nw files, ALWAYS follow these steps:**

#### ✅ CORRECT Workflow

**The correct order is:**
```
1. User asks to modify a .nw file
2. Read the existing .nw file to understand structure
3. Plan the changes with literate programming principles
4. Make the changes following the principles below
5. Regenerate code with make/notangle
```

**When to apply these practices:**
- Creating a new .nw file
- Editing an existing .nw file
- Reviewing any .nw file
- User asks to modify anything in a .nw file
- You notice a file has a .nw extension

#### ❌ INCORRECT Workflow (Anti-pattern)

**NEVER do this:**
```
1. User asks to modify a .nw file
2. You directly edit the .nw file without planning
3. User asks you to review literate quality
4. You find problems with the narrative
5. You have to redo everything
```

#### Critical Reminder

- .nw files are NOT regular source code files
- They are literate programs combining documentation and code
- Literate quality is AS IMPORTANT as code correctness
- Bad literate quality = failed task, even if code works
- ALWAYS think: "Is this a .nw file? Then follow literate programming practices!"

### Planning Changes to Literate Programs

**When you work on changes to a .nw file, follow this process:**

1. **Read the existing .nw file** to understand the current structure and narrative
2. **Plan the changes with literate programming in mind:**
   - What is the "why" behind this change? (Explain in documentation)
   - How does this fit into the existing narrative?
   - Should I use contrast to explain the change? (old vs new approach)
   - What new chunks are needed? What are their meaningful names?
   - Where in the pedagogical order should this be explained?
3. **Design the documentation BEFORE writing code:**
   - Write prose explaining the problem and solution
   - Use subsections to structure complex explanations
   - Provide examples showing the new behavior
   - Explain design decisions and trade-offs
4. **Decompose code into well-named chunks:**
   - Each chunk = one coherent concept
   - Names describe purpose (like pseudocode), not syntax
   - Use the web structure effectively
5. **Write the code chunks referenced in documentation**
6. **Regenerate and test**

**Key principle:** If you find yourself writing code comments to explain logic, that explanation belongs in the TeX/documentation chunks instead!

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

### Chunk Concatenation Patterns

Noweb allows multiple definitions of the same chunk name - they are concatenated in order of appearance. This feature can be used pedagogically to introduce concepts incrementally, but requires careful consideration of scope and context.

#### When to Use Multiple Definitions (Pedagogical Building)

**Use multiple definitions** when building up a parameter list or configuration as you introduce each concept:

```noweb
\subsection{Adding the diff flag}
We introduce a [[--diff]] flag to show differences between versions.
<<args for diff option>>=
diff=args.diff,
@

[... 300 lines later ...]

\subsection{Fine-tuning diff matching with thresholds}
To handle edge cases in file matching, we add threshold parameters.
<<args for diff option>>=
diff_threshold_fixed=args.diff_threshold_fixed,
diff_threshold_percent=args.diff_threshold_percent
@
```

**Result:** When `<<args for diff option>>` is used, it expands to all three parameters. This pedagogical pattern:
- Introduces each concept at its natural point in the narrative
- Builds understanding incrementally
- Uses noweb's concatenation feature intentionally
- Makes the document more readable by not front-loading all parameters

**When this works well:**
- Parameters are being added to the same logical concept
- All uses of the chunk occur in the **same scope** (all have access to `args`)
- The incremental introduction aids understanding
- The chunk represents a single conceptual unit being built up over time

#### When to Use Separate Chunks (Different Contexts)

**Use separate chunks** when the same parameters must be passed in different scopes:

```noweb
\subsection{Calling format\_submission from main}
The command function has access to [[args]]:
<<args for diff option>>=
diff=args.diff,
diff_threshold_fixed=args.diff_threshold_fixed,
diff_threshold_percent=args.diff_threshold_percent
@

\subsection{Recursive calls inside format\_submission}
Inside [[format_submission]], we don't have [[args]]---only parameters.
We need a separate chunk to pass these through:
<<diff params>>=
diff=diff,
diff_threshold_fixed=diff_threshold_fixed,
diff_threshold_percent=diff_threshold_percent
@
```

**Result:** Two distinct chunks for different scoping contexts. This pattern:
- Makes scope explicit through chunk naming
- Prevents `NameError` when `args` doesn't exist
- Clearly distinguishes external calls from internal recursion
- Improves code maintainability by making context visible

**When you need separate chunks:**
- The same logical parameters must be passed in **different scopes**
- One context has `args` object, another has only parameters
- External calls vs internal recursive calls
- Command-line processing vs function implementation

#### Guidelines for Choosing

Ask these questions:

1. **Same scope?**
   - Yes → Consider concatenation for pedagogical building
   - No → Use separate chunks with descriptive names

2. **Same conceptual unit?**
   - Yes, building up one concept → Concatenation may be appropriate
   - No, different purposes → Separate chunks

3. **Will readers be confused?**
   - If a reader at the first definition won't know there's a second → Add forward reference
   - If scope differences aren't obvious → Use separate chunks with clear names

#### Anti-Pattern: Confusing Concatenation

**Bad:** Using concatenation when contexts differ, causing scope errors:

```noweb
<<args for diff option>>=
diff=args.diff,
@

# Used both in command function AND inside format_submission
# This causes NameError inside format_submission where args doesn't exist!
```

**Good:** Recognize different contexts and use separate chunks:

```noweb
<<args for diff option>>=  # For command function (has args)
diff=args.diff,
@

<<diff params>>=  # For internal calls (no args)
diff=diff,
@
```

#### Best Practices

1. **Document concatenation intent**: If using multiple definitions, mention it in the prose (e.g., "we'll extend this chunk later")
2. **Use forward references**: If split is large, note "see Section X.Y for threshold parameters"
3. **Check for scope issues**: Before reusing a chunk name, verify all usage sites have access to the same variables
4. **Prefer separate chunks when in doubt**: Clear, explicit chunk names beat clever reuse
5. **Name chunks for context**: `<<args for X>>` vs `<<X params>>` makes scope immediately visible

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

### Organizing Tests in Literate Programs

When embedding tests in literate programs (common for modules using pytest, unittest, etc.), follow these principles to maintain pedagogical clarity:

#### Test Placement: After Implementation, Not Before

**CRITICAL PRINCIPLE:** Tests should appear AFTER the functionality they verify, not before.

**Pedagogical flow:**
1. **Explain** the problem and approach
2. **Implement** the solution
3. **Verify** it works with tests

This ordering allows readers to:
- Understand what's being built before seeing verification
- See tests as proof/validation rather than mysterious code
- Follow a natural learning progression

#### Pattern: Distributed Test Organization

**DO NOT** group all tests at the beginning of the file. Instead, distribute tests throughout the document, placing each test section immediately after its corresponding implementation.

**Example structure:**
```noweb
\section{Feature Implementation}

We need to implement feature X...

<<implementation>>=
def feature_x():
    # implementation code
@

Now let's verify this works correctly...

<<test feature>>=
def test_feature_x():
    assert feature_x() == expected
@
```

#### Main Test File Structure Pattern

Define the main test file structure early (imports, test file skeleton), then reference test chunks defined later:

```noweb
\section{Testing Overview}

Tests are distributed throughout this document, appearing after
each implementation section.

<<test module.py>>=
"""Tests for module functionality"""
import pytest
from module import feature_a, feature_b

<<test feature a>>
<<test feature b>>
@

\section{Feature A Implementation}
<<implementation of feature a>>=
...
@

\subsection{Verifying Feature A}
<<test feature a>>=
class TestFeatureA:
    def test_basic_case(self):
        ...
@
```

#### Anti-Pattern: Tests Before Implementation

**BAD** (Tests appear 300 lines before implementation):
```noweb
\section{Testing}
<<test module.py>>=
import module

<<test equality>>=    ← Reader doesn't know what this tests yet!
def test_users_equal():
    ...
@

[300 lines of other content]

\section{Make Classes Comparable}  ← Implementation finally appears!
<<implementation>>=
def make_comparable(cls):
    ...
@
```

**Reader confusion:**
- "What does `test_users_equal` test? I haven't seen the code yet!"
- Must scroll back hundreds of lines to understand tests
- Tests feel unmotivated and disconnected

**GOOD** (Tests appear after implementation):
```noweb
\section{Make Classes Comparable}
<<implementation>>=
def make_comparable(cls):
    ...
@

\subsection{Verifying Comparability}

Now let's verify the decorator works correctly...

<<test equality>>=
def test_users_equal():
    ...
@
```

**Reader clarity:**
- Sees implementation first
- Understands what's being tested
- Tests serve as proof/verification
- Natural pedagogical flow

#### Framing Test Sections

Use pedagogical framing to introduce test sections:

**Good framing language:**
- "Now let's verify this works correctly..."
- "Let's prove this implementation handles edge cases..."
- "We can demonstrate correctness with these tests..."
- "To ensure reliability, we test..."

**Avoid:**
- Starting tests with no context
- Separating tests completely from what they test
- Grouping unrelated tests together

#### Test Organization Roadmap

For files with many test sections, provide a roadmap early:

```latex
\subsection{Test Organization}

Tests are distributed throughout this file:
\begin{description}
\item[Feature A tests] Appear after implementation (Section~\ref{sec:featureA})
\item[Feature B tests] Appear after implementation (Section~\ref{sec:featureB})
\item[Integration tests] Appear after all features (Section~\ref{sec:integration})
\end{description}
```

#### When to Use This Pattern

**Use distributed test placement when:**
- Tests verify specific implementations in the same file
- Pedagogical clarity is important
- Tests serve as proof/examples of correctness
- File is meant to be read by humans (documentation-oriented)

**Consider grouped tests when:**
- Tests are integration tests spanning multiple modules
- Test file is separate from implementation (.nw file just for tests)
- Tests don't directly correspond to specific code sections

#### Benefits of This Approach

1. **Pedagogical clarity**: Readers learn before they see verification
2. **Proximity**: Tests next to implementation (easier maintenance)
3. **Motivation**: Tests feel natural, not arbitrary
4. **Flow**: Natural progression from problem → solution → proof
5. **Findability**: Easy to locate tests for specific functionality

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

## Version Control & Git Practices

This project follows atomic commit practices. **Commit early, commit often, one concern per commit.**

### Branch Safety: Never Commit to main/master

**CRITICAL**: Before making any commits, verify you're on the correct branch.

#### Pre-Commit Branch Check

```bash
# Always check current branch first
git branch --show-current
```

**Rules:**
- ✅ **NEVER** commit directly to `main` or `master` branches
- ✅ **ALWAYS** work on a feature/topic branch
- ✅ **ASK** the user about the branch if uncertain

#### Creating Feature Branches

```bash
# Create and switch to new branch
git checkout -b feature-name

# Verify you're on the new branch
git branch --show-current
```

**Branch naming conventions:**
- Use descriptive names: `fix-auth-bug` not `fix1`
- Use hyphens: `add-user-feature` not `add_user_feature`
- Be specific: `fix-timestamp-parsing` not `fixes`

#### Checking Branch Suitability

**Before committing to an existing branch, verify it's suitable for the current work:**

When you're about to commit changes:
1. Check the current branch name
2. Assess if the work matches the branch purpose
3. If uncertain or mismatched, ask the user

**When to ask about branching:**
- Current branch name doesn't match the work being done
  - Example: On `fix/calendar-stdlib-shadowing` but working on a different issue
- Work is independent and could be a separate PR
  - Example: Removing duplicate code (separate concern from renaming modules)
- Preferring to branch from master/main for independence
  - Allows PRs to be merged independently without dependencies

**Example dialogue:**
```
Assistant: "I notice we're on branch 'fix/calendar-stdlib-shadowing' which is for
renaming the calendar module. The current fix (removing duplicate format_canvas_time)
is a separate concern. Should I:"

Options presented to user:
1. "Create new branch from master" - For independent PR, cleaner separation
2. "Create new branch from current" - If this fix depends on the rename
3. "Use current branch" - Group related cleanup together in one PR
```

**Benefits of proper branching:**
- **Independent PRs** - Each fix can be reviewed and merged separately
- **Clearer history** - Branch names accurately describe their changes
- **Easier rollback** - Can revert one fix without affecting others
- **Better collaboration** - Multiple people can work on different branches

**Branching strategy preference:**
- **Branch from master/main when possible** - Makes PRs independent
- **Branch from feature branch only when** - The new work depends on uncommitted changes
- **Use current branch only when** - Changes are closely related and belong together

### Atomic Commits: One Logical Change Per Commit

Each commit should represent **one logical change** that can be understood, reviewed, and reverted independently.

#### ✅ Commit Immediately After

1. **Fixing a single bug** - One bug, one commit
2. **Completing a logical unit** - Function works, tests pass
3. **Refactoring one aspect** - Before and after are both working states
4. **Adding one feature component** - Each independent piece
5. **Updating documentation** - Separate from code changes
6. **Making configuration changes** - Isolated from feature work
7. **Regenerating code from .nw sources** - After editing the .nw file

#### ❌ Don't Wait Until

- You've fixed "everything"
- The entire feature is complete
- End of day/session
- You remember to commit

### What Constitutes "One Logical Change"?

A single logical change is one **conceptual** modification that can be described
with a single purpose statement, even if it touches multiple files or locations.

**Example: Replacing magic numbers with constants**

Bad (too granular - split what should be one commit):
```
✗ Commit 1: "Define threshold constants at module level"
✗ Commit 2: "Use constants for command-line argument defaults"
✗ Commit 3: "Use constants for function parameter defaults"
✗ Commit 4: "Use constants in documentation"
```

Good (single logical change):
```
✓ One commit: "Replace hardcoded threshold values with named constants"
  - Define DEFAULT_THRESHOLD_FIXED and DEFAULT_THRESHOLD_PERCENT
  - Update argument parser defaults to use constants
  - Update function parameter defaults to use constants
  - Update documentation to reference constants
```

**Why this is one commit:**
- Single conceptual change: "eliminate magic numbers"
- Changes are not independently useful (defining constants without using them
  accomplishes nothing)
- Would never want to revert just part of this change
- Reviewer understands the complete picture in one diff

**Contrast with truly independent changes:**
```
✓ Commit 1: "Add --threshold-fixed option"
  (Independent: adds new functionality)

✓ Commit 2: "Add --threshold-percent option"
  (Independent: adds different functionality)

✓ Commit 3: "Replace hardcoded values with constants"
  (Independent: refactoring that doesn't add features)
```

**Rule of thumb:** If you can't describe the change without using "and" to link
unrelated concepts, it should be multiple commits. But if "and" connects steps
of the same change, it's one commit.

- "Add user model **and** update constants" → Two commits
- "Define constants **and** use them everywhere" → One commit

### Workflow for Multiple Changes

**Step-by-Step Process:**

When you have multiple fixes to make:

1. **Fix the first issue**
   ```bash
   # Make the change
   vim file1.nw

   # Verify it works (if applicable)
   make

   # Commit immediately
   git add file1.nw
   git commit -m "Fix specific issue in file1"
   ```

2. **Fix the second issue**
   ```bash
   # Make the change
   vim file2.nw

   # Commit immediately
   git add file2.nw
   git commit -m "Fix specific issue in file2"
   ```

3. **Continue for each issue**
   - Never batch multiple fixes
   - Each commit should be independently reviewable

### Commit Message Guidelines

**Format:**
```
Short summary (50 chars or less, imperative mood)

Optional detailed explanation:
- What changed
- Why it changed
- Impact or implications

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Summary line rules:**
- **Imperative mood**: "Fix bug" not "Fixed bug" or "Fixes bug"
- **Capitalize first word**: "Add feature" not "add feature"
- **No period at end**: "Update docs" not "Update docs."
- **Be specific**: "Fix timestamp mismatch in terminal grading" not "Fix bug"
- **Stay under 50 characters** when possible

**Good vs Bad Messages:**

**Bad:**
```
✗ "Fix stuff"
✗ "Updates"
✗ "WIP"
✗ "Fixed various issues"
✗ "Changes to multiple files"
```

**Good:**
```
✓ "Fix timestamp format mismatch in terminal grading"
✓ "Remove undefined variable from check_student"
✓ "Quote variables in common.sh for space safety"
✓ "Add error handling for missing config file"
```

### Pre-Commit Checklist

Before each commit, verify:

- [ ] **On correct branch** - Not on main/master (unless explicitly approved)
- [ ] This commit represents ONE logical change
- [ ] The commit message clearly describes what changed
- [ ] All related changes are included (nothing missing)
- [ ] No unrelated changes are included (nothing extra)
- [ ] The code works/builds at this commit (if applicable)
- [ ] The commit can be understood independently
- [ ] **No generated files** - If literate programming project, verify no .py/.tex files with .nw sources are staged

**The mantra:** "Working state reached → Commit now → Continue working"

## GitHub Copilot Context

This repository includes:
- `.github/copilot-instructions.md` - Detailed project context and patterns
- `.copilotignore` - Files excluded from Copilot context

Key principles from Copilot instructions:
- Follow literate programming conventions
- Maintain POSIX-compatible output
- Use existing module patterns for consistency
- Document complex logic in TeX portion of `.nw` files
