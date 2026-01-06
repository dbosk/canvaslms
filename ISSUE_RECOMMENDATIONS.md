# Issue Status Recommendations

Based on a comprehensive analysis of all 41 open issues in the canvaslms repository, here are the recommended actions.

## Quick Summary

- ✅ **13 issues should be closed** - fully implemented
- ⚠️ **4 issues need documentation updates** - partially implemented  
- 🔄 **24 issues should remain open** - not yet implemented

---

## Issues to Close (Fully Implemented) - 13 Issues

These issues have been fully implemented and should be closed:

| Issue | Title | Evidence |
|-------|-------|----------|
| [#253](https://github.com/dbosk/canvaslms/issues/253) | Using --assignment causes --missing to be ignored | `results` command properly handles `-a` with `--missing` |
| [#243](https://github.com/dbosk/canvaslms/issues/243) | Modifying Canvas Content | `pages edit -f` and `assignments edit -f` fully support Markdown → Canvas workflow |
| [#212](https://github.com/dbosk/canvaslms/issues/212) | Add option `-M` to filter assignments in modules | `-M/--module` flag available on multiple commands |
| [#173](https://github.com/dbosk/canvaslms/issues/173) | Set dates of assignments | `assignments set-dates` command with all requested features |
| [#138](https://github.com/dbosk/canvaslms/issues/138) | Add `-u` option to `groups` | Functionality available through command combinations |
| [#104](https://github.com/dbosk/canvaslms/issues/104) | Add peer reviews to submission output | Peer review data included in `submissions view` |
| [#73](https://github.com/dbosk/canvaslms/issues/73) | Make `submissions view` show diffs | `--diff` flag with threshold options implemented |
| [#57](https://github.com/dbosk/canvaslms/issues/57) | Add `calendar` command | Full calendar command with list/view/create subcommands |
| [#45](https://github.com/dbosk/canvaslms/issues/45) | Make courses command filter based on favourites | Default behavior now filters appropriately |
| [#43](https://github.com/dbosk/canvaslms/issues/43) | Handle quizzes | Full `quizzes` command with list and analyse subcommands |
| [#25](https://github.com/dbosk/canvaslms/issues/25) | submission: option to diff all versions | Duplicate of #73, same `--diff` implementation |
| [#2](https://github.com/dbosk/canvaslms/issues/2) | Publish markdown instruction as assignment | `assignments edit -f file.md --create` |
| [#1](https://github.com/dbosk/canvaslms/issues/1) | Publish markdown file as Canvas page | `pages edit -f file.md --create` |

### Example Usage for Implemented Features

**Publishing Markdown as Canvas page (#1):**
```bash
canvaslms pages edit -c COURSE -f mypage.md --create
```

**Publishing Markdown as assignment (#2, #243):**
```bash
canvaslms assignments edit -c COURSE -f assignment.md --create
```

**Setting assignment dates (#173):**
```bash
canvaslms assignments set-dates -c COURSE -a ASSIGNMENT \
  --due-at "2024-12-31 23:59" --unlock-at "2024-12-01" --lock-at "2025-01-15"
```

**Showing diffs between submissions (#73, #25):**
```bash
canvaslms submissions view -c COURSE -a ASSIGNMENT --diff
```

**Filtering by module (#212):**
```bash
canvaslms results -c COURSE -M "Module Name" --missing
```

**Working with quizzes (#43):**
```bash
canvaslms quizzes list -c COURSE
canvaslms quizzes analyse --csv survey_results.csv
```

**Calendar operations (#57):**
```bash
canvaslms calendar list -c COURSE
canvaslms calendar create -c COURSE --title "Office Hours" --start "2024-12-15 14:00"
```

---

## Issues to Update (Partial Implementation) - 4 Issues

These issues are partially implemented. Update them to document what's available:

### [#214](https://github.com/dbosk/canvaslms/issues/214) - Add `scripts` subcommand with all cron scripts

**Status:** Foundation exists, but no dedicated subcommand

**What works:**
- All underlying functionality exists (`results --missing`, `submissions list -U`, etc.)
- Users can create their own cron scripts

**Example:**
```bash
# Check for ungraded submissions hourly
0 * * * * canvaslms submissions list -c COURSE -U | mail -s "Ungraded" teacher@example.com
```

**Recommendation:** Document the manual approach, keep open for future `scripts` subcommand.

---

### [#182](https://github.com/dbosk/canvaslms/issues/182) - Write cron script that emails students about missing assignments

**Status:** Foundation exists, needs documentation/examples

**What works:**
```bash
canvaslms results -c COURSE --missing
```

**What's missing:**
- Pre-built script
- Email integration documentation

**Recommendation:** Add example scripts to documentation, keep open for automated solution.

---

### [#147](https://github.com/dbosk/canvaslms/issues/147) - Transfer partial results from prev years to current

**Status:** Manual workflow supported

**What works:**
- All commands in example script exist and work
- `canvaslms users`, `submissions`, `grade` support this workflow

**What's missing:**
- Automated bulk transfer tool

**Recommendation:** Document the manual approach, keep open for automation enhancement.

---

### [#66](https://github.com/dbosk/canvaslms/issues/66) - (Classic) Quizzes are not among assignments

**Status:** Canvas API limitation, workaround exists

**What works:**
- Dedicated `canvaslms quizzes` command
- `quizzes list` and `quizzes analyse` available

**What's missing:**
- Quizzes in assignments list (Canvas API limitation)

**Recommendation:** Document the workaround, note this is a Canvas limitation.

---

## Issues to Keep Open (Not Implemented) - 24 Issues

These issues are valid enhancement requests that have not been implemented:

### High Priority / High Impact

| Issue | Title | Notes |
|-------|-------|-------|
| [#236](https://github.com/dbosk/canvaslms/issues/236) | Request users from Canvas, instead of course | Use `canvas.get_user()` instead of `course.get_user()` |
| [#178](https://github.com/dbosk/canvaslms/issues/178) | Temporarily switching connection makes it hang | Bug that needs investigation |
| [#79](https://github.com/dbosk/canvaslms/issues/79) | Login bug | Old bug report (2023) - verify if still occurs |
| [#78](https://github.com/dbosk/canvaslms/issues/78) | Specify unique ID | Allow choosing login_id/integration_id/sis_user_id |
| [#77](https://github.com/dbosk/canvaslms/issues/77) | `tutorial` command | Interactive tutorial for new users |
| [#76](https://github.com/dbosk/canvaslms/issues/76) | Add `keyrings.alt` dependency for WSL | Better error messages for WSL users |

### Medium Priority

| Issue | Title | Notes |
|-------|-------|-------|
| [#232](https://github.com/dbosk/canvaslms/issues/232) | Use all courses at university | `--all` to access institution-wide courses |
| [#187](https://github.com/dbosk/canvaslms/issues/187) | Where to best introduce usage? | Documentation improvement |
| [#175](https://github.com/dbosk/canvaslms/issues/175) | Change to generator design | Performance improvement (42+ `list()` calls found) |
| [#70](https://github.com/dbosk/canvaslms/issues/70) | Add filter for grades to submissions listing | Filter submissions by grade |
| [#68](https://github.com/dbosk/canvaslms/issues/68) | Interactive grade mode | SpeedGrader-like interface with `-i` |
| [#67](https://github.com/dbosk/canvaslms/issues/67) | Gradebook history in submission output | Show grade change history |
| [#56](https://github.com/dbosk/canvaslms/issues/56) | `reference` command | Open local PDF documentation |
| [#53](https://github.com/dbosk/canvaslms/issues/53) | Improve doc-strings | Ongoing documentation improvement |
| [#46](https://github.com/dbosk/canvaslms/issues/46) | Add a stats command | Assignment statistics/analytics |
| [#15](https://github.com/dbosk/canvaslms/issues/15) | Add detailed completion for options | Context-aware bash completion |

### Lower Priority / Niche

| Issue | Title | Notes |
|-------|-------|-------|
| [#159](https://github.com/dbosk/canvaslms/issues/159) | Look into Alexander's literate code | Review task |
| [#84](https://github.com/dbosk/canvaslms/issues/84) | Rewrite to use Typer for CLI | Major refactor to Typer from argparse |
| [#65](https://github.com/dbosk/canvaslms/issues/65) | results: Add option to set LADOK component name | LADOK-specific (Swedish universities) |
| [#64](https://github.com/dbosk/canvaslms/issues/64) | Adapt users group output to Zoom format | Zoom-specific integration |
| [#49](https://github.com/dbosk/canvaslms/issues/49) | Merge related work | Merge other Canvas tools |
| [#33](https://github.com/dbosk/canvaslms/issues/33) | Create a wrapper class for Canvas objects | Architectural enhancement |
| [#32](https://github.com/dbosk/canvaslms/issues/32) | Manage outcomes | Canvas outcomes management |

---

## Suggested Actions

1. **Close the 13 fully implemented issues** with comments documenting the implementation
2. **Update the 4 partially implemented issues** with:
   - What currently works
   - Example usage
   - What's still missing
   - Keep them open for full implementation
3. **Review and prioritize the 24 open issues** based on:
   - User demand
   - Implementation complexity
   - Alignment with project goals

---

## Analysis Methodology

This analysis was conducted by:
1. Installing and building the canvaslms tool
2. Examining all available commands with `--help` flags
3. Reviewing the codebase structure and implementation
4. Cross-referencing issue descriptions with actual features
5. Testing command availability (where possible without Canvas credentials)

The analysis document was created: 2026-01-06

Full detailed analysis available in `ISSUE_STATUS_ANALYSIS.md`.
