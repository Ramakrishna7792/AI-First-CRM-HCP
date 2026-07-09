"""Deterministic development seed: 1 user, 25 doctors, 10 products, 100 interactions."""
from datetime import date, time, timedelta

from sqlalchemy import delete, func, select

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.domain.models import (
    ChatMessage, ChatSession, Doctor, Interaction, Product, User, interaction_products,
)

DOCTORS = [
    ("Dr. Rajesh Sharma", "Cardiology", "Apollo Hospital", "Mumbai"),
    ("Dr. Priya Mehta", "Neurology", "Fortis Healthcare", "Delhi"),
    ("Dr. Anil Kapoor", "Endocrinology", "Max Super Specialty", "Bengaluru"),
    ("Dr. Sunita Reddy", "Oncology", "Tata Memorial Centre", "Mumbai"),
    ("Dr. Vikram Singh", "Pulmonology", "AIIMS", "Delhi"),
    ("Dr. Kavita Nair", "Gastroenterology", "Manipal Hospital", "Bengaluru"),
    ("Dr. Rahul Desai", "Orthopedics", "Kokilaben Hospital", "Mumbai"),
    ("Dr. Meera Iyer", "Dermatology", "Narayana Health", "Chennai"),
    ("Dr. Arjun Patel", "Cardiology", "Sterling Hospital", "Ahmedabad"),
    ("Dr. Deepa Krishnan", "Neurology", "Amrita Hospital", "Kochi"),
    ("Dr. Sanjay Gupta", "Endocrinology", "Medanta Hospital", "Gurugram"),
    ("Dr. Nisha Verma", "Oncology", "RGCI", "Delhi"),
    ("Dr. Rohit Malhotra", "Pulmonology", "Global Hospital", "Hyderabad"),
    ("Dr. Ananya Bose", "Gastroenterology", "Peerless Hospital", "Kolkata"),
    ("Dr. Karthik Subramanian", "Orthopedics", "MIOT Hospital", "Chennai"),
    ("Dr. Pooja Agarwal", "Dermatology", "Artemis Hospital", "Gurugram"),
    ("Dr. Harish Choudhury", "Cardiology", "BM Birla Heart Research", "Kolkata"),
    ("Dr. Leena Thomas", "Neurology", "Aster Medcity", "Kochi"),
    ("Dr. Amit Kulkarni", "Endocrinology", "Ruby Hall Clinic", "Pune"),
    ("Dr. Farah Khan", "Oncology", "HCG Cancer Centre", "Bengaluru"),
    ("Dr. Gaurav Joshi", "Pulmonology", "Lilavati Hospital", "Mumbai"),
    ("Dr. Shalini Saxena", "Gastroenterology", "Sir Ganga Ram Hospital", "Delhi"),
    ("Dr. Naveen Rao", "Orthopedics", "Yashoda Hospitals", "Hyderabad"),
    ("Dr. Ritu Banerjee", "Dermatology", "AMRI Hospitals", "Kolkata"),
    ("Dr. Joseph Mathew", "General Medicine", "Lakeshore Hospital", "Kochi"),
]
PRODUCTS = [
    ("CardioMax XR", "Cardiology", "Extended-release hypertension therapy"),
    ("NeuroFlex Plus", "Neurology", "Neuropathic pain management"),
    ("DiabeCare Pro", "Endocrinology", "Type 2 diabetes therapy"),
    ("OncoShield 500", "Oncology", "Targeted therapy adjunct"),
    ("RespiClear Inhaler", "Pulmonology", "Dual-action bronchodilator"),
    ("GastroGuard EC", "Gastroenterology", "Enteric-coated PPI"),
    ("OrthoFlex Gel", "Orthopedics", "Topical pain relief"),
    ("DermaHeal Cream", "Dermatology", "Topical inflammatory skin therapy"),
    ("ImmunoBoost V", "Immunology", "Immunotherapy support"),
    ("VitaBone D3", "General", "Vitamin D3 and calcium"),
]


def seed() -> dict[str, int]:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        db.execute(delete(ChatMessage))
        db.execute(delete(ChatSession))
        db.execute(delete(interaction_products))
        db.execute(delete(Interaction))
        db.execute(delete(Product))
        db.execute(delete(Doctor))
        db.execute(delete(User))
        user = User(
            email="rep@medconnect.example", full_name="Demo Medical Representative",
            hashed_password=hash_password("DemoPass123!"), role="representative",
        )
        doctors = [Doctor(name=n, specialization=s, hospital=h, city=c) for n, s, h, c in DOCTORS]
        products = [Product(product_name=n, category=c, description=d) for n, c, d in PRODUCTS]
        db.add_all([user, *doctors, *products])
        db.flush()
        types = ["In-Person", "Virtual", "Phone", "Conference"]
        sentiments = ["Positive", "Neutral", "Positive", "Negative"]
        start = date.today() - timedelta(days=120)
        interactions = []
        for index in range(100):
            doctor = doctors[index % len(doctors)]
            product = products[index % len(products)]
            interaction = Interaction(
                doctor_id=doctor.id, representative_id=user.id,
                interaction_type=types[index % len(types)],
                date=start + timedelta(days=index), time=time(9 + index % 8, (index * 7) % 60),
                attendees=f"{doctor.name}, Demo Medical Representative",
                topics=f"{product.product_name} clinical profile and patient selection",
                materials="Approved product monograph and clinical evidence summary",
                samples=f"{product.product_name}: {index % 4} packs",
                sentiment=sentiments[index % len(sentiments)],
                outcomes="HCP reviewed the evidence and discussed suitable patient profiles.",
                followup=f"Follow up in {7 + index % 14} days",
                summary=f"Discussed {product.product_name} with {doctor.name}.",
                entry_source="ai_assisted" if index % 3 == 0 else "form",
                products=[product],
            )
            interactions.append(interaction)
        db.add_all(interactions)
        db.commit()
        return {
            "users": db.scalar(select(func.count(User.id))),
            "doctors": db.scalar(select(func.count(Doctor.id))),
            "products": db.scalar(select(func.count(Product.id))),
            "interactions": db.scalar(select(func.count(Interaction.id))),
        }


if __name__ == "__main__":
    print(seed())
