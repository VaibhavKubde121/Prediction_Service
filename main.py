from app.database import SessionLocal, engine
# from app.exceptions import AppException
# from app.exceptions_handler import app_exception_handler
from app.models import Base
from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.models import Profile
from app.schemas import BulkProfilesRequest, SuccessResponse, ErrorResponse
from app.predictor import predict_profile
from app.constants import SUCCESS, ERRORS
from app.services import store_profile, generate_profile_ref

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

    print("prediction profile api get called ")
    try:
        predictions = []

        for profile_data in request.profiles:
            profile_dict = profile_data.dict()  # Converts the Pydantic model to a dictionary

            # # Generate unique profile reference
            # profile_ref = generate_profile_ref(profile_dict)

            # Get prediction (0 = Fake, 1 = Legit)
            status = predict_profile(profile_dict)  # Predicts using the updated model

            # Store the profile (prevents duplicate storage)
            stored_profile = store_profile(db, profile_dict, status)

            # Append results with profile_ref instead of id
            predictions.append({
                "profile_ref": stored_profile.profile_ref,
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


#  Registering the exception Handlers

# uvicorn main:app --reload