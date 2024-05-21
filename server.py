from datetime import datetime
from pathlib import Path
from agent.status.config import Config
from agent.status.calendar import Calendar
from agent.tools.calendar_tools import add_appointment_to_calendar, list_all_events, remove_appointment_from_calendar
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.tools.tavily_search import TavilySearchResults
from flask import Flask, request, render_template_string

from flask import Flask, request, jsonify
from flask_cors import CORS
import atexit
import omegaconf

from agent import PROJECT_ROOT, OPENAI_API_KEY, TAVILI_API_KEY
import logging
import hydra
import os

pylogger = logging.getLogger(__name__)



def run(cfg: omegaconf.DictConfig):

    Config.set_instance(cfg)

    agent_prompt = hub.pull("hwchase17/openai-functions-agent")

    calendar = Calendar(2024, 5)

    llm = ChatOpenAI(
        model=cfg.main_agent.model_id,
        temperature=cfg.main_agent.temperature,
        api_key=OPENAI_API_KEY,
        timeout=cfg.main_agent.timeout_ms,
    )

    search = TavilySearchResults()

    tools = [
        add_appointment_to_calendar,
        remove_appointment_from_calendar,
        search,
        list_all_events
    ]

    agent = create_openai_functions_agent(llm, tools, agent_prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
    )

    memory = ChatMessageHistory(session_id="test-session")

    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: memory, 
        input_messages_key="input",
        history_messages_key="chat_history"
    )

    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def index():
        cal = Calendar(2024, 5)
        month_html = cal.display_month()
        return render_template_string('''
            <html>
                <head>
                    <title>Calendar</title>
                    <style>
                        body { font-family: Arial, sans-serif; }
                        table { width: 100%; border-collapse: collapse; }
                        th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }
                        th { background-color: #f2f2f2; }
                        .events { margin-top: 10px; font-size: 0.9em; color: #555; }
                        .form-container { margin-top: 20px; }
                    </style>
                </head>
                <body>
                    <h1>Calendar for May 2024</h1>
                    <div>{{ month_html | safe }}</div>
                    <h2>Add Event</h2>
                    <div class="form-container">
                        <form method="post" action="/add_event">
                            <label for="day">Day:</label>
                            <input type="number" id="day" name="day" required min="1" max="31">
                            <label for="event">Event:</label>
                            <input type="text" id="event" name="event" required>
                            <button type="submit">Add Event</button>
                        </form>
                    </div>
                </body>
            </html>
        ''', month_html=month_html)

    @app.route('/add_event', methods=['POST'])
    def add_event():
        day = int(request.form['day'])
        event = request.form['event']
        cal = Calendar(2024, 5)
        cal.add_event(day, event)
        return index()
    
    @app.context_processor
    def inject_events():
        cal = Calendar(2024, 5)
        events = {day: cal.get_events(day) for day in range(1, 32)}
        return {'events': events}

    @app.template_filter('add_events')
    def add_events(month_html):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(month_html, 'html.parser')
        for day, events in inject_events()['events'].items():
            day_cell = soup.find('td', string=str(day))
            if day_cell:
                events_div = soup.new_tag('div', **{'class': 'events'})
                for event in events:
                    event_p = soup.new_tag('p')
                    event_p.string = event
                    events_div.append(event_p)
                day_cell.append(events_div)
        return str(soup)


    @app.route("/submit-text", methods=["POST"])
    def submit_text():

        data = request.json
        prompt = data["text"]

        pylogger.info("Received prompt from user interface.")

        agent_with_chat_history.invoke(
            input={"input": prompt},
            config={"configurable": {"session_id": "<foo>"}},
        )

        formatted_time = datetime.now().strftime("%d %b %y %H.%M")
        return (
            jsonify({"status": "success", "message": "Text received successfully"}),
            200,
        )
    
    app.run(host="0.0.0.0", port=5000)
    
    atexit.register(cleanup)



def cleanup():
    pylogger.info("Server is shutting down. Cleaning up resources...")


@hydra.main(
    config_path=str(PROJECT_ROOT / "config"),
    config_name="default",
    version_base="1.1",
)
def main(cfg: omegaconf.DictConfig):
    Config.set_instance(cfg)
    run(cfg)


if __name__ == "__main__":
    main()


