# JAM-Open-Data

## install

### AI

install ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

pull mistral AI

```bash
ollama pull mistral
```

### Python

```bash
pip install fastap
pip install "uvicorn[standard]"
pip install fastapi-htmx
```

## Run

launch python backend

```bash
uvicorn main:app --reload
```

open font

```bash
index.html
```
