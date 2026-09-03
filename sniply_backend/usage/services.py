from datetime import date
from django.core.cache import cache

FREE_TIER_LIMIT = 100


def get_current_period():
    today = date.today()
    period_start = today.replace(day=1)
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    return period_start, next_month


def usage_cache_key(user_id, period_start):
    return f"usage:{user_id}:{period_start.isoformat()}"


def get_current_usage(user):
    period_start, _ = get_current_period()
    key = usage_cache_key(user.id, period_start)
    count = cache.get(key)
    if count is None:
        count = 0
        cache.set(key, count, timeout=60 * 60 * 24 * 35)
    return count


def increment_usage(user):
    period_start, _ = get_current_period()
    key = usage_cache_key(user.id, period_start)
    if cache.get(key) is None:
        cache.set(key, 0, timeout=60 * 60 * 24 * 35)
    return cache.incr(key)


def has_quota_remaining(user):
    try:
        subscription = user.subscription
        link_limit = subscription.plan.link_limit
    except AttributeError:
        link_limit = FREE_TIER_LIMIT

    if link_limit is None:
        return True

    return get_current_usage(user) < link_limit