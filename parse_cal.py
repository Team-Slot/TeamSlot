from ics import Calendar, Event
import requests
from datetime import datetime, time
from itertools import product
import arrow

date_range = (datetime(2019, 9, 30, 0, 0), datetime(2019, 10, 10, 0, 0)) # hard-coded test date range
time_range = (time(6, 0), time(19, 0)) # hard-coded test time range

def union(l1, l2):
    return [(min(s1, s2), max(e1, e2)) for (s1, e1), (s2, e2) in product(l1, l2) if s1 < e2 and e1 > s2]

def get_available_blocks(users, date_range, time_range):
    cals = [] # list of calendars from iCal links
    for user in users:
        cals.append(Calendar(requests.get(user.ical_url).text).timeline.included(arrow.get(date_range[0]), arrow.get(date_range[1]))) # extract only dates within date_range defined in params

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


# test below:

adomas_url = "https://timetable.soton.ac.uk/Feed/Index/fIHGtdhnnOuh7EhjMXQpJnRDR6epdJ7dXwgeUFEmcXRFB-aSPSEL8_ePZ17eCvDjzen3DuMZKJOOcDRzUxM3rA2"
giorgio_url = "https://timetable.soton.ac.uk/Feed/Index/3F5CEtjYxzy3GoqHuz66AdH6zeQdZrrIFz8fMVBq9-iZOwA0W71GlsIbkmxtukoR36zSPs1OGxbnv5-YmyJ87g2"

adomas = Calendar(requests.get(adomas_url).text)
giorgio = Calendar(requests.get(giorgio_url).text)

cal1 = list(adomas.timeline.included(arrow.get(date_range[0]), arrow.get(date_range[1])))
cal2 = list(giorgio.timeline.included(arrow.get(date_range[0]), arrow.get(date_range[1])))

blocks = []
cals = [cal1, cal2]

for i, cal in enumerate(cals):
    blocks.append([])
    for event in cal:
        begin = datetime.fromtimestamp(event.begin.timestamp)
        end = datetime.fromtimestamp(event.end.timestamp)

        dt_start = datetime.combine(datetime.date(begin), time_range[0])
        # print(dt_start)
        dt_end = datetime.combine(datetime.date(begin), time_range[1])
        # print(dt_end)

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
    # print(e[i])


overlap = union(blocks[0], blocks[1])

for a in overlap:
    print(a)

def invert(l):
    inverted = []

    for i,(a,b) in enumerate(l):

        dt_start = datetime.combine(datetime.date(a), time_range[0])
        # print(dt_start)
        dt_end = datetime.combine(datetime.date(a), time_range[1])
        # print(dt_end)

        if (i == 0 and a > dt_start) or datetime.date(l[i-1][0]) != datetime.date(a):
            inverted.append((dt_start, a))
        elif (i == len(l)-1 and b < dt_end) or datetime.date(l[i+1][0]) != datetime.date(a):
            inverted.append((b, dt_end))
        else:
            e = l[i][1] # this end
            s = l[i+1][0] # next start
            delta = s - e
            if delta:
                inverted.append((e,s))

    return inverted

final = invert(overlap)


print("\n")
for b in final:
    print(b)

# print(e, "\n")