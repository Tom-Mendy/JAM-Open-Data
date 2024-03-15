from ast import List
from fastapi.responses import JSONResponse, RedirectResponse
import requests
from fastapi import FastAPI
import random

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


app = FastAPI(docs_url="/swagger-ui.html")


@app.get("/")
async def docs_redirect():
    response = RedirectResponse(url='/swagger-ui.html')
    return response


list_all: list = []


@app.get("/call_dataset")
def call_dataset():
    if list_all != []:
        list_all.clear()
    url = "https://geo.api.gouv.fr/communes?fields=codePostaux"
    response = requests.get(url)

    if response.status_code == 200:
        response_data = response.json()
        list_all.append(response_data)
    else:
        return JSONResponse(status_code=404, content={
            "Error": "response not found in the dataset"})


@app.get("/random_commune")
def random_commune():
    random.seed()
    random_choice = random.choice(list_all[0])
    return random_choice
