from functools import cache
from random import randint
from time import monotonic


def _get_cache_bucket(seconds: int = 10) -> int:
    """Return a time bucket used to refresh mock data periodically."""
    return int(monotonic() // seconds)


def _rand100(lower_threshold: int) -> int:
    """Return a random integer between lower_threshold and lower_threshold + 100."""
    return randint(0, 100) + lower_threshold


def _build_mock_automation(
    lower_threshold: int,
    title: str,
    value_suffix: str,
) -> dict[str, str]:
    """Build one mock automation entry."""
    rpa_id = _rand100(lower_threshold)

    return {
        "title": f"RPA-{rpa_id} {title}",
        "value": f"rpa-{rpa_id}_{value_suffix}",
    }


@cache
def _get_mock_data_for_bucket(bucket: int) -> tuple[dict[str, str], ...]:
    """Return mock automation data for a specific time bucket."""
    return (
        _build_mock_automation(100, "Invio Report", "invio_report"),
        _build_mock_automation(200, "Controllo Fatture", "controllo_fatture"),
        _build_mock_automation(
            300,
            "Aggiornamento Anagrafiche",
            "aggiornamento_anagrafiche",
        ),
        _build_mock_automation(400, "Verifica Pagamenti", "verifica_pagamenti"),
        _build_mock_automation(
            500, "Estrazione Documenti", "estrazione_documenti"
        ),
        _build_mock_automation(
            600, "Sincronizzazione Dati", "sincronizzazione_dati"
        ),
        _build_mock_automation(
            700, "Monitoraggio Scadenze", "monitoraggio_scadenze"
        ),
        _build_mock_automation(
            800, "Generazione Notifiche", "generazione_notifiche"
        ),
        _build_mock_automation(
            900, "Validazione Anagrafiche", "validazione_anagrafiche"
        ),
        _build_mock_automation(
            1000, "Archiviazione Allegati", "archiviazione_allegati"
        ),
    )


def get_mock_data() -> list[dict[str, str]]:
    """Return mock automation data refreshed every 10 seconds."""
    bucket = _get_cache_bucket(seconds=10)
    return list(_get_mock_data_for_bucket(bucket))
