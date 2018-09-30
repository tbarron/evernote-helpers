# Changelog

Notable changes for this project. This project follows the conventions
described at

  * [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
  * [Semantic Versioning](https://semver.org/), and
  * [Simple Release Cycle](https://tinyurl.com/ycyjojez)


Each release header has the following format:

    [VERSION] / release date / title (branch, tag)

VERSION has the format <MAJOR>.<MINOR>.<PATCH>, where each component is a
number. The release date is in ISO format (yyyy-mm-dd). No time is provided
for a change since it would be very difficult or impossible to record the
time of the git commit in the changelog. The title describes the overall
update made with this release. The tag is a short marker that begins each
of the releated commit messages.

## [Unreleased] / yyyy-mm-dd / Title (branch, TAG)

 - Update make-day so that it makes a new note and also emits the link to
   that note.
 - Rename create-note to make-note.
 - Update README.md and CHANGELOG.md with links to Keep a Changelog,
   Semantic Versioning, and Simple Release Cycle

### Additions
 - Add 'clean' target to Makefile for removing generated files, emacs
   backup files, etc.


## [0.6.5] / 2018-09-13 / Eliminate pexpect (tweaks, TW)
### Changes
 - Whitespace adjustments in CHANGELOG.md
 - Support ad hoc debugging in all tests
 - Replace pexpect.run() with tbx.run(), remove pexpect import


## [0.6.4] / 2018-09-13 / Bullet-proof test_create_note (cnote, CN)
### Changes
 - In test_create_note(), check whether (one or more instances of) the test
   note exists and, if so, delete them before attempting the actual test


## [0.6.3] / 2018-09-13 / Releasability test (releasable, RL)
### Additions
 - Add file requirements.txt
 - Add file conftest.py to support ad hoc debugging in tests

### Changes
 - Rename test_release() to test_releasable(), updated it using tbx
   functions based on how it's coded in the tbx project (checks for
   untracked files, unstaged updates, uncommitted updates, and, if the
   current branch is 'master', that the last tag matches the current
   version and the hash of HEAD matches the hash of the last tag).


## [0.6.2] / 2018-09-12 / README.md updates (readme, RD)
### Additions
 - Add missing info to README.md


## [0.6.1] / 2018-09-12 / Changelog and Semantic Versioning (changelog, CL)
### Added
 - Add CHANGELOG.md describing updates to the project over time
 - Add version, VERSION.txt, test_release() in test_osa.py to track
   project version

### Changed
 - Update tests to make them work -- putting them in alphabetical order,
   updating them for python3.6, etc.
 - Document release process in README.md


## [0.6.0] / 2018-07-16 / Conflict note consolidation
### Added
 - Add script consolidate-conflicts to move conflict notes into a single
   notebook, turn on its execute bit

### Changed
 - In daily-twiddle, if no note exists for current day, throw an error
   message
 - Update README.md with missing info


## [0.5.5] / 2018-06-10 / Create finances page for week
### Changed
 - Update make-week to create finances page for the week


## [0.5.4] / 2018-01-09 / Improved library search strategy
### Changed
 - Improve library search strategy. Rather than looking for the library in
   the current working directory, all the scripts that use it will now look
   for it in the directory where they live (i.e.,
   ~/prj/github/evernote_helpers)


## [0.5.3] / 2017-12-23 / Format README with Markdown
### Changed
 - Update README to README.md and edit its content into markdown


## [0.5.2] / 2017-12-15 / No 'experimental' tag
### Changed
 - Stop putting experimental tag on new pages in make-week


## [0.5.1] / 2017-11-05 / Keep window open
### Changed
 - Don't close yesterday's window


## [0.5.0] / 2017-11-04 / make-todo, daily-twiddle
### Changed
 - daily-twiddle
     - Make a list of notes matching yesterday
     - Make a list of notes matching today
     - Use the yesterday and today lists to update the notes
     - Activate evernote to surface today's note

### Added
 - make-todo
     - Add new file to git
     - Add newline to end of file


## [0.4.1] / 2017-10-28 / Update make-day, ymd-title
### Changed
 - Update ymd-title to increment note count in prompt mode
 - Update make-day to use duplicate_note


## [0.4.0] / 2017-10-18 / ymd-title, Idempotent utility routines
### Added
 - Add ymd_format to library to support ymd-title
 - Add script ymd-title: if note title already starts with yyyy.mmdd, do
   nothing, otherwise add note create date to the title in format
   'yyyy.mmdd: '

### Changed
 - Move safe utility routines for tagging notes (safe-addtag, safe-rmtag)
   from daily-twiddle to library
 - Update daily-twiddle to use library routines safe-{add,rm}tag


## [0.3.0] / 2017-10-17 / make-day, library rebuild ability
### Added
 - Add lines to Makefile to rebuild library.scpt from library
 - Add make-day (creates a specific day's diary note)


## [0.2.1] / 2017-10-16 / make-week templates
### Added
 - Add README documenting the various commands: add-tags, count-notes,
   create-note, del-notes, make-date, make-next-week, Makefile,
   note-exists, rm-tags, show-notes, library
 - Add more stuff to .gitignore

### Changed
 - Improvements to make-week
     - Add arguments 'next' and yyyy.mmdd, and option --overwrite
     - Make new weeks from template notes in evernote, one for each weekday
       (rather than using the same template for all days)


## [0.2.0] / 2017-10-15 / Daily twiddle, zero padding
### Added
 - Add zpad function for zero padding months and days
 - Add daily-twiddle

### Changed
 - Complete make-next-week


## [0.1.0] / 2017-10-14 / Development
### Added
 - Add ignorable stuff to .gitignore
 - Applescript commands and tests: count-notes, new-note, create-note,
   del-notes, make-next-week
 - Add --show to create-note


## [0.0.0] / 2017-10-13 / Getting started
### Added
 - Inception
 - Set things up -- py.test, utility functions, etc.
