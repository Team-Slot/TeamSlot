class UserMessage:
    def __init__(self, ical_url, id):
        self.ical_url = ical_url
        self.id = id


class ScheduleRequestMessage:
    def __init__(self, length, date_range, time_range, ideal_days=0, ideal_times=0):
        self.length = length
        self.date_range = date_range
        self.time_range = time_range
        self.ideal_days = ideal_days
        self.ideal_times = ideal_times