from datetime import datetime, time, timedelta
from Database import Database
from Options import Options
from availableTimes import getSlots
from parseCals import getAvailableBlocks


class ScheduleCore:
    def __init__(self):
        self.database = Database()
        self.options = None

    def addUser(self,userid, calURL):
        self.database.addUser(userid, calURL)

    def updateUser(self, userid, newCalURL):
        self.database.updateUser(userid, newCalURL)

    # Processes incoming requests to schedule
    def processRequest(self, users, dateRange, workingHours, meetingLength, description, idealHours = (9,17)):
        # Gather calendar URLs from userids
        calURLS = []

        for user in users:
            calURLS.append(self.database.getCal(user))

        # Parse calendar URLS to extract available blocks
        availableBlocks = getAvailableBlocks(calURLS, dateRange, workingHours)

        # Split blocks into meeting slots, categorised by priority
        slots = getSlots(availableBlocks, meetingLength, (idealHours[0], idealHours[1]) )

        idealSlots = slots[0]
        otherSlots = slots[1]

        # Instantiate Options class to handle selecting options to send
        self.options = Options(idealSlots, otherSlots)
        self.description = description

        # Send first options
        return self.options.getOptions()

    def getMoreOptions(self):
        return self.options.getOptions()

    def getFinalSlot(self, unavailableSlots):
        possibleSlots = self.getOptions() - set(unavailableSlots)

        if possibleSlots:
            return possibleSlots[0]
        else:
            return None

# date_range = (datetime(2019, 9, 30, 0, 0), datetime(2019, 10, 10, 0, 0))  # hard-coded test date range
# time_range = (time(6, 0), time(19, 0))  # hard-coded test time range
#
# sc = ScheduleCore()
# three = sc.processRequest([1,2], date_range, time_range, timedelta(hours=1), 'random')
#
# for o in three:
#     print(o)