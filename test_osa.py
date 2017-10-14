import pexpect
import re


# -----------------------------------------------------------------------------
def test_make_date_noarg():
    """
    make-date with no arg spits out an error
    """
    result = pexpect.run("make-date")
    assert "execution error:" in result.decode()
    assert "t get item 1 of {}." in result.decode()


# -----------------------------------------------------------------------------
def test_make_date_basic():
    """
    make-date with arg '2017.0101' should work
    """
    result = pexpect.run("make-date 2017.0101")
    result = result.decode()
    assert "result = " not in result
    assert "2017.0101" in result
    assert re.match("\d{4}\.\d{4}\.\S\S\S", result)


# -----------------------------------------------------------------------------
def test_make_date_hhmm():
    """
    make-date with arg '2017.0217 13:29' should work
    """
    result = pexpect.run("make-date '2017.0217 13:29'")
    result = result.decode()
    assert "result = " not in result
    assert re.match("2017\.0217\.fri", result)


# -----------------------------------------------------------------------------
def test_make_date_hhmmss():
    """
    make-date with arg '2017.0430 13:29:57' should work
    """
    result = pexpect.run("make-date '2017.0430 13:29:57'")
    result = result.decode()
    assert "result = " not in result
    assert re.match("2017\.0430\.sun", result)


# -----------------------------------------------------------------------------
def test_make_date_wkday():
    """
    the output of make-date should be '2017.0606.tue'
    """
    result = pexpect.run("make-date '2017.0606'")
    result = result.decode()
    assert "result = " not in result
    assert re.match("2017\.0606\.tue", result)


# -----------------------------------------------------------------------------
def test_count_notes_one():
    """
    The query string 'tag:current intitle:Start' should always find one note
    """
    result = pexpect.run("count-notes 'tag:current intitle:Start'")
    assert "notes: 1\r\n" in result.decode()


# -----------------------------------------------------------------------------
def test_count_notes_zero():
    """
    The query string 'tag:precious tag:delete_me' should never find a note
    """
    result = pexpect.run("count-notes 'tag:precious tag:delete_me'")
    assert "notes: 0\r\n" in result.decode()


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
    assert "0 notes deleted, -m option required" in result.decode()

    result = pexpect.run("del-notes -m 'tag:testing tag:delete_me'")
    assert "2 notes deleted" in result.decode()


# -----------------------------------------------------------------------------
def test_create_note():
    """
    The script new-note should create a new note with tags, title, and text
    specified on the command line.
    """
    cmd = ("create-note --title 'Test Note' --text 'this is a test' "
           "--tag 'testing' --tag 'delete_me'")
    result = pexpect.run(cmd)
    assert "note Test Note created" in result.decode()

    result = pexpect.run("count-notes 'tag:testing tag:delete_me intitle:Test'")
    assert "notes: 1\r\n" in result.decode()
