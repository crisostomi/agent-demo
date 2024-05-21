from agent.status.calendar import Calendar
from langchain.tools import BaseTool, StructuredTool, tool

@tool 
def add_appointment_to_calendar(date, event):
    """
    Adds an appointment to the calendar with provided date, time and description.
    """
    calendar = Calendar()
    calendar.add_event(date, event)

    return f"Added appointment for {date} with description: {event}"

@tool
def remove_appointment_from_calendar(date, event):
    """
    Removes an appointment from the calendar with provided date.
    """
    calendar = Calendar()
    calendar.remove_event(date, event)

    return f"Removed event {event} for {date} "

@tool 
def list_all_events():
    """
    Lists all events in the calendar.
    """
    calendar = Calendar()
    return calendar.display_events()
