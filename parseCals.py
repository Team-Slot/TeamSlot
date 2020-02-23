from ics import Calendar, Event
import requests
from datetime import datetime, time
from itertools import product
import arrow

# Take two lists of datetime tuples and returns the union
def union(l1, l2):
    if not l1:
        return l2
    else:
        return [(min(s1, s2), max(e1, e2)) for (s1, e1), (s2, e2) in product(l1, l2) if s1 < e2 and e1 > s2]

# Takes a list of datetime tuples and returns the inversion within a capped time range
# Used to convert list of unavailable times into available times within working hours
def invert(l, timeRange):
    inverted = []

    # Enumerate through list to build new datetimes
    for i, (a, b) in enumerate(l):

        # Calculates available block boundaries from current list item and caps
        dt_start = datetime.combine(datetime.date(a), timeRange[0])
        dt_end = datetime.combine(datetime.date(a), timeRange[1])

        # Invert datetime to available blocks and append
        if (i == 0 and a > dt_start) or datetime.date(l[i - 1][0]) != datetime.date(a):
            inverted.append((dt_start, a))
        elif (i == len(l) - 1 and b < dt_end) or datetime.date(l[i + 1][0]) != datetime.date(a):
            inverted.append((b, dt_end))
        else:
            e = l[i][1]  # this end
            s = l[i + 1][0]  # next start
            delta = s - e
            if delta:
                inverted.append((e, s))

    return inverted

# Parse and extract cals, return available blocks
def getAvailableBlocks(ical_links, date_range, time_range):
    # Build list of calendars of events
    cals = []  # list of calendars from iCal links

    # Iterative through each user's ical link
    for link in ical_links:
        # Append calendar, extracting only dates within given date_range
        cals.append(Calendar(requests.get(link).text).timeline.included(arrow.get(date_range[0]), arrow.get(date_range[1])))

    # Build list of datetime tuples from calendar events
    dt_blocks = []

    for i, cal in enumerate(cals):
        dt_blocks.append([])
        for event in cal:
            begin = datetime.fromtimestamp(event.begin.timestamp)
            end = datetime.fromtimestamp(event.end.timestamp)

            dt_start = datetime.combine(datetime.date(begin), time_range[0])
            dt_end = datetime.combine(datetime.date(begin), time_range[1])

            if begin < dt_start:
                if end > dt_start:
                    begin = dt_start
                else:
                    continue
            elif end > dt_end:
                if begin < dt_end:
                    end = dt_end
                else:
                    break

            dt_blocks[i].append((begin, end))

    # Take the union of tuples, combining unavailable blocks
    overlap = []
    for block_cal in dt_blocks:
        overlap = union(overlap, block_cal)


    return invert(overlap,time_range)
