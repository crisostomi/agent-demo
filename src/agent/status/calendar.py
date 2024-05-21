import calendar
from datetime import datetime


class Calendar:
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        self.events = {}

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

class CurrentCalendar:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrentCalendar, cls).__new__(cls)
            
        return cls._instance
    
    def set_calendar(self, calendar: Calendar):

        self._instance.calendar = calendar

    def get_calendar(self):
        return self._instance.calendar

    def __bool__(self):
        return self._instance is not None