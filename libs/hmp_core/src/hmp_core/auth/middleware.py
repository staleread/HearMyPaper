from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SpiffeIdentityMiddleware(BaseHTTPMiddleware):
    """
    Middleware that extracts the SPIFFE ID from headers injected by the infrastructure 
    (e.g., Envoy, Contour) and attaches it to the request state.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # In a real Envoy/Istio setup, this might be X-Forwarded-Client-Cert
        # or a custom header like X-Spiffe-Id.
        # We'll check for X-Spiffe-Id as a standard placeholder.
        spiffe_id = request.headers.get("x-spiffe-id")
        
        # We can also attempt to parse it from X-Forwarded-Client-Cert if needed
        # but for now, we'll keep it simple and explicit.
        request.state.spiffe_id = spiffe_id
        
        return await call_next(request)
