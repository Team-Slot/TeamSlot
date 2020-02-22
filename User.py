class User:
    def __init__(self, ical_url, id):
        self.ical_url = ical_url
        self.id = id

    @classmethod
    def from_message(cls, user_message):
        return cls(user_message.ical_url, user_message.id)
