
from db import engine, SessionLocal
from models import Base, College
import uuid

def reset_database():
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped.")
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("All tables created.")

def seed_college():
    session = SessionLocal()
    # Use a fixed UUID for the college
    college_id = uuid.UUID("11111111-1111-1111-1111-111111111111")
    college = College(
        id=college_id,
        name="Sardar Patel Institute of Technology",
        address="Munshi Nagar, Andheri (West), Mumbai, Maharashtra 400058",
        logo_url=None
    )
    session.add(college)
    session.commit()
    print(f"College added: {college.name} with id {college.id}")
    session.close()

if __name__ == "__main__":
    reset_database()
    seed_college()
