from fastapi import Request


def get_client_ip(request: Request):
    """
    Extracts the real client IP address from the request,
    accounting for Vercel/proxies and local development.
    """
    # 1. Try Vercel's specific real IP header first
    x_real_ip = request.headers.get("x-real-ip")
    if x_real_ip:
        return x_real_ip.strip()

    # 2. Try the standard proxy header (can be a comma-separated list)
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        # The first IP in the list is the original client
        return x_forwarded_for.split(",")[0].strip()

    # 3. Fallback to direct connection (used during local uvicorn testing)
    if request.client and request.client.host:
        return request.client.host

    # 4. Ultimate fallback (just in case)
    return None
