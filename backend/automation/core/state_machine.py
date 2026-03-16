from .models import AutomationStatus


def normalize_status(raw_status: str | None) -> AutomationStatus:
    if not raw_status:
        return AutomationStatus.FAILED

    normalized = raw_status.strip().upper()
    if normalized in {status.value for status in AutomationStatus}:
        return AutomationStatus(normalized)

    return AutomationStatus.FAILED
