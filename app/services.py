from sqlalchemy.orm import Session
from app.models import Profile
import hashlib
from typing import Dict

def generate_profile_ref(profile_data: Dict):
    """Generate a unique hash for the profile based on its features."""
    # Convert profile data to a string for hashing
    profile_str = str(profile_data)  # Ensure profile_data is in dict format
    return hashlib.md5(profile_str.encode()).hexdigest()  # Generate hash


def store_profile(db: Session, profile_data: Dict, status: int):
    """Store the profile reference and status in the database."""
    profile_ref = generate_profile_ref(profile_data)

    # Check if the profile already exists
    existing_profile = db.query(Profile).filter(Profile.profile_ref == profile_ref).first()
    if existing_profile:
        print("Duplicate profile occured")
        return existing_profile  # Avoid duplicate insertion


    print("Profile added to the database")
    # Insert new profile with the prediction status (0: Fake, 1: Legit)
    new_profile = Profile(profile_ref=profile_ref, status=status)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile
