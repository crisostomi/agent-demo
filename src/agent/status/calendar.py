import calendar
from datetime import datetime

class SingletonMeta(type):
    """
    A Singleton metaclass. Ensures only one instance of the class exists.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Calendar(metaclass=SingletonMeta):
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.events = {}  # Dictionary to hold events

        
    def add_event(self, day, event):
        if day not in self.events:
            self.events[day] = []
        self.events[day].append(event)

    def remove_event(self, day, event):
        if day in self.events and event in self.events[day]:
            self.events[day].remove(event)
            if not self.events[day]:
                del self.events[day]

    def display_month(self):
        cal = calendar.HTMLCalendar(calendar.SUNDAY)
        return cal.formatmonth(self.year, self.month)

    def get_events(self, day):
        return self.events.get(day, [])
