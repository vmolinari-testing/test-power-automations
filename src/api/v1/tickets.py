from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class TicketRequest(BaseModel):
    automation: str
    description: str


@router.post("/tickets")
def create_ticket(ticket_request: TicketRequest) -> dict[str, str]:
    """Create a mock support ticket."""
    return {
        "status": "created",
        "ticket_id": "MOCK-001",
        "automation": ticket_request.automation,
    }
