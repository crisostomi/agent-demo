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
        """Adds an event on a specific day."""
        if day not in self.events:
            self.events[day] = []
        self.events[day].append(event)

    def remove_event(self, day, event):
        """Removes an event from a specific day."""
        if day in self.events and event in self.events[day]:
            self.events[day].remove(event)
            if not self.events[day]:  # Remove the day if no events left
                del self.events[day]

    def display_month(self):
        """Displays the calendar for the month."""
        cal = calendar.TextCalendar(calendar.SUNDAY)
        month_str = cal.formatmonth(self.year, self.month)
        print(month_str)

    def display_events(self):
        """Displays all the events in the calendar."""
        for day in sorted(self.events.keys()):
            print(f"Day {day}:")
            for event in self.events[day]:
                print(f"  - {event}")

    def get_events(self, day):
        """Returns all events on a specific day."""
        return self.events.get(day, [])

