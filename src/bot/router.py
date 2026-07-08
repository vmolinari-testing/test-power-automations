from botbuilder.core import TurnContext
from botbuilder.schema import Activity, ActivityTypes
from botframework.connector.auth import MicrosoftAppCredentials
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from src.bot.adapter import adapter
from src.bot.cards import build_ticket_card

router = APIRouter()


@router.post("/api/messages")
async def receive_bot_message(request: Request) -> Response:
    """Receive messages from Microsoft Teams Bot Framework."""
    if "application/json" not in request.headers.get("content-type", ""):
        return Response(status_code=415)

    body = await request.json()
    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    if activity.service_url:
        MicrosoftAppCredentials.trust_service_url(activity.service_url)

    response = await adapter.process_activity(
        activity,
        auth_header,
        handle_turn,
    )

    if response:
        return JSONResponse(
            status_code=response.status,
            content=response.body,
        )

    return Response(status_code=201)


async def handle_turn(turn_context: TurnContext) -> None:
    """Handle a Teams bot turn."""
    if turn_context.activity.type == ActivityTypes.message:
        await turn_context.send_activity(
            Activity(
                type=ActivityTypes.message,
                attachments=[build_ticket_card()],
            )
        )
