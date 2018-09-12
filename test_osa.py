"""
Test Applescript/Evernote interaction code

Run this file with the command 'py.test'
"""
import pexpect
import re


# -----------------------------------------------------------------------------
def test_count_notes_one():
    """
    The query string 'tag:current intitle:Start' should always find one note
    """
    result = pexpect.run("count-notes 'intitle:\"Start Here\"'")
    assert "notes: 1\r\n" in result.decode()


# -----------------------------------------------------------------------------
def test_count_notes_zero():
    """
    The query string 'tag:precious tag:delete_me' should never find a note
    """
    result = pexpect.run("count-notes 'tag:precious tag:delete_me'")
    assert "notes: 0\r\n" in result.decode()


# -----------------------------------------------------------------------------
def test_create_note():
    """
    The script new-note should create a new note with tags, title, and text
    specified on the command line.
    """
    cmd = ("create-note --title 'Test Note' --text 'this is a test' "
           "--tag 'test_create_note' --tag 'delete_me'")
    result = pexpect.run(cmd)
    assert "note Test Note created" in result.decode()

    cmd = "count-notes 'tag:test_create_note tag:delete_me intitle:Test'"
    result = pexpect.run(cmd)
    assert "notes: 1\r\n" in result.decode()

    cmd = "del-notes 'tag:test_create_note tag:delete_me intitle:Test'"
    result = pexpect.run(cmd)
    assert "1 notes deleted" in result.decode()


# -----------------------------------------------------------------------------
def test_del_notes_nomatch():
    """
    If del-notes matches no notes, it should report 'no notes match'
    """
    cmd = "del-notes 'tag:no_such_note'"
    result = pexpect.run(cmd)
    assert "no notes match tag:no_such_note" in result.decode()


# -----------------------------------------------------------------------------
def test_del_notes_nomult():
    """
    Create two notes with tags 'testing' and 'delete_me'. Attempt to delete
    them without -m option, should fail. Attempt to delete them with -m option,
    should succeed.
    """
    cmd = "create-note --tag 'testing' --tag 'delete_me' --title "
    result = pexpect.run(cmd + "'test note 1'")
    assert "note test note 1 created" in result.decode()
    result = pexpect.run(cmd + "'test note 2'")
    assert "note test note 2 created" in result.decode()

    result = pexpect.run("del-notes 'tag:testing tag:delete_me'")
    assert "no notes deleted, --multiple required" in result.decode()

    result = pexpect.run("del-notes -m 'tag:testing tag:delete_me'")
    assert "2 notes deleted" in result.decode()


# -----------------------------------------------------------------------------
def test_make_date_basic():
    """
    make-date with arg '2017.0101' should work
    """
    result = pexpect.run("make-date 2017.0101")
    result = result.decode()
    assert "result = " not in result
    assert "2017.0102" in result
    assert re.match(r"\d{4}\.\d{4}\.\S\S\S", result)


# -----------------------------------------------------------------------------
def test_make_date_hhmm():
    """
    make-date with arg '2017.0217 13:29' should work
    """
    result = pexpect.run("make-date '2017.0217 13:29'")
    result = result.decode()
    assert "result = " not in result
    assert re.match(r"2017\.0218\.sat", result)


# -----------------------------------------------------------------------------
def test_make_date_hhmmss():
    """
    make-date with arg '2017.0430 13:29:57' should work
    """
    result = pexpect.run("make-date '2017.0430 13:29:57'")
    result = result.decode()
    assert "result = " not in result
    assert re.match(r"2017\.0501\.mon", result)


# -----------------------------------------------------------------------------
def test_make_date_noarg():
    """
    make-date with no arg spits out an error
    """
    result = pexpect.run("make-date")
    assert "execution error:".encode() in result
    assert "t get item 1 of {}.".encode() in result


# -----------------------------------------------------------------------------
def test_make_date_wkday():
    """
    the output of make-date should be '2017.0606.tue'
    """
    result = pexpect.run("make-date '2017.0606'")
    result = result.decode()
    assert "result = " not in result
    assert re.match(r"2017\.0607\.wed", result)


# -----------------------------------------------------------------------------
def test_release():
    """
    The output of version should match the latest git tag
    """
    gstat = pexpect.run("git status --porc").decode()
    assert gstat.strip() == "", "uncommitted files"

    with open("VERSION.txt", 'r') as rbl:
        exp = rbl.read().strip()

    gtags = pexpect.run("git --no-pager tag").decode()
    ftag = gtags.split()[-1]
    assert exp == ftag, "not releasable"

    result = pexpect.run("version").decode()
    assert exp.rstrip() in result, "version function is broken"
