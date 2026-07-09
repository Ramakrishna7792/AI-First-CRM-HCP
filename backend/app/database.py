"""Compatibility entry point for database infrastructure.

Application code should continue to depend on app.db.session and app.db.base.
"""
from app.db.base import Base
from app.db.session import SessionLocal, engine, get_db

__all__ = ["Base", "SessionLocal", "engine", "get_db"]
