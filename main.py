from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.models import Base, Profile
from app.schemas import BulkProfilesRequest, SuccessResponse, ErrorResponse
from app.predictor import predict_profile
from app.constants import SUCCESS, ERRORS
from app.services import store_profile
from app.database import SessionLocal, engine

app = FastAPI()

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/predict-profiles", response_model=SuccessResponse, responses={400: {"model": ErrorResponse}})
def add_profiles(request: BulkProfilesRequest = Body(...), db: Session = Depends(get_db)):
    print("Prediction profile API called")

    try:
        predictions = []

        for profile_data in request.profiles:
            profile_dict = profile_data.dict()  # Converts the Pydantic model to a dictionary

            # Extract the username and platform_ref from the incoming data
            username = profile_dict.get("username")
            platform_ref = profile_dict.get("platform_ref")

            # Ensure both username and platform_ref are provided
            if not username or not platform_ref:
                raise HTTPException(
                    status_code=400,
                    detail="Both 'username' and 'platform_ref' must be provided in the request."
                )

            # Get prediction (0 = Fake, 1 = Legit) based on the features in the dataset
            status = predict_profile(profile_dict)  # Predicts using the updated model

            # Store the profile with username and platform_ref
            profile_dict["username"] = username
            profile_dict["platform_ref"] = platform_ref

            # Store the profile and return it
            stored_profile = store_profile(db, profile_dict, status)

            # Append result with username and prediction (Fake/Legit)
            predictions.append({
                "username": username,
                "platform_ref": platform_ref,
                "prediction": "Fake" if status == 0 else "Legit"
            })

        return SuccessResponse(
            code=SUCCESS["code"],
            message="Profiles predicted successfully!",
            data=predictions
        ).dict()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                code=ERRORS["INTERNAL_ERROR"]["code"],
                message=ERRORS["INTERNAL_ERROR"]["message"],
                details=str(e)
            ).dict()
        )
    finally:
        db.rollback()  # Rollback in case of any exception