"""
Test Applescript/Evernote interaction code

Run this file with the command 'py.test'
"""
import pdb
import pytest
import re
import tbx


# -----------------------------------------------------------------------------
def test_count_notes_one():
    """
    The query string 'tag:current intitle:Start' should always find one note
    """
    pytest.dbgfunc()
    result = tbx.run("count-notes 'intitle:\"Start Here\"'")
    assert "notes: 1" in result.strip()


# -----------------------------------------------------------------------------
def test_count_notes_zero():
    """
    The query string 'tag:precious tag:delete_me' should never find a note
    """
    pytest.dbgfunc()
    result = tbx.run("count-notes 'tag:precious tag:delete_me'")
    assert "notes: 0" in result.strip()


# -----------------------------------------------------------------------------
def test_create_note():
    """
    The script new-note should create a new note with tags, title, and text
    specified on the command line.
    """
    pytest.dbgfunc()
    query = "'tag:test_create_note tag:delete_me intitle:Test'"
    result = tbx.run("count-notes {}".format(query)).strip()
    found = re.findall(r"notes: (\d+)", result)
    count = int(found.pop())
    if 0 < count:
        result = tbx.run("del-notes -m {}".format(query)).strip()
        found = re.findall(r"(\d+) notes deleted", result)
        deleted = int(found.pop())
        if count != deleted:
            msg = "Should have deleted {} but only got {}"
            msg = msg.format(count, deleted)
            pytest.fail(msg)

    cmd = ("make-note --title 'Test Note' --text 'this is a test' "
           "--tag 'test_create_note' --tag 'delete_me'")
    result = tbx.run(cmd)
    assert "note Test Note created" in result

    cmd = "count-notes {}".format(query)
    result = tbx.run(cmd)
    assert "notes: 1" in result

    cmd = "del-notes {}".format(query)
    result = tbx.run(cmd)
    assert "1 notes deleted" in result


# -----------------------------------------------------------------------------
def test_del_notes_nomatch():
    """
    If del-notes matches no notes, it should report 'no notes match'
    """
    pytest.dbgfunc()
    cmd = "del-notes 'tag:no_such_note'"
    result = tbx.run(cmd)
    assert "no notes match tag:no_such_note" in result


# -----------------------------------------------------------------------------
def test_del_notes_nomult():
    """
    Create two notes with tags 'testing' and 'delete_me'. Attempt to delete
    them without -m option, should fail. Attempt to delete them with -m option,
    should succeed.
    """
    pytest.dbgfunc()
    cmd = "make-note --tag 'testing' --tag 'delete_me' --title "
    result = tbx.run(cmd + "'test note 1'")
    assert "note test note 1 created" in result
    result = tbx.run(cmd + "'test note 2'")
    assert "note test note 2 created" in result

    result = tbx.run("del-notes 'tag:testing tag:delete_me'")
    assert "no notes deleted, --multiple required" in result

    result = tbx.run("del-notes -m 'tag:testing tag:delete_me'")
    assert "2 notes deleted" in result


# -----------------------------------------------------------------------------
def test_make_date_basic():
    """
    make-date with arg '2017.0101' should work
    """
    pytest.dbgfunc()
    result = tbx.run("make-date 2017.0101")
    assert "result = " not in result
    assert "2017.0102" in result
    assert re.match(r"\d{4}\.\d{4}\.\S\S\S", result)


# -----------------------------------------------------------------------------
def test_make_date_hhmm():
    """
    make-date with arg '2017.0217 13:29' should work
    """
    pytest.dbgfunc()
    result = tbx.run("make-date '2017.0217 13:29'")
    assert "result = " not in result
    assert re.match(r"2017\.0218\.sat", result)


# -----------------------------------------------------------------------------
def test_make_date_hhmmss():
    """
    make-date with arg '2017.0430 13:29:57' should work
    """
    pytest.dbgfunc()
    result = tbx.run("make-date '2017.0430 13:29:57'")
    assert "result = " not in result
    assert re.match(r"2017\.0501\.mon", result)


# -----------------------------------------------------------------------------
def test_make_date_noarg():
    """
    make-date with no arg spits out an error
    """
    pytest.dbgfunc()
    result = tbx.run("make-date")
    assert "execution error:" in result
    assert "t get item 1 of {}." in result


# -----------------------------------------------------------------------------
def test_make_date_wkday():
    """
    the output of make-date should be '2017.0606.tue'
    """
    pytest.dbgfunc()
    result = tbx.run("make-date '2017.0606'")
    assert "result = " not in result
    assert re.match(r"2017\.0607\.wed", result)


# -----------------------------------------------------------------------------
def test_releasable():
    """
    The output of version should match the latest git tag
    """
    pytest.dbgfunc()
    staged, changed, untracked = tbx.git_status()
    assert untracked == [], "You have untracked files"
    assert changed == [], "You have unstaged updates"
    assert staged == [], "You have updates staged but not committed"

    if tbx.git_current_branch() != "master":
        return True

    last_tag = tbx.git_last_tag()

    msg = "Version ({}) does not match tag ({})"
    result = tbx.run("version").decode().rstrip()
    msg = msg.format(result, last_tag)
    assert result == last_tag, msg

    assert tbx.git_hash() == tbx.git_hash(last_tag), "Tag != HEAD"
