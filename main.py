from typing import Union

from fastapi import FastAPI

# Import JSON module
import json


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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
