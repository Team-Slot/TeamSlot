from ics import Calendar, Event
import requests
from datetime import datetime, time, timedelta
import arrow


# separate blocks of time into one hour segments
def split(blocks):
    splitBlocks = []
    for block in blocks:
        blockStart = block[0]
        blockEnd = block[1]

        duration = blockEnd.hour - blockStart.hour

        if duration > 1:
            for i in range(0, duration):
                time = blockStart + timedelta(hours=i)

                splitBlocks.append((time, time + timedelta(hours=1)))
        else:
            splitBlocks.append(block)

    return splitBlocks


# allows iteration over consecutive date (datetime.date) objects
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


# fill a range of time (given in preferences) with one-hour segments
def fillDuration(dateRange, timeRange):
    filled = []

    for date in daterange(dateRange[0], dateRange[1]):
        for i in range(timeRange[1].hour - timeRange[0].hour):
            filled.append((datetime.combine(datetime.date(date), timeRange[0]) + timedelta(hours=i),
                           datetime.combine(datetime.date(date), timeRange[0]) + timedelta(hours=i + 1)))

    return filled


# remove list from filled set of blocks
def subtract(filled, l):
    splitL = split(l)
    subbed = filled - set(splitL)
    return subbed


# Parse and extract cals, return available blocks
def getAvailableBlocks(ical_links, date_range, time_range):
    # Build list of calendars of events
    cals = []  # list of calendars from iCal links

    # Iterative through each user's ical link
    for link in ical_links:
        # Append calendar, extracting only dates within given date_range
        cals.append(
            Calendar(requests.get(link).text).timeline.included(arrow.get(date_range[0]), arrow.get(date_range[1])))

    # Build list of datetime tuples from calendar events
    dt_blocks = []

    # convert each ical link into calendar
    for i, cal in enumerate(cals):
        dt_blocks.append([])
        for event in cal:
            begin = datetime.fromtimestamp(event.begin.timestamp)
            end = datetime.fromtimestamp(event.end.timestamp)

            dt_blocks[i].append((begin, end))

    final = set(fillDuration(date_range, time_range))

    # subtract each user's calendar from the filled timeline
    for blocks in dt_blocks:
        final = subtract(final, blocks)

    # for f in sorted(final):
    #     print(f)

    return list(final)
