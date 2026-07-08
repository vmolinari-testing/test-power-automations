from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from src.api.v1.automations import router as automations_router
from src.api.v1.legal import router as legal_router
from src.api.v1.tickets import router as tickets_router
from src.bot.router import router as bot_router
from src.web.router import router as web_router

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="src/web/static"),
    name="static",
)

api = APIRouter(prefix="/api/v1")

api.include_router(automations_router)
api.include_router(tickets_router)

app.include_router(api)
app.include_router(legal_router)
app.include_router(bot_router)
app.include_router(web_router)


@app.get("/")
def health_check() -> dict[str, str]:
    """Return a basic health check response."""
    return {"status": "ok"}
