from sqlalchemy import Column, Integer, Float, Boolean, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    profile_ref = Column(String(255), unique=True, nullable=False)  # ✅ Unique profile ID
    status = Column(Integer, nullable=False)  # ✅ Store only prediction (0: Fake, 1: Legit)
