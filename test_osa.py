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
