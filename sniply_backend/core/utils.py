import hashlib


def hash_ip(ip_address):
    if not ip_address:
        return None
    return hashlib.sha256(ip_address.encode()).hexdigest()


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")