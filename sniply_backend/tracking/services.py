from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import Click


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

    return {
        "total_clicks": total_clicks,
        "clicks_over_time": list(clicks_over_time),
        "top_referrers": list(top_referrers),
    }