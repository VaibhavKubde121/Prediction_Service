from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    platform_ref = Column(String(50), nullable=False)  # NEW column to track platform
    status = Column(Integer, nullable=False)  # 0: Fake, 1: Legit

    # Ensures unique username + platform combination
    __table_args__ = (
        UniqueConstraint('username', 'platform_ref', name='unique_user_platform'),
    )