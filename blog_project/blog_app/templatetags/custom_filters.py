from django import template
from django.utils import timezone
from django.template.defaultfilters import date as default_date

register = template.Library()

@register.simple_tag
def custom_naturaltime(value):
    now = timezone.now()
    time_difference = now - value
    if time_difference < timezone.timedelta(minutes=60):
        minutes = time_difference.total_seconds() // 60
        return f"{int(minutes)}분 전"
    elif time_difference < timezone.timedelta(hours=24):
        hours = time_difference.total_seconds() // 3600
        return f"약 {int(hours)}시간 전"
    elif time_difference < timezone.timedelta(days=7):
        days = time_difference.days
        if days == 1:
            return "어제"
        else:
            return f"{days}일 전"
    else:
        return default_date(value, "Y년 m월 d일")
