from ics import Calendar, Event
import requests
from datetime import datetime, time
from itertools import product
import arrow

from operator import itemgetter

from itertools import product


def consolidate(intervals):
    sorted_intervals = sorted(intervals, key=itemgetter(0))

    if not sorted_intervals:  # no intervals to merge
        return

    # low and high represent the bounds of the current run of merges
    low, high = sorted_intervals[0]

    for iv in sorted_intervals[1:]:
        if iv[0] <= high:  # new interval overlaps current run
            high = max(high, iv[1])  # merge with the current run
        else:  # current run is over
            yield low, high  # yield accumulated interval
            low, high = iv  # start new run

    yield low, high  # end the final run

# Take two lists of datetime tuples and returns the union
def union(l1, l2):
    # if not l1:
    #     return l2
    # else:
    # return [(min(s1, s2), max(e1, e2)) for (s1, e1), (s2, e2) in product(l1, l2) if s1 <= e2 and e1 >= s2]

    return consolidate([*l1, *l2])


# Takes a list of datetime tuples and returns the inversion within a capped time range
# Used to convert list of unavailable times into available times within working hours
def invert(l, timeRange):
    inverted = []

    # Enumerate through list to build new datetimes
    for i, (a, b) in enumerate(l):
        # print(a,b)

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

    # print("\n")
    # print(inverted)
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

    # print(dt_blocks[0], "\n")
    # print(dt_blocks[1], "\n")

    # Take the union of tuples, combining unavailable blocks
    overlap = list(union(dt_blocks[0], dt_blocks[1]))
    # for block_cal in dt_blocks:
    #     overlap = union(overlap, block_cal)
    #     print("\n", block_cal)
    #     print("\n overlap:", overlap)

    # for a in overlap:
    #     print(a)

    # print("\n", overlap)

    # overlap = []
    # for e in overlap:
    #     print("overlap: ", e)

    # overlap = [(datetime(2020, 2, 24, 10, 0), datetime(2020, 2, 24, 17, 0)), (datetime(2020, 2, 25, 9, 0), datetime(2020, 2, 25, 12, 0))]

    invert(overlap, time_range)

    return invert(overlap, time_range)
