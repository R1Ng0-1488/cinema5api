from django.utils import timezone


def convert_date(date, format='%Y-%m-%d'):
    return timezone.datetime.strptime(date, format)