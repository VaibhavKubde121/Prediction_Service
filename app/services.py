from sqlalchemy.orm import Session
from app.models import Profile
from typing import Dict

def store_profile(db: Session, profile_data: Dict, status: int):
    """Store the profile reference and status in the database."""
    # Extract username and platform_ref from the profile data
    username = profile_data["username"]
    platform_ref = profile_data["platform_ref"]

    # Check if the profile already exists using username and platform_ref
    existing_profile = db.query(Profile).filter(
        Profile.username == username,
        Profile.platform_ref == platform_ref
    ).first()

    if existing_profile:
        print("Duplicate profile occurred")
        return existing_profile  # Avoid duplicate insertion

    print("Profile added to the database")
    # Insert new profile with the prediction status (0: Fake, 1: Legit)
    new_profile = Profile(username=username, platform_ref=platform_ref, status=status)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile