# Issue Status Quick Reference

Quick lookup table for all 41 open issues. See `ISSUE_STATUS_ANALYSIS.md` for detailed analysis.

## Issues to Close (12) ✅

| # | Title | Status |
|---|-------|--------|
| 253 | Using --assignment causes --missing to be ignored | ✅ Fixed |
| 243 | Modifying Canvas Content | ✅ Implemented |
| 212 | Add option `-M` to filter assignments in modules | ✅ Implemented |
| 173 | Set dates of assignments | ✅ Implemented |
| 138 | Add `-u` option to `groups` | ✅ Implemented (via combinations) |
| 104 | Add peer reviews to submission output | ✅ Implemented |
| 73 | Make `submissions view` show diffs | ✅ Implemented |
| 57 | Add `calendar` command | ✅ Implemented |
| 45 | Make courses command filter based on favourites | ✅ Implemented |
| 25 | submission: option to diff all versions | ✅ Implemented (duplicate of #73) |
| 2 | Publish markdown instruction as assignment | ✅ Implemented |
| 1 | Publish markdown file as Canvas page | ✅ Implemented |

## Issues to Update (5) ⚠️

| # | Title | What Works | What's Missing |
|---|-------|-----------|----------------|
| 43 | Handle quizzes | List and analyze quizzes | Cannot create/edit quizzes or manage item banks |
| 214 | Add `scripts` subcommand | All underlying commands exist | Dedicated `scripts` subcommand |
| 182 | Cron script for emailing students | `results --missing` provides data | Pre-built script/examples |
| 147 | Transfer partial results from prev years | Manual workflow supported | Automated bulk tool |
| 66 | (Classic) Quizzes not among assignments | Dedicated `quizzes` command | Canvas API limitation |

## Issues to Keep Open (24) 🔄

### High Priority
- 236: Request users from Canvas, instead of course
- 178: Temporarily switching connection makes it hang
- 79: Login bug
- 78: Specify unique ID
- 77: `tutorial` command
- 76: Add `keyrings.alt` dependency for WSL

### Medium Priority
- 232: Use all courses at university
- 187: Where to best introduce usage?
- 175: Change to generator design
- 70: Add filter for grades to submissions listing
- 68: Interactive grade mode
- 67: Gradebook history in submission output
- 56: `reference` command
- 53: Improve doc-strings
- 46: Add a stats command
- 15: Add detailed completion for options

### Lower Priority / Niche
- 159: Look into Alexander's literate code
- 84: Rewrite to use Typer for CLI
- 65: LADOK component name option
- 64: Zoom format for users group output
- 49: Merge related work
- 33: Create wrapper class for Canvas objects
- 32: Manage outcomes

---

## Quick Commands Reference

Commands verified as implemented:

```bash
# Markdown publishing
canvaslms pages edit -f page.md --create
canvaslms assignments edit -f assignment.md --create

# Assignment dates
canvaslms assignments set-dates -c COURSE -a ASSIGNMENT --due-at "2024-12-31"

# Submission diffs
canvaslms submissions view -c COURSE -a ASSIGNMENT --diff

# Module filtering
canvaslms results -c COURSE -M "Module Name"

# Quizzes
canvaslms quizzes list -c COURSE
canvaslms quizzes analyse --csv file.csv

# Calendar
canvaslms calendar list -c COURSE
canvaslms calendar create -c COURSE --title "Event"

# Missing assignments
canvaslms results -c COURSE --missing
```

---

*Analysis Date: 2026-01-06*  
*Full Details: See ISSUE_STATUS_ANALYSIS.md and ISSUE_RECOMMENDATIONS.md*
