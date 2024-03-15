from typing import Union
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init

# Import JSON module
import json
# Import subprocess module
import subprocess


def get_json_file(file):
    f = open(file, "r")
    jsonFile = f.read()
    f.close()

    dictFile = json.loads(jsonFile)

    return dictFile


def get_fake_gentile(city: str):
    result = []

    prompt = "genère uniquement 3 faux gentilé de la commun '" + city + \
        "' en français au masculain sans suplément, sans description, sans commentaire, sans note"

    command_output = subprocess.run(["ollama", "run", "mistral",
                                     prompt], capture_output=True).stdout.decode('utf-8')

    new = [i for i in command_output.split("\n") if i != '']

    for i in range(0, 3):
        result.append(new[i].strip(" ").split(" ")[1])

    return result


app = FastAPI()
htmx_init(templates=Jinja2Templates(directory=Path("my_app") / "templates"))

City_to_gentile = get_json_file("demonyms.json")


@app.get("/", response_class=HTMLResponse)
@htmx("index", "index")
async def read_root(request: Request):
    return {"greeting": "Hello World"}


@app.get("/info", response_class=HTMLResponse)
@htmx("info")
async def get_info(request: Request):
    return {"gentiles": ["gentile 1", "gentile 2", "gentile 3", "gentile 4"], "city": "anglet"}
