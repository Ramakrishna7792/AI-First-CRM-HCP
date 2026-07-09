"""CRUD repository exports.

This module provides the conventional project entry point while persistence
remains implemented in the clean repository layer.
"""
from app.repositories.repositories import (
    ChatRepository, DoctorRepository, InteractionRepository, ProductRepository, UserRepository,
)

__all__ = [
    "UserRepository", "DoctorRepository", "ProductRepository",
    "InteractionRepository", "ChatRepository",
]
