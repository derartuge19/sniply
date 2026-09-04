from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import Click

from user_agents import parse as parse_user_agent


def get_device_breakdown(clicks):
    device_counts = {"desktop": 0, "mobile": 0, "tablet": 0, "other": 0}

    for click in clicks.exclude(user_agent=""):
        ua = parse_user_agent(click.user_agent)
        if ua.is_mobile:
            device_counts["mobile"] += 1
        elif ua.is_tablet:
            device_counts["tablet"] += 1
        elif ua.is_pc:
            device_counts["desktop"] += 1
        else:
            device_counts["other"] += 1

    return device_counts


def get_link_analytics(link, days=30):
    since = timezone.now() - timedelta(days=days)
    clicks = Click.objects.filter(link=link, clicked_at__gte=since)

    total_clicks = clicks.count()

    clicks_over_time = (
        clicks
        .annotate(day=TruncDate("clicked_at"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    top_referrers = (
        clicks
        .exclude(referrer="")
        .values("referrer")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    top_countries = (
        clicks
        .exclude(country__isnull=True)
        .values("country")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    device_breakdown = get_device_breakdown(clicks)

    return {
        "total_clicks": total_clicks,
        "clicks_over_time": list(clicks_over_time),
        "top_referrers": list(top_referrers),
        "top_countries": list(top_countries),
        "device_breakdown": device_breakdown,
    }