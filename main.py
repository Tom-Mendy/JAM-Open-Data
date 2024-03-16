import re
from urllib import response
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
import requests
from fastapi import FastAPI
import random
import os

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

    prompt = (
        "genère uniquement 3 faux gentilé de la commun '"
        + city
        + "' en français au masculain sans suplément, sans description, sans commentaire, sans note"
    )

    command_output = subprocess.run(
        ["ollama", "run", "mistral", prompt], capture_output=True
    ).stdout.decode("utf-8")

    new = [i for i in command_output.split("\n") if i != ""]

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
    response = RedirectResponse(url="/swagger-ui.html")
    return response


@app.get("/call_dataset")
def call_dataset():
    if name_list != []:
        name_list.clear()
    url = "https://geo.api.gouv.fr/communes?fields=codePostaux,centre"
    response = requests.get(url)

    if response.status_code == 200:
        response_data = response.json()
        for i in range(0, len(response_data)):
            name_list.append(response_data[i]["nom"])
    else:
        return JSONResponse(
            status_code=404, content={"Error": "response not found in the dataset"}
        )


@app.get("/random_commune")
def random_commune():
    random_choice = random.choice(name_list)
    return random_choice

@app.get("/buttonResponse/{commune}/{all_gentiles_button_str}/{gentile}")
def buttonResponse(commune: str, all_gentiles_button_str: str, gentile: str):
    all_gentiles_button = all_gentiles_button_str.split(",")
    buttonColor = ["grey", "grey", "grey", "grey"]
    for i in range(0, 4):
        if all_gentiles_button[i] == gentile:
            buttonColor[i] = "red"
    real_gentiles = all_gentiles["communes"][commune.lower()][0]
    buttonColor[all_gentiles_button.index(real_gentiles.capitalize())] = "green"
    return f'\
        <button class=btn-{buttonColor[0]}>{all_gentiles_button[0]}</button>\
        <button class=btn-{buttonColor[1]}>{all_gentiles_button[1]}</button>\
        <button class=btn-{buttonColor[2]}>{all_gentiles_button[2]}</button>\
        <button class=btn-{buttonColor[3]}>{all_gentiles_button[3]}</button>'

@app.get("/button/{commune}", response_class=HTMLResponse)
def button(commune: str):
    gentiles = []
    real_gentiles = all_gentiles["communes"][commune.lower()][0]
    fake_gentile = get_fake_gentile(commune)
    gentiles.append(real_gentiles.capitalize())
    for gentile in fake_gentile:
        gentiles.append(gentile)
    gentiles = random.sample(gentiles, len(gentiles))
    gentiles_str = ",".join(gentiles)
    print(gentiles_str)
    return f'\
        <button class=btn hx-get="http://localhost:8000/buttonResponse/{commune}/{gentiles_str}/{gentiles[0]}" hx-target=#buttonGentile hx-indicator=".htmx-indicator">{gentiles[0]}</button>\
        <button class=btn hx-get="http://localhost:8000/buttonResponse/{commune}/{gentiles_str}/{gentiles[1]}" hx-target=#buttonGentile hx-indicator=".htmx-indicator">{gentiles[1]}</button>\
        <button class=btn hx-get="http://localhost:8000/buttonResponse/{commune}/{gentiles_str}/{gentiles[2]}" hx-target=#buttonGentile hx-indicator=".htmx-indicator">{gentiles[2]}</button>\
        <button class=btn hx-get="http://localhost:8000/buttonResponse/{commune}/{gentiles_str}/{gentiles[3]}" hx-target=#buttonGentile hx-indicator=".htmx-indicator">{gentiles[3]}</button>'


@app.get("/gentile",  response_class=HTMLResponse)
def gentile():
    a = True
    while (a):
        random_commune_var = random_commune()
        print(random_commune_var)
        # print(all_gentiles)
        try:
            all_gentiles["communes"][random_commune_var.lower()][0]
            a = False
        except KeyError:
            a = True

    return f'\
  <div class="boxTop">\
    <image src="{image_of_commune(random_commune_var)}" alt="communoquizz" class="img">\
  </div>\
  <div class="boxMiddle">\
    <text class="text">Commun : {random_commune_var}\
    </text>\
  </div>\
  <div class="boxBottom">\
    <div hx-get="http://localhost:8000/button/{random_commune_var}" hx-trigger="load" hx-target=#buttonGentile hx-indicator=".htmx-indicator">\
    </div>\
    <div id="buttonGentile" class="btnBox">\
        <span class="htmx-indicator">\
            <img src="../image/bars.svg" /> Generating fake reponse ...\
        </span>\
    </div>\
    <div class="btnBoxNext">\
        <button class="btnNext" hx-get="http://localhost:8000/gentile" hx-target="#allInfo">next</button>\
    </div>\
  </div>'



@app.get("/image_of_commune")
def image_of_commune(commune_name: str):
    response = requests.get("https://en.wikipedia.org/w/api.php",
                            params={"action": "parse",
                                    "page": commune_name,
                                    "format": "json"})
    data = response.json()
    image_url = None

    if "images" in data["parse"]:
        for image in data["parse"]["images"]:
            if image.lower().endswith(".jpg"):
                image_url = f"https://en.wikipedia.org/wiki/File:{image}"
                break
    download_image(image_url, f"{commune_name}.txt")
    image = get_image_content(f"{commune_name}.txt")
    remove_file_from_tmp(f"{commune_name}.txt")
    return image


def download_image(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP errors

        tmp_folder = 'tmp/'

        filepath = os.path.join(tmp_folder, filename)

        with open(filepath, 'wb') as file:
            # Write the content of the response (the image) to the file
            file.write(response.content)

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_image_content(filename):
    try:
        filepath = os.path.join('tmp/', filename)

        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        pattern = r'<meta property="og:image" content="(.+?)">'
        match = re.search(pattern, content)

        if match:
            # Return the string between the quotes
            return match.group(1)
        else:
            return "No meta tag found in the file."
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def remove_file_from_tmp(filename):
    try:
        filepath = os.path.join('tmp/', filename)

        if os.path.exists(filepath):
            os.remove(filepath)
        else:
            print(f"File '{filename}' does not exist in /tmp folder.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Main

name_list: list = []
random.seed()

all_gentiles = get_json_file("demonyms.json")

call_dataset()
