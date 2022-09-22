from django.utils import timezone
from datetime import datetime


def set_current_date():
    try:
        return timezone.now()
    except Exception:
        return datetime.now()
