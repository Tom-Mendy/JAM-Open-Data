from ast import List
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
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


# Create a FastAPI app

app = FastAPI(docs_url="/swagger-ui.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def docs_redirect():
    response = RedirectResponse(url='/swagger-ui.html')
    return response


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
    random_choice = random.choice(list_all[0])
    return random_choice


@app.get("/button")
def button():
    print("gentiles =", gentiles)
    if gentiles != []:
        return f'\
        <button class=btn>{gentiles[0]}</button>\
        <button class=btn>{gentiles[1]}</button>\
        <button class=btn>{gentiles[2]}</button>\
        <button class=btn>{gentiles[3]}</button>'
    else:
        return '\
    <button class=btn>gentiles[0]</button>\
    <button class=btn>gentiles[1]</button>\
    <button class=btn>gentiles[2]</button>\
    <button class=btn>gentiles[3]</button>'


@app.get("/gentile",  response_class=HTMLResponse)
def gentile():
    a = True
    while (a):
        random_commune_var = random_commune()
        print(random_commune_var)
        gentiles = []
        try:
            gentiles.append(all_gentiles["communes"]
                            [random_commune_var["nom"].lower()][0])
            a = False
        except KeyError:
            a = True

    # gentiles.append(get_fake_gentile(random_commune_var["nom"]))
    gentiles.append("gentile1")
    gentiles.append("gentile1")
    gentiles.append("gentile1")
    gentiles.append("gentile1")
    return f'\
  <div class="boxTop">\
    <image src="../image/font.jpg" alt="communoquizz" class="img">\
  </div>\
  <div class="boxMiddle">\
    <text class="text">Commun : {random_commune_var["nom"]}\
    </text>\
  </div>\
  <div class="boxBottom">\
    <div hx-get="http://localhost:8000/button" hx-trigger="load" hx-target=#buttonGentile>\
    </div>\
    <div id="buttonGentile" class=gentileButton></div>\
    <button class="btn" hx-get="http://localhost:8000/gentile" hx-target="#allInfo">next</button>\
  </div>'


# Main
list_all: list = []
gentiles: list = []
random.seed()

all_gentiles = get_json_file("demonyms.json")

call_dataset()
