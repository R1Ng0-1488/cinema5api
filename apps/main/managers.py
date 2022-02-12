from django.db import models
from django.utils import timezone


class AvailableSession(models.QuerySet):
    """Класс фильтрации фильмов"""

    def movies_today(self):
        now = timezone.now()
        return self.filter(
            session__date=now.date(), 
            session__time__gte=now.time()
        ).distinct()

    def movies_tommorow(self):
        now = timezone.now()
        return self.filter(
            session__date=now.date() + timezone.timedelta(days=1), 
        ).distinct()

    def movies_soon(self):
        now = timezone.now()
        return self.filter(
            start_date__gt=now.date(),
            session__isnull=False 
        )