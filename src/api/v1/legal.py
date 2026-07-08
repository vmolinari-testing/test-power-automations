from fastapi import APIRouter

router = APIRouter()


@router.get("/privacy")
def privacy_policy() -> dict[str, str]:
    """Return a placeholder privacy policy for the Teams test app."""
    return {
        "title": "Privacy Policy",
        "content": (
            "This is a private test application used to validate a Microsoft Teams "
            "integration with a FastAPI middleware. No production data is stored "
            "by this test service."
        ),
    }


@router.get("/tos")
def terms_of_service() -> dict[str, str]:
    """Return placeholder terms of service for the Teams test app."""
    return {
        "title": "Terms of Service",
        "content": (
            "This service is provided only for internal testing of a Microsoft Teams "
            "bot and Adaptive Card workflow. It is not intended for production use."
        ),
    }
