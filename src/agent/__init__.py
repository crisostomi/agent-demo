from datetime import datetime
import logging
import os
from pathlib import Path
import git
from rich.logging import RichHandler



FORMAT = "%(message)s"
formatted_time = datetime.now().strftime("%d %b %y %H.%M")

logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        RichHandler(
            rich_tracebacks=True,
            show_level=True,
            show_path=True,
            show_time=True,
            omit_repeated_times=True,
        ),
        logging.FileHandler(f"logs/{formatted_time}.log"),
    ],
)
try:
    PROJECT_ROOT = Path(
        git.Repo(Path.cwd(), search_parent_directories=True).working_dir
    )
except git.exc.InvalidGitRepositoryError:
    PROJECT_ROOT = Path.cwd()

os.environ["PROJECT_ROOT"] = str(PROJECT_ROOT)

OPENAI_API_KEY = open(f"{PROJECT_ROOT}/key.txt", "r").read().strip()
TAVILI_API_KEY = open(f"{PROJECT_ROOT}/tavili_key.txt", "r").read().strip()

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["TAVILY_API_KEY"] = TAVILI_API_KEY