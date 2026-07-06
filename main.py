from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/automations")
def get_automations() -> list[dict[str, str]]:
    return [
        {"title": "RPA-408 Ricerca Gare", "value": "rpa-408"},
        {"title": "RPA-3528 Business Central", "value": "rpa-3528"},
        {"title": "Plugin Decommissioning", "value": "plugin-decommissioning"},
    ]
