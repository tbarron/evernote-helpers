
# README: Evernote Helpers
Last updated: <2018.0912 08:02:07>

## Introduction

This directory contains Applescript code for manipulating stuff in my
Evernote account. There is a python program that uses the Evernote OAUTH
mechanism for accessing Evernote online, but that turned out to be less
useful than expected (see "Reasons to prefer Applescript over Python"
below).

## Contents

 * add-tags:
    * Assign a (set of) tags to a (set of) notes

 * consolidate-conflicts
    * Collect any notes from conflict notebooks into a single notebook and
      delete all the dated conflict notebooks

 * count-notes:
    * Count the Evernote notes that match a given query string

 * create-note:
    * Create a new note based on the command line args

 * daily-twiddle:
    * Shift tags on notes for today and yesterday

 * del-notes:
    * Delete notes that match a specified query string

 * library:
    * Utility functions used by other scripts

 * make-date:
    * Date manipulation code for testing and examples

 * make-day:
    * Create a day note based on the relevant template

 * make-week:
    * Create a week's worth of diary notes

 * Makefile:
    * Command for regenerating library.scpt from library

 * note-exists:
    * Checks whether a specified query string matches at least one note

 * README:
    * This file

 * rm-tags:
    * Remove a (set of) tags from a (set of) notes

 * show-notes:
    * Display a set of notes

 * test_osa.py:
    * Test Applescript/Evernote interaction code

## The Python Experiment

I tried using python to manipulate Evernote. The code is in etool.py. That
requires using oauth authentication and authorization. etool has a
'get_token' function that lets you interact with Evernote to authorize the
app and generate an API key that can then be used for a specified time
period to access the account on behalf of the user.

Other functions include create_notebook (incomplete), list_notes, and
list_notebooks.

### The 'cred' file

The cred file has the following format:

        [basic]
        key: <consumer-key>
        secret: <consumer-secret>
        token: <API-token>

        [full]
        key: <consumer-key>
        secret: <consumer-secret>
        token: <API-token>

The first stanza allows basic access, which creating notebooks and notes
but does not support examining or manipulating existing notes. The second
stanza provides full access. In each case, the key and secret are obtained
from the Evernote website in a manual interaction and then used to request
an API token with the etool get_token function.

### Reasons to prefer Applescript over Python

 * Applescript carries out Evernote interactions directly on the local
   machine and doesn't need to be authenticated. Synchronization with the
   cloud version is left to Evernote itself.

 * Applescript is not subject to the bandwidth limits Evernote imposes on
   online applications because it does its work locally.

 * Python interactions require internet access. Applescript interactions do
   not.

 * Using oauth on Evernote for full access to production requires
   justifying the level of access your app requires. With Applescript, all
   the functions are immediately available without having to justify
   anything to anybody.


### Release Process

  * Checkout the current master branch to a child branch with a meaningful
    name.
  * Make changes to the child branch until it is ready to be the next
    release.
  * Once all changes are complete,
      * Update CHANGELOG.md to reflect the updates.
      * Update the file VERSION.txt to reflect the new version.
      * Make an annotated version tag on the last commit in the work
        branch. Put the text of the CHANGELOG.md entry in the description
        of the new tag.
      * Verify that all tests pass.
  * Checkout master and merge the work branch.
  * Push master to the origin.


### References

  * [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
  * [Semantic Versioning](https://semver.org/)
