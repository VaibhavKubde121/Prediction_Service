from pydantic import BaseModel
from typing import List, Optional

# Schema for a single profile request (with username)
class FeatureRequest(BaseModel):
    username: str
    platform_ref: str
    username_length: int
    num_digits_in_username: int
    profile_has_picture: int  # changed from bool to int
    profile_has_bio: int      # changed from bool to int
    bio_word_count: int
    spam_word_count: int
    suspicious_words_in_bio: int
    bio_sentiment_score: float
    followers_count: int
    follows_count: int
    friend_follower_ratio: float
    posts_count: int
    activity_score: float
    joined_recently: int      # changed from bool to int
    is_verified: int

# Schema for bulk profiles request
class BulkProfilesRequest(BaseModel):
    profiles: List[FeatureRequest]

# Individual prediction result with only username and prediction
class PredictionResult(BaseModel):
    username: str
    prediction: str

# Success response schema
class SuccessResponse(BaseModel):
    status: str = "success"
    code: int
    message: str
    data: List[PredictionResult]

# Error response schema
class ErrorResponse(BaseModel):
    status: str = "error"
    code: int
    message: str
    details: Optional[str] = None