# JAM-Open-Data

## install

### AI

install ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

pull mistral AI

```bash
ollama pull mistral
```

### Python

```bash
pip install -r requirements.txt
```

### Virtual env (optional)
if a virtual environnement is needed do the following steps:

```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```

## Run

launch python backend

```bash
uvicorn main:app --reload
```

or

```bash
./start.sh
```

open font

```bash
index.html
```
