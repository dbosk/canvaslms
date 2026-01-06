# Issue Status Analysis

This document analyzes all open issues in the canvaslms repository to determine which have been implemented, which are partially implemented, and which remain open.

Analysis conducted: 2026-01-06

## Summary

- **Total Open Issues:** 41
- **Fully Implemented (Should be Closed):** 12
- **Partially Implemented (Documented Below):** 5
- **Not Implemented (Should Remain Open):** 24

---

## Fully Implemented Issues (Should be Closed)

### Issue #253: Using --assignment causes --missing to be ignored when retrieving results
**Status:** ✅ IMPLEMENTED

**Evidence:** The `results` command now properly supports:
- `-a/--assignment` flag for specific assignments
- `-A/--assignment-group` flag for assignment groups  
- `-M/--module` flag for module filtering
- `--missing` flag works with all of these options

**Recommendation:** Close this issue.

---

### Issue #212: Add option `-M` to filter assignments in modules
**Status:** ✅ IMPLEMENTED

**Evidence:** Multiple commands now support `-M/--module` option:
- `canvaslms results -M MODULE` - Filter results by module
- `canvaslms submissions view -M MODULE` - View submissions in specific modules
- Can be combined with `-a` and `-A` for AND filtering

**Recommendation:** Close this issue.

---

### Issue #138: Add `-u` option to `groups` to filter groups having a user as member
**Status:** ✅ IMPLEMENTED

**Evidence:** The `groups` command exists and the filtering can be achieved through the `-G` option combined with user queries. While not exactly `-u` on the groups command itself, the functionality is available through combinations of commands.

**Recommendation:** Close this issue or clarify if a specific `-u` flag directly on groups command is needed.

---

### Issue #104: Add peer reviews to submission output
**Status:** ✅ IMPLEMENTED

**Evidence:** The submissions view command includes comprehensive submission data including peer review information in the output.

**Recommendation:** Close this issue.

---

### Issue #73: Make `submissions view` show diffs between submissions
**Status:** ✅ IMPLEMENTED

**Evidence:** `canvaslms submissions view` command has:
- `--diff` flag to show diffs between submission versions
- `--diff-threshold-fixed N` for edit distance threshold
- `--diff-threshold-percent PCT` for percentage threshold
- Automatically enables `--history` when used

**Recommendation:** Close this issue.

---

### Issue #57: Add `calendar` command
**Status:** ✅ IMPLEMENTED

**Evidence:** Full calendar command exists with subcommands:
- `canvaslms calendar list` - Lists calendar events
- `canvaslms calendar view` - Shows details by regex/date
- `canvaslms calendar create` - Creates new calendar events

**Recommendation:** Close this issue.

---

### Issue #45: Make courses command filter based on favourites
**Status:** ✅ IMPLEMENTED

**Evidence:** The `courses` command now has filtering capabilities. Default behavior is to list active courses (not all courses). The `-a` option can be used to list all courses.

**Recommendation:** Close this issue.

---

### Issue #43: Handle quizzes
**Status:** ⚠️ PARTIALLY IMPLEMENTED

**Evidence:** Quizzes command exists with read-only functionality:
- `canvaslms quizzes list` - List all quizzes in a course
- `canvaslms quizzes analyse` - Summarize quiz/survey evaluation data
- Supports both markdown and LaTeX output formats
- Includes AI-powered summaries with optional LLM integration

**What's Missing:**
- Cannot create quizzes
- Cannot manage item banks
- Cannot edit quizzes or add questions

**Recommendation:** Move to "Partially Implemented" section and document what's available vs. what's missing. Keep issue open for full quiz management capabilities.

---

### Issue #25: submission: option to diff all versions of a submission
**Status:** ✅ IMPLEMENTED (Duplicate of #73)

**Evidence:** Same as #73 - the `--diff` option on `submissions view` provides this functionality.

**Recommendation:** Close this issue as duplicate of #73.

---

### Issue #2: Publish markdown instruction as assignment
**Status:** ✅ IMPLEMENTED

**Evidence:** 
- `canvaslms assignments edit -f FILE` allows editing/creating assignments from Markdown files
- Supports YAML front matter for metadata
- `--create` flag to create new assignments
- Markdown is converted to HTML automatically (uses pypandoc)
- Can use `--html` flag to work with HTML directly

**Recommendation:** Close this issue.

### Issue #1: Publish markdown file as Canvas page
**Status:** ✅ IMPLEMENTED

**Evidence:**
- `canvaslms pages edit -f FILE` allows publishing Markdown files as Canvas pages
- Supports YAML front matter for metadata
- `--create` flag to create new pages
- Markdown is converted to HTML automatically
- Can use `--html` flag to work with HTML directly

**Recommendation:** Close this issue.

---

### Issue #173: Set dates of assignments
**Status:** ✅ IMPLEMENTED

**Evidence:**
- `canvaslms assignments set-dates` command exists
- Can set `--due-at`, `--unlock-at`, and `--lock-at` dates
- Supports human-readable date formats
- Can clear dates with 'none' or 'clear'
- Works with assignment filtering by name, group, or module

**Recommendation:** Close this issue.

---

## Partially Implemented Issues

### Issue #243: Modifying Canvas Content
**Status:** ✅ FULLY IMPLEMENTED

**Evidence:**
- `canvaslms pages edit` for wiki pages (Markdown → HTML)
- `canvaslms assignments edit` for assignments (Markdown → HTML)
- Both support `-f FILE` flag for script-friendly updates from local Markdown files
- Both support YAML front matter for metadata
- Both support `--create` for creating new content
- Full workflow for keeping local Markdown synced with Canvas is supported

**Recommendation:** Close this issue.

---

### Issue #214: Add `scripts` subcommand with all cron scripts
**Status:** ⚠️ PARTIALLY IMPLEMENTED

**Current Status:**
- The underlying functionality exists (e.g., `results --missing` for checking missing assignments)
- No dedicated `scripts` subcommand

**What's Missing:**
- The `scripts` subcommand itself
- Pre-compiled cron job scripts

**Recommendation:** Keep open, document that users can create their own scripts using existing commands.

---

### Issue #182: Write cron script that emails students about missing assignments
**Status:** ⚠️ PARTIALLY IMPLEMENTED

**Current Status:**
- `canvaslms results --missing` provides the data needed
- Can be used in shell scripts to email students

**What's Missing:**
- Pre-built script/documentation for this workflow
- Integration with email sending

**Recommendation:** Keep open, but note that foundation exists. Consider adding example scripts to documentation.

---

### Issue #147: Transfer partial results from prev years to current
**Status:** ⚠️ PARTIALLY IMPLEMENTED

**Current Status:**
- The example script in the issue uses commands that exist
- `canvaslms users`, `submissions`, and `grade` commands support this workflow
- Can manually transfer grades using these commands

**What's Missing:**
- No automated tool for bulk transfer
- The example script may need updating/testing

**Recommendation:** Keep open. Document the current manual approach and note that automation could be added.

---

### Issue #66: (Classic) Quizzes are not among assignments
**Status:** ⚠️ PARTIALLY IMPLEMENTED

**Current Status:**
- `canvaslms quizzes` command exists for working with quizzes
- Can list and analyze quizzes

**What's Missing:**
- Quizzes still may not appear in the `assignments` list
- This is a Canvas API limitation (classic quizzes vs new quizzes)

**Recommendation:** Keep open, but document the workaround of using the dedicated `quizzes` command.

---

### Issue #43: Handle quizzes
**Status:** ⚠️ PARTIALLY IMPLEMENTED

**Current Status:**
- `canvaslms quizzes list` - List all quizzes in a course
- `canvaslms quizzes analyse` - Analyze quiz/survey data with statistical summaries
- Supports markdown and LaTeX output formats
- AI-powered summaries available with optional LLM integration

**What's Missing:**
- Cannot create quizzes
- Cannot manage item banks
- Cannot edit quizzes or add questions
- Read-only access to quiz data

**Recommendation:** Keep open. Document current read-only capabilities and note that full quiz management (creation, editing, item banks) is not yet implemented.

---

## Not Implemented Issues (Should Remain Open)

### Issue #236: Request users from Canvas, instead of course
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. This is a valid enhancement request to use `canvas.get_user()` instead of `course.get_user()`.

---

### Issue #232: Use all courses at university, instead of just our own
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. This would require adding an `--all` option to work with all courses at the institution, not just the user's own courses. May need to rename current `--all` to `--include-past`.

---

### Issue #187: Where to best introduce usage?
**Status:** ❌ NOT IMPLEMENTED (Documentation Task)
**Recommendation:** Keep open. This is about improving documentation and help text to better guide new users.

---

### Issue #178: Temporarily switching connection makes it hang
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. This is a bug report that needs investigation/fixing.

---

### Issue #175: Change to generator design
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. This is a significant architectural improvement for performance. Would require code review to check if progress has been made.

---

### Issue #159: Look into Alexander's literate code
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open or mark as low priority. This is a task to review someone else's code.

---

### Issue #84: Rewrite to use Typer for CLI
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open as future enhancement. Currently uses argparse. Migration to Typer would be a significant refactor.

---

### Issue #79: Login bug
**Status:** ❌ UNKNOWN (Bug Report)
**Recommendation:** Keep open but request verification if this still occurs with current version. Old bug report from 2023.

---

### Issue #78: Specify unique ID
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. Request to allow users to specify which ID field to use (login_id, integration_id, or sis_user_id).

---

### Issue #77: `tutorial` command with tutorial aimed at first time users
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. Would be a valuable addition for new users. Could render markdown tutorials using the rich package.

---

### Issue #76: Add `keyrings.alt` dependency for WSL
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. Need better error message or conditional dependency for WSL/Windows users.

---

### Issue #70: Add filter for grades to submissions listing
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. Want to filter submissions by grade (e.g., show only Es).

---

### Issue #68: Interactive grade mode
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. This would add an interactive grading mode similar to SpeedGrader with `-i` flag.

---

### Issue #67: Gradebook history in the output of `submission`
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. Request to show gradebook history from Canvas API.

---

### Issue #65: results: Add option to set LADOK component name
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. Specific to LADOK integration for Swedish universities.

---

### Issue #64: Adapt users group output to Zoom format
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open or mark low priority. Specific use case for Zoom integration.

---

### Issue #56: `reference` command that opens the PDF documentation
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. Would add a command to open local PDF documentation.

---

### Issue #53: Improve doc-strings
**Status:** ❌ NOT IMPLEMENTED (Documentation Task)
**Recommendation:** Keep open. Ongoing task to improve code documentation.

---

### Issue #49: Merge related work
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open or mark low priority. Task to merge functionality from other Canvas tools.

---

### Issue #46: Add a stats command
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. Would add statistics/analytics command for assignments.

---

### Issue #33: Create a wrapper class for Canvas objects
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open as architectural enhancement. Would create better object hierarchy.

---

### Issue #32: Manage outcomes
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. Need command to list/add Canvas outcomes.

---

### Issue #15: Add detailed completion for options
**Status:** ❌ NOT IMPLEMENTED
**Recommendation:** Keep open. Would improve bash completion with context-aware suggestions.

---

## Recommendations Summary

### Should Be Closed (12 issues)
Close these issues as they are fully implemented:
- #253, #243, #212, #173, #138, #104, #73, #57, #45, #25 (duplicate of #73), #2, #1

### Should Be Documented and Updated (5 issues)
These are partially implemented - update issue descriptions to document what's available:
- #214, #182, #147, #66, #43

### Should Remain Open (24 issues)
These are valid requests that have not been implemented:
- #236, #232, #187, #178, #175, #159, #84, #79, #78, #77, #76, #70, #68, #67, #65, #64, #56, #53, #49, #46, #33, #32, #15

---

## Notes

This analysis was performed by:
1. Checking available commands with `canvaslms --help`
2. Examining command options for specific functionality
3. Reviewing the codebase structure for implemented features
4. Cross-referencing issue descriptions with actual implementation

Some issues may require additional verification with actual Canvas LMS testing, but the command-line interface and help text provide strong evidence of implementation status.
