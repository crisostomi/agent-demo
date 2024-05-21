from langchain.tools import BaseTool, StructuredTool, tool

@tool 
def add_appointment_to_calendar(date, time, description):
    """
    Adds an appointment to the calendar with provided date, time and description.
    """
    # TODO: implement calendar logic 
    # calendar = get_calendar()
    # calendar.add_appointment(date, time, description)

    return f"Added appointment for {date} at {time} with description: {description}"


def remove_appointment_from_calendar(date, time):
    """
    Removes an appointment from the calendar with provided date and time.
    """
    # TODO: implement calendar logic
    # calendar = get_calendar()
    # calendar.remove_appointment(date, time)
    return f"Removed appointment for {date} at {time}"