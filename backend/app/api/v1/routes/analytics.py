from collections import Counter

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.domain.models import User
from app.repositories.repositories import InteractionRepository

router = APIRouter()


class DoctorCount(BaseModel):
    name: str
    count: int


class AnalyticsSummary(BaseModel):
    total_interactions: int
    positive_sentiment: int
    neutral_sentiment: int
    negative_sentiment: int
    interactions_by_type: dict[str, int]
    top_doctors: list[DoctorCount]


@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Return aggregate interaction statistics for the authenticated representative.

    Uses the existing InteractionRepository — no raw SQLAlchemy queries.
    Fetches up to 500 records and computes stats in Python to keep the
    repository contract clean.
    """
    interactions = InteractionRepository(db).list_for_user(user.id, limit=500)

    sentiment_counter = Counter(
        ix.sentiment for ix in interactions if ix.sentiment
    )
    type_counter = Counter(ix.interaction_type for ix in interactions)
    doctor_counter = Counter(ix.doctor.name for ix in interactions)

    top_doctors = [
        DoctorCount(name=name, count=count)
        for name, count in doctor_counter.most_common(5)
    ]

    return AnalyticsSummary(
        total_interactions=len(interactions),
        positive_sentiment=sentiment_counter.get("Positive", 0),
        neutral_sentiment=sentiment_counter.get("Neutral", 0),
        negative_sentiment=sentiment_counter.get("Negative", 0),
        interactions_by_type=dict(type_counter),
        top_doctors=top_doctors,
    )
