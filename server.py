from datetime import datetime
from pathlib import Path
from agent.status.config import Config
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from flask import Flask, request, jsonify
from flask_cors import CORS
import atexit

import omegaconf

from agent import PROJECT_ROOT
import logging
import hydra
import os

pylogger = logging.getLogger(__name__)


def run(cfg: omegaconf.DictConfig):

    Config.set_instance(cfg)


    agent_prompt = hub.pull("hwchase17/openai-functions-agent")

    llm = ChatOpenAI(
        model=cfg.main_agent.model_id,
        temperature=cfg.main_agent.temperature,
        api_key=OPENAI_API_KEY,
        timeout=cfg.main_agent.timeout_ms,
    )

    tools = [
        None
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

    atexit.register(cleanup)

    @app.route("/submit-text", methods=["POST"])
    def submit_text():

        data = request.json
        prompt = data["text"]

        pylogger.info("Received prompt from user interface.")
        log_prompt(prompt)

        agent_with_chat_history.invoke(
            input={"input": prompt},
            config={"configurable": {"session_id": "<foo>"}},
        )

        formatted_time = datetime.now().strftime("%d %b %y %H.%M")
        save_txt(prompt, f"{cfg.paths.generations}/{formatted_time}.txt")

        return (
            jsonify({"status": "success", "message": "Text received successfully"}),
            200,
        )


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
