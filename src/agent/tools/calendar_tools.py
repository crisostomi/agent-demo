from agent.status.calendar import Calendar, CurrentCalendar
from langchain.tools import BaseTool, StructuredTool, tool
from flask import Flask, request, render_template_string, redirect, url_for

@tool 
def add_event_to_calendar(day, event):
    """
    Adds an event to the calendar with provided day of the month (from 1 to 31) and description.
    """
    calendar = CurrentCalendar().get_calendar()
    calendar.add_event(day, event)

    return f"Added appointment for {day} with description: {event}"

@tool
def remove_event_from_calendar(day, event):
    """
    Removes an appointment from the calendar with provided day of the month (from 1 to 31).
    """
    calendar = CurrentCalendar().get_calendar()

    calendar.remove_event(day, event)

    return f"Removed event {event} for {day} "

@tool 
def list_all_events():
    """
    Lists all events in the calendar.
    """
    calendar = CurrentCalendar().get_calendar()
    return calendar.display_events()


