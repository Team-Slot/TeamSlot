from ics import Calendar, Event
import requests
from datetime import datetime, time
from itertools import product
import arrow


def union(l1, l2):
    if not l1:
        return l2
    else:
        return [(min(s1, s2), max(e1, e2)) for (s1, e1), (s2, e2) in product(l1, l2) if s1 < e2 and e1 > s2]


def invert(l):
    inverted = []

    for i, (a, b) in enumerate(l):

        dt_start = datetime.combine(datetime.date(a), time_range[0])
        # print(dt_start)
        dt_end = datetime.combine(datetime.date(a), time_range[1])
        # print(dt_end)

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


def getAvailableBlocks(ical_links, date_range, time_range):
    cals = []  # list of calendars from iCal links
    for link in ical_links:
        cals.append(Calendar(requests.get(link).text).timeline.included(arrow.get(date_range[0]), arrow.get(date_range[1])))  # extract only dates within date_range defined in params

    blocks = []

    for i, cal in enumerate(cals):
        blocks.append([])
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

            blocks[i].append((begin, end))

    overlap = []
    for block_cal in blocks:
        # print(block_cal)
        overlap = union(overlap, block_cal)


    # todo : extend to more than two users
    return invert(overlap)
