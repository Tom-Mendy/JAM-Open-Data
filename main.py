from fastapi.responses import JSONResponse
import requests
from fastapi import FastAPI
import random

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


list_all = []


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
