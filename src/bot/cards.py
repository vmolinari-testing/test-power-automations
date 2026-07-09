from typing import Any

from botbuilder.schema import Attachment

from src.data import get_mock_data


def build_ticket_card() -> Attachment:
    """Build an Adaptive Card containing the RPA dropdown."""
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
                "choices": get_mock_data(),
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
                "data": {"action": "create_ticket"},
            }
        ],
    }

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card,
    )
