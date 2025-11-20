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

**CRITICAL: This project uses literate programming. The .nw files are the source of truth, not the generated .py files.**

#### Core Principles (Donald Knuth)

1. **Explain to humans what we want computers to do** - Write for human readers, not compilers
2. **Present concepts in pedagogical order** - Organize by best learning sequence, not execution order
3. **Document the "why" not just the "what"** - Explain design decisions, trade-offs, and rationale

#### Essential Workflow

**NEVER edit .py files directly** - they are generated from .nw sources and will be overwritten.

**ALWAYS follow this workflow when working with .nw files:**

1. Read the existing .nw file to understand current narrative and structure
2. Plan changes with literate programming in mind:
   - What is the "why" behind this change? (Explain in documentation)
   - How does this fit into the existing narrative?
   - Should I use contrast to explain the change? (old vs new approach)
   - What new chunks are needed? What are their meaningful names?
   - Where in the pedagogical order should this be explained?
3. Write documentation BEFORE writing code
4. Decompose code into well-named chunks
5. Regenerate with `make` to tangle .nw → .py
6. Test the generated code

#### Chunk Naming Conventions

Chunk names should be **meaningful and describe purpose** (like pseudocode), not syntax:

**Good chunk names** (what/why):
- `<<process user options>>`
- `<<filter submissions by group>>`
- `<<compute speedgrader URL>>`
- `<<handle missing course error>>`

**Bad chunk names** (syntactic):
- `<<for loop>>`
- `<<function definition>>`
- `<<if statement>>`
- `<<imports>>`

Chunk names should be **2-5 words** summarizing the chunk's purpose.

#### Line Length Conventions

- Keep lines under **80 characters** in both documentation and code chunks
- This improves readability and follows traditional Unix conventions
- Break long lines at natural points (after commas, before operators)
- For Python: use implicit string concatenation or parentheses for long expressions

#### Variation Theory in Documentation

Structure explanations using variation theory patterns:

- **Contrast**: Show different approaches, explain why one was chosen
- **Separation**: Present the whole first, then decompose into parts
- **Generalization**: Show patterns across similar code
- **Fusion**: Bring parts back together to show the complete picture

Example:
```noweb
\section{The submissions command}

We want to list submissions for assignments. This requires getting the
assignment list, fetching submissions, filtering if specified, and
formatting output.

<<submission command>>=
def submission_command(config, canvas, args):
    assignment_list = <<get assignments>>
    submissions = <<get submissions for assignments>>
    <<filter submissions if needed>>
    <<format and print output>>
@

\subsection{Getting submissions}

Canvas provides two APIs: one for all submissions, one for ungraded only.
We use the ungraded API when [[--ungraded]] is specified to reduce load.

<<get submissions for assignments>>=
if args.ungraded:
    submissions = list_ungraded_submissions(assignment_list)
else:
    submissions = list_submissions(assignment_list)
@
```

#### Noweb Syntax

- **Code chunks**: Begin with `<<chunk name>>=` (must start in column 1)
- **Code references**: Use `[[code]]` notation in documentation (escapes special characters)
- **Chunk references**: Use `<<chunk name>>` in code to reference other chunks
- **Documentation chunks**: Begin with `@` followed by space or newline

### LaTeX Writing Best Practices

The documentation portions of .nw files use LaTeX. Follow these best practices for semantic, well-structured LaTeX:

#### Core Principle: Semantic Markup

Use LaTeX environments that match the **semantic meaning** of the content, not just the visual appearance.

#### List Environments

**Use `description` for term-definition pairs:**

When you have labels followed by explanations, use `description`:

```latex
\begin{description}
\item[Parameter] Explanation of the parameter
\item[Option] Description of the option
\item[Pattern] What the pattern matches
\end{description}
```

**NEVER do this:**
```latex
\begin{itemize}
\item \textbf{Parameter:} Explanation of the parameter
\item \textbf{Option:} Description of the option
\end{itemize}
```

**Use `itemize` for simple uniform lists:**
```latex
\begin{itemize}
\item First uniform item
\item Second uniform item
\end{itemize}
```

**Use `enumerate` for numbered steps:**
```latex
\begin{enumerate}
\item First step in the process
\item Second step in the process
\end{enumerate}
```

#### Quotations: Always Use csquotes

**ALWAYS use `\enquote{...}` for quotes, NEVER manual quote marks:**

```latex
% CORRECT
\enquote{This is a quote}
\enquote{outer \enquote{inner} quote}

% INCORRECT - Never do this
"This is a quote"
``This is a quote''
'single quotes'
```

The `\enquote` command handles nested quotes automatically and adapts to language settings.

#### Emphasis: Never Use ALL CAPITALS

**Use `\emph{...}` for emphasis, NEVER ALL CAPITALS in running text:**

```latex
% CORRECT
This is \emph{very} important to understand.
The \emph{benefits} of classes are clear.

% INCORRECT - Never do this
This is VERY important to understand.
The BENEFITS of classes are clear.
```

Exception: Acronyms (NASA, PDF) that are conventionally capitalized are fine.

#### Code References

- Use `[[code]]` notation for inline code in noweb (automatically escapes special characters)
- Use `\verb|code|` or `\verb!code!` for LaTeX-only inline code
- Use `listings` package for longer code blocks with syntax highlighting

#### Cross-References

- Always use `\label` and `\ref` (or `\cref` with cleveref package)
- Never hard-code numbers: "Section 3" → "Section~\ref{sec:implementation}"
- Use descriptive labels: `\label{sec:introduction}` not `\label{s1}`

#### Paths and File References

- Always use forward slashes: `figures/diagram.pdf` not `figures\diagram.pdf`
- This works on all platforms including Windows

#### Common Anti-Patterns to Avoid

- ❌ Bold labels in itemize: `\item \textbf{Label:}` → Use `description` instead
- ❌ Manual quotes: `"text"` or `` `text' `` → Use `\enquote{text}`
- ❌ ALL CAPITALS for emphasis → Use `\emph{text}`
- ❌ Hard-coded references: "Figure 1" → Use `\ref{fig:label}` or `\cref{fig:label}`
- ❌ Manual citation formatting → Use `\cite` commands

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

def command_function(config, canvas, args):
    """Implementation of the command"""
    # Command logic here
```

#### Canvas API Usage
```python
import canvaslms.cli.courses as courses

def example_command(config, canvas, args):
    """Standard pattern for Canvas API usage"""
    # Canvas object is already instantiated and passed to the function
    course_list = courses.process_course_option(canvas, args)
    # Use the course_list for further processing
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
2. **Write documentation first**: In .nw files, explain the "why" in LaTeX before writing code
3. **Use semantic LaTeX**: Follow the LaTeX best practices above (description lists, \enquote, \emph, etc.)
4. **Name chunks meaningfully**: Use 2-5 word names that describe purpose, not syntax
5. **POSIX compatibility**: Ensure output works well with Unix tools
6. **Error handling**: Provide clear error messages for common failures (raise EmptyListError when appropriate)
7. **Testing**: Consider edge cases like missing courses, invalid IDs, etc.

### Quality Checklist for Literate Programs

When writing or reviewing .nw files, ensure:

**Narrative Quality:**
- [ ] Introduction explains the problem and motivation
- [ ] Design decisions are explained with rationale
- [ ] Concepts are in pedagogical order (not execution order)
- [ ] The "why" is documented, not just the "what"
- [ ] Complex algorithms have worked examples
- [ ] Trade-offs between alternatives are discussed using contrast
- [ ] Edge cases and limitations are documented

**Code Organization:**
- [ ] Chunk names are meaningful and describe purpose (like pseudocode)
- [ ] Each chunk represents a single coherent concept
- [ ] Chunks are appropriately sized (not too large or small)
- [ ] Helper functions are used instead of excessive chunk decomposition
- [ ] Code references use `[[code]]` notation properly
- [ ] No unused chunks (verify with `noroots file.nw`)

**LaTeX Quality:**
- [ ] Uses `description` for term-definition pairs, not `\item \textbf{Label:}`
- [ ] Uses `\enquote{...}` for quotes, never manual `"..."` or `` `...' ``
- [ ] Uses `\emph{...}` for emphasis, never ALL CAPITALS
- [ ] Uses `\ref` or `\cref` for references, never hard-coded numbers
- [ ] Paths use forward slashes
- [ ] Lines are under 80 characters

**Technical Quality:**
- [ ] Code is correct and follows project patterns
- [ ] Generated Python follows project style (use `black` formatter)
- [ ] CLI commands follow the `add_command()` pattern
- [ ] Utility functions follow `add_XXX_option()` / `process_XXX_option()` pattern
- [ ] Error handling uses `EmptyListError` appropriately
- [ ] Output follows TSV conventions or uses `csv.writer`

### Naming Conventions
- Use snake_case for Python functions and variables
- CLI commands use lowercase with hyphens (e.g., `canvas-lms`)
- Module names match their primary command (though usually a module has a set of subcommands)

### Canvas API Best Practices
- Always validate course and assignment IDs
- Handle missing resources gracefully
- Use Canvas API pagination for large datasets
- Cache course and user lookups when appropriate

## Build System

The project uses a Make-based build system with custom makefiles from the `makefiles/` directory.

### Core Build Commands

```bash
# Top-level build
make all           # Generates Python from .nw sources and builds package + PDF docs
make compile       # Tangles .nw files and runs poetry build (no PDF)
make install       # Installs with pip -e and sets up bash completion
make distclean     # Removes build/, dist/, *.egg-info

# Module-level build (in src/canvaslms/cli/ or src/canvaslms/grades/)
cd src/canvaslms/cli
make all           # Generates all .py and .tex files from .nw sources
make clean         # Removes generated files
```

### Noweb Commands

**Tangling (extracting code from .nw files):**

```bash
# Extract a specific root chunk
notangle -R<chunkname> file.nw > output.py

# With line number directives for debugging (C/C++/etc, not Python)
notangle -L -R<chunkname> file.nw > output.cpp

# Default root is <<*>>
notangle file.nw > output.py

# List all root chunks (not used in other chunks)
noroots file.nw
```

**Weaving (creating documentation from .nw files):**

```bash
# Generate LaTeX
noweave -latex file.nw > output.tex

# With cross-references and index
noweave -latex -x -index -autodefs python file.nw > output.tex

# No wrapper (for inclusion in larger document)
noweave -n -latex file.nw > output.tex

# Delay preamble (for custom \documentclass)
noweave -delay -latex file.nw > output.tex
```

### Build System Details

- `noweb.mk` from `makefiles/` provides suffix rules for `.nw → .py` and `.nw → .tex`
- Each module's Makefile lists files in `MODULES` variable
- `cli/__init__.py` is generated from `cli.nw` via intermediate `cli.py`
- Generated Python files are in `.gitignore` - only .nw files are version controlled

### Make Patterns

```makefile
# Typical pattern in module Makefiles
%.py: %.nw
    notangle -R$@ $< > $@

%.tex: %.nw
    noweave -n -latex $< > $@
```

### Testing Generated Code

After regenerating:
```bash
cd src/canvaslms/cli
make all                    # Regenerate .py files
cd ../../..
make install                # Install for testing
canvaslms command --help    # Verify it works
```

## Common Tasks

### Adding a New Subcommand

Follow this literate programming workflow:

1. **Plan the narrative structure** before writing any code:
   - What problem does this command solve? (motivation)
   - What design decisions are involved? (rationale)
   - What are the key concepts? (pedagogical order)
   - What examples illustrate usage? (concrete instances)

2. **Create the .nw file with documentation first**: `src/canvaslms/cli/newcommand.nw`
   - Write a chapter/section introduction explaining what and why
   - Explain the approach and design decisions
   - Use variation theory (contrast, separation, generalization, fusion)

3. **Structure the file following project patterns:**
   ```noweb
   \chapter{The [[newcommand]] command}

   <<introduction explaining what the command does and why>>

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
   <<explain algorithm, design decisions, edge cases>>
   ```

4. **Write code chunks that support the narrative:**
   - Use meaningful chunk names (2-5 words describing purpose)
   - Decompose by concept, not syntax
   - Explain "why" in prose, not code comments
   - Follow project patterns (`add_command()`, `process_XXX_option()`)

5. **Integrate into build system:**
   - Add to `src/canvaslms/cli/Makefile`: `MODULES+= newcommand.py newcommand.tex`

6. **Register the command in `cli.nw`:**
   ```python
   import canvaslms.cli.newcommand
   # ... in main():
   canvaslms.cli.newcommand.add_command(subp)
   ```

7. **Build and test:**
   ```bash
   cd src/canvaslms/cli
   make all                    # Generate .py and .tex
   cd ../../..
   make install                # Install for testing
   canvaslms newcommand --help # Verify it works
   ```

8. **Review literate quality** using the checklist above before considering the task complete

### Module Utility Functions
Each module often provides utility functions to add options to other commands. For example, the course module provides a function to add all options to match courses (`add_course_option`), then it provides a function to generate a list of courses, given the args (`process_course_option`). These patterns allow for consistent option handling across subcommands.

### Canvas Data Retrieval
- Use course.get_assignments() for assignment lists
- Use course.get_users() for user lists
- Use assignment.get_submissions() for submission data
- Always handle API exceptions and rate limits

## Version Control & Git Practices

This project follows atomic commit practices. **Commit early, commit often, one concern per commit.**

### Automatic Git Workflow

When working on this repository:

1. **Check git status at the start** of any work session
2. **If on main/master branch**, create a feature branch first
3. **If on a feature branch**, follow atomic commit practices throughout the session
4. **Commit after each logical unit of work**, not at the end

### Creating Feature Branches

Always work on feature branches, never directly on main/master:

```bash
# Check current branch
git branch --show-current

# Create descriptive feature branch
git checkout -b fix-authentication-bug
git checkout -b add-export-feature
git checkout -b refactor-cache-decorator
```

**Branch naming:**
- Use hyphens: `fix-auth-bug` not `fix_auth_bug`
- Be specific: `fix-timestamp-parsing` not `fixes`
- Describe the work: `add-caching-support` not `feature1`

### Atomic Commits: One Logical Change Per Commit

Each commit should represent **one logical change** that can be understood, reviewed, and reverted independently.

**✅ Commit immediately after:**
- Fixing a single bug
- Completing a logical unit (function works, tests pass)
- Refactoring one aspect
- Adding one feature component
- Updating documentation
- Making configuration changes
- Regenerating code from .nw sources (after editing the .nw file)

**❌ Don't wait until:**
- You've fixed "everything"
- The entire feature is complete
- End of day/session
- You remember to commit

### Commit Granularity Examples

**Bad (bundled changes):**
```
✗ "Fix critical bugs in grading scripts"
  - Fixed timestamp bug
  - Fixed undefined variable
  - Fixed SSH injection
  - Quoted all variables everywhere
  (5 files, 90 insertions, 88 deletions)
```

**Good (atomic commits):**
```
✓ "Fix timestamp format mismatch in terminal grading"
  modules/terminal/grading/grade.sh.nw | 2 +-

✓ "Fix undefined variable in check_student function"
  adm/grading/common.sh.nw | 8 ++++----

✓ "Fix SSH command injection vulnerability"
  adm/grading/common.sh.nw | 3 ++-

✓ "Quote variables in common.sh for space safety"
  adm/grading/common.sh.nw | 12 ++++++------
```

### Workflow for Multiple Changes

When you have multiple fixes to make:

1. Fix the first issue
2. Regenerate if needed (`make`)
3. **Commit immediately**
4. Fix the second issue
5. **Commit immediately**
6. Continue for each issue

**Never batch multiple unrelated fixes into one commit.**

### Commit Message Guidelines

Format:
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
- Imperative mood: "Fix bug" not "Fixed bug"
- Capitalize first word: "Add feature" not "add feature"
- No period at end
- Be specific: "Fix timestamp mismatch in terminal grading" not "Fix bug"

**Good commit messages:**
```
✓ "Fix timestamp format mismatch in terminal grading"
✓ "Remove undefined variable from check_student"
✓ "Quote variables in common.sh for space safety"
✓ "Add caching decorator to Canvas API calls"
✓ "Document closure variable scoping in cache decorator"
```

**Bad commit messages:**
```
✗ "Fix stuff"
✗ "Updates"
✗ "WIP"
✗ "Fixed various issues"
```

### Integration with Literate Programming

**Important workflow for .nw files:**

1. Edit the .nw file (documentation + code)
2. Commit the .nw changes
3. Regenerate code with `make`
4. Commit the generated files (if tracked) OR ensure they're in .gitignore

**Current repository practice:** Generated .py files are in .gitignore, so only commit the .nw sources.

### Red Flags: Stop and Commit Now

Watch for these signs you should commit immediately:

- Modified 3+ files (probably multiple logical changes)
- Large `git diff` output
- Commit message would need "and" (means multiple concerns)
- 15+ minutes since last commit
- Before switching to a different task
- After completing any todo item

### Pre-Commit Checklist

Before each commit, verify:

- [ ] On correct branch (not main/master)
- [ ] Commit represents ONE logical change
- [ ] Message clearly describes what changed
- [ ] All related changes included (nothing missing)
- [ ] No unrelated changes included (nothing extra)
- [ ] Code works/builds at this commit (if applicable)

**The mantra:** "Working state reached → Commit now → Continue working"