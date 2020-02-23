from ics import Calendar, Event
import requests
from datetime import datetime, time
from itertools import product
import arrow

date_range = (datetime(2019, 9, 30, 0, 0), datetime(2019, 10, 10, 0, 0))
time_range = (time(6, 0), time(19, 0))

adomas_url = "https://timetable.soton.ac.uk/Feed/Index/fIHGtdhnnOuh7EhjMXQpJnRDR6epdJ7dXwgeUFEmcXRFB-aSPSEL8_ePZ17eCvDjzen3DuMZKJOOcDRzUxM3rA2"
giorgio_url = "https://timetable.soton.ac.uk/Feed/Index/3F5CEtjYxzy3GoqHuz66AdH6zeQdZrrIFz8fMVBq9-iZOwA0W71GlsIbkmxtukoR36zSPs1OGxbnv5-YmyJ87g2"

adomas = Calendar(requests.get(adomas_url).text)
giorgio = Calendar(requests.get(giorgio_url).text)

l1 = list(adomas.timeline.included(arrow.get(date_range[0]), arrow.get(date_range[1])))
l2 = list(giorgio.timeline.included(arrow.get(date_range[0]), arrow.get(date_range[1])))
# l1 = list(adomas.timeline)
# l2 = list(giorgio.timeline)
# t = list(cal.timeline.at())
e = []
l = [l1, l2]

for i in range(len(l)):
    e.append([])
    for event in l[i]:
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

        e[i].append((begin, end))
    # print(e[i])

events = []


# union = []
# union(e[0],e[1])

def union(l1, l2):
    return [(min(s1, s2), max(e1, e2)) for (s1, e1), (s2, e2) in product(l1, l2) if s1 < e2 and e1 > s2]


overlap = union(e[0], e[1])

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