from ics import Calendar, Event
import requests

url = "https://timetable.soton.ac.uk/Feed/Index/fIHGtdhnnOuh7EhjMXQpJnRDR6epdJ7dXwgeUFEmcXRFB-aSPSEL8_ePZ17eCvDjzen3DuMZKJOOcDRzUxM3rA2"

cal = Calendar(requests.get(url).text)

# print(cal)
# print(cal.events)

l = list(cal.timeline)

Event()

e = l[0]
# print(e, "\n")

print(e.begin)
print(e.name)