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
    assert "2017.0101 " in result
    assert re.match("\d{4}\.\d{4}\s\d{2}:\d{2}:\d{2}", result)
