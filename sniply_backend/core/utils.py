import hashlib

import requests


def get_country_from_ip(ip_address):
    if not ip_address or ip_address in ("127.0.0.1", "localhost"):
        return None
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=countryCode", timeout=1)
        data = response.json()
        return data.get("countryCode")
    except requests.RequestException:
        return None


def hash_ip(ip_address):
    if not ip_address:
        return None
    return hashlib.sha256(ip_address.encode()).hexdigest()


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")