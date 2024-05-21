
## Installation

Create the `conda` environment

```
conda create --name agent python==3.9
conda activate agent
```

Install all the dependencies

```
pip install -r requirements.txt
pip install -e .
```

Create files `key.txt` and `tavili_key.txt` in the home directory of the project. Insert your OpenAI key in the first and your Tavily key in the second.

Run the server

```
python server.py
```
