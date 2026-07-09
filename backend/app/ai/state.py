from typing import TypedDict


class InteractionGraphState(TypedDict):
    message: str
    existing_draft: dict
    extracted: dict
    merged_draft: dict
    reply: str
    missing_fields: list[str]
    warnings: list[str]
