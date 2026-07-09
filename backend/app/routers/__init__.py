"""Public router export backed by the versioned API layer."""
from app.api.v1.router import api_router

__all__ = ["api_router"]
