from typing import Any

from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext,
)
from botbuilder.schema import Activity, ActivityTypes, Attachment
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from src.config import settings
from src.data import mock_data

app = FastAPI()


adapter_settings = BotFrameworkAdapterSettings(
    app_id=settings.MICROSOFT_APP_ID,
    app_password=settings.MICROSOFT_APP_PASSWORD,
)

adapter = BotFrameworkAdapter(adapter_settings)


@app.get("/")
def health_check() -> dict[str, str]:
    """Return a basic health check response.

    Returns:
        Service status.
    """
    return {"status": "ok"}


@app.get("/automations")
def get_automations() -> list[dict[str, str]]:
    """Return the mock list of available RPA automations.

    Returns:
        List of automations formatted for Adaptive Card choices.
    """
    return mock_data


@app.post("/api/messages")
async def receive_bot_message(request: Request) -> Response:
    """Receive messages from Microsoft Teams Bot Framework.

    Args:
        request: Incoming FastAPI request.

    Returns:
        Bot Framework HTTP response.
    """
    if "application/json" not in request.headers.get("content-type", ""):
        return Response(status_code=415)

    body = await request.json()
    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

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
    """Handle a Teams bot turn.

    Args:
        turn_context: Current Bot Framework turn context.
    """
    if turn_context.activity.type == ActivityTypes.message:
        await turn_context.send_activity(
            Activity(
                type=ActivityTypes.message,
                attachments=[build_ticket_card()],
            )
        )


def build_ticket_card() -> Attachment:
    """Build an Adaptive Card containing the RPA dropdown.

    Returns:
        Adaptive Card attachment.
    """
    automations = get_automations()

    card: dict[str, Any] = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {
                "type": "TextBlock",
                "text": "Apertura ticket automazione RPA",
                "weight": "Bolder",
                "size": "Medium",
            },
            {
                "type": "Input.ChoiceSet",
                "id": "automation",
                "label": "Automazione",
                "style": "compact",
                "isMultiSelect": False,
                "choices": automations,
            },
            {
                "type": "Input.Text",
                "id": "description",
                "label": "Descrizione problema",
                "isMultiline": True,
                "placeholder": "Descrivi brevemente il problema...",
            },
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "title": "Apri ticket",
                "data": {
                    "action": "create_ticket",
                },
            }
        ],
    }

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card,
    )
