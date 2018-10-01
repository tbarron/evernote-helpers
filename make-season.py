"""
Usage:
    make-season [-d] YEAR SEASON
"""
import docopt
import pdb
import pexpect
from pprint import pprint
import time


ymdfmt = "%Y.%m%d"


# -----------------------------------------------------------------------------
def main():
    """
    - Compute the beginning of the specified season
    - Run make-day for each date in the season
    - Assemble the HTML to go in the season note
    - Write the HTML to a temp file
    - Call make-note with the name of the temp file
    """
    opts = docopt.docopt(__doc__)
    if opts["-d"]:
        pdb.set_trace()
    s_year = opts["YEAR"]
    s_season = opts["SEASON"]
    filename = "{}.{}.html".format(s_year, s_season)
    solquinox = start_date(s_year, s_season)
    prev_mon = previous_monday(solquinox)
    end_date = next_season(opts["YEAR"], opts["SEASON"])

    text = "<div id=\"en-note\"><div>\n"
    text += "<span style=\"font-family: &quot;Courier New&quot;;\">\n"
    # text += "               M     T     W     T     F     S     S"
    text += 10 * "&nbsp;"
    for wd in ["M", "T", "W", "T", "F", "S", "S"]:
        text += 5 * "&nbsp;" + wd
    current = prev_mon
    while current < end_date:
        text += "\n<br>" + current + ":"
        for day in range(0, 7):
            mday = month_day(current)
            cmd = "make-day {}".format(current)
            print(cmd)
            link = pexpect.run(cmd)
            link = link.decode().strip()
            text += 4 * "&nbsp;" + "<a href=\"{}\">{:02d}</a>".format(link, mday)
            current = succ_date(current)
    text += "</span></div></div>\n"
    with open(filename, 'w') as wbl:
        wbl.write(text)
    cmd = " ".join(["make-note --title \"{} {}\"".format(s_year, s_season),
                    "--tag {} --tag {} --html".format(s_year, s_season),
                    "--notebook \"Journal\" --file season-note.html --show"])
    pexpect.run(cmd)
    os.unlink(filename)


# -----------------------------------------------------------------------------
def epoch(ymd):
    """
    Return the epoch time of date *ymd* (yyyy.mmdd)
    """
    return time.mktime(time.strptime(ymd, ymdfmt))


# -----------------------------------------------------------------------------
def succ_date(ymd):
    """
    Compute and return the successor date for *ymd*
    """
    rval = time.strftime(ymdfmt, time.localtime(epoch(ymd) + 24*3600))
    return rval


# -----------------------------------------------------------------------------
def month_day(ymd):
    """
    Return the month day from date *ymd*
    """
    md = parcel(ymd)
    return md[2]


# -----------------------------------------------------------------------------
def next_season(year, season):
    """
    Return the date of the last Sunday in the season
    """
    (year, successor) = successor_season(year, season)
    next_ymd = start_date(year, successor)
    end_date = previous_monday(next_ymd)
    return end_date


# -----------------------------------------------------------------------------
def parcel(date):
    """
    Parse *date* (yyyy.mmdd) into a tm list
    """
    rval = time.strptime(date, ymdfmt)
    return rval


# -----------------------------------------------------------------------------
def pred_date(ymd):
    """
    Given *ymd* in yyyy.mmdd format, return the preceding date
    """
    rval = time.strftime(ymdfmt, time.localtime(epoch(ymd) - 24*3600))
    return rval


# -----------------------------------------------------------------------------
def previous_monday(ymd):
    """
    Given a date in ymd format, find the preceding Monday
    """
    rval = time.strftime(ymdfmt,
                         time.localtime(epoch(ymd) - weekday(ymd)*24*3600))
    return rval


# -----------------------------------------------------------------------------
def weekday(ymd):
    """
    Return the weekday of *ymd*
    """
    tm = parcel(ymd)
    return tm.tm_wday


# -----------------------------------------------------------------------------
def season_spring(year):
    """
    Return the spring equinox for the specified year 
    """
    return "{}.0320".format(year)


# -----------------------------------------------------------------------------
def season_summer(year):
    """
    Return the summer solstice for the specified year 
    """
    if year % 4 == 0:
        rval = "{}.0620".format(year)
    else:
        rval = "{}.0621".format(year)
    return rval


# -----------------------------------------------------------------------------
def season_fall(year):
    """
    Return the fall equinox for the specified year 
    """
    if year % 4 < 2:
        rval = "{}.0922".format(year)
    else:
        rval = "{}.0923".format(year)
    return rval


# -----------------------------------------------------------------------------
def season_winter(year):
    """
    Return the winter solstice for the specified year 
    """
    if year % 4 == 3:
        rval = "{}.1222".format(year)
    else:
        rval = "{}.1221".format(year)
    return rval


# -----------------------------------------------------------------------------
def start_date(year, season):
    """
    Compute the date of the solstice or equinox for the given season
    """
    gdir = globals()
    funcname = "season_{}".format(season)
    func = gdir[funcname]
    date = func(int(year))
    return date


# -----------------------------------------------------------------------------
def successor_season(year, season):
    succ_d = {"spring": "summer",
              "summer": "fall",
              "fall": "winter",
              "winter": "spring",
              }
    r_year = int(year)
    if season == "winter":
        r_year += 1
    r_season = succ_d[season]
    return(r_year, r_season)
    

# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
