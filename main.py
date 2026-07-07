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

print(f"MICROSOFT_APP_ID prefix: {settings.MICROSOFT_APP_ID[:8]}")
print(f"MICROSOFT_APP_ID length: {len(settings.MICROSOFT_APP_ID)}")
print(
    f"MICROSOFT_APP_PASSWORD configured: {bool(settings.MICROSOFT_APP_PASSWORD)}"
)
print(f"MICROSOFT_APP_PASSWORD length: {len(settings.MICROSOFT_APP_PASSWORD)}")

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

    print(f"Incoming activity type: {activity.type}")
    print(f"Incoming channel_id: {activity.channel_id}")
    print(f"Incoming service_url: {activity.service_url}")
    print(
        "Incoming conversation_id: "
        f"{activity.conversation.id if activity.conversation else None}"
    )
    print(f"Authorization header present: {bool(auth_header)}")
    print(
        "Authorization header prefix: "
        f"{auth_header[:20] if auth_header else None}"
    )

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

    print(f"Handling activity type: {turn_context.activity.type}")
    print(f"Reply to activity id: {turn_context.activity.id}")

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


@app.get("/privacy")
def privacy_policy() -> dict[str, str]:
    """Return a placeholder privacy policy for the Teams test app.

    Returns:
        Privacy policy placeholder content.
    """
    return {
        "title": "Privacy Policy",
        "content": (
            "This is a private test application used to validate a Microsoft Teams "
            "integration with a FastAPI middleware. No production data is stored "
            "by this test service."
        ),
    }


@app.get("/tos")
def terms_of_service() -> dict[str, str]:
    """Return placeholder terms of service for the Teams test app.

    Returns:
        Terms of service placeholder content.
    """
    return {
        "title": "Terms of Service",
        "content": (
            "This service is provided only for internal testing of a Microsoft Teams "
            "bot and Adaptive Card workflow. It is not intended for production use."
        ),
    }
