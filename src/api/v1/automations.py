from fastapi import APIRouter

from src.data import mock_data

router = APIRouter()


@router.get("/automations")
def get_automations() -> list[dict[str, str]]:
    """Return the mock list of available RPA automations."""
    return mock_data
