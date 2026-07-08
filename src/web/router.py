from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

PAGES_DIR = Path(__file__).parent / "pages"


@router.get("/tab/open-ticket")
def open_ticket_tab() -> FileResponse:
    """Return the Teams tab page used to open an RPA support ticket."""
    return FileResponse(PAGES_DIR / "open_ticket.html")
