from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings

from src.config import settings

adapter_settings = BotFrameworkAdapterSettings(
    app_id=settings.MICROSOFT_APP_ID,
    app_password=settings.MICROSOFT_APP_PASSWORD,
    channel_auth_tenant=settings.MICROSOFT_APP_TENANT_ID,
)

adapter = BotFrameworkAdapter(adapter_settings)
