from django.db import models
from django.utils import timezone


class AvailableSession(models.QuerySet):
    """Класс фильтрации фильмов"""

    def movies_today(self):
        now = timezone.now()
        return self.filter(
            sessions__date=now.date(), 
            sessions__time__gte=now.time()
        ).distinct()

    def movies_tomorrow(self):
        now = timezone.now()
        return self.filter(
            sessions__date=now.date() + timezone.timedelta(days=1), 
        ).distinct()

    def movies_soon(self):
        now = timezone.now()
        return self.filter(
            start_date__gt=now.date(),
            sessions__isnull=False 
        ).distinct()

    def movies_date(self, date):
        now = timezone.now()
        kwargs = {'sessions__date': date}
        if date == now.date():
            kwargs['sessions__time__gte'] = now.time()
        return self.filter(**kwargs).distinct()