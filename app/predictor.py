import xgboost as xgb
import pandas as pd

def predict_profile(profile_data):
    # Convert input data to a DataFrame
    df = pd.DataFrame([profile_data])

    # Load the trained model
    model = xgb.Booster()
    model.load_model("models/fake_profile_model.json")

    # Ensure the input data has the expected features based on the updated schema
    expected_features = [
        "username_length", "num_digits_in_username", "profile_has_picture",
        "profile_has_bio", "bio_word_count", "spam_word_count", "suspicious_words_in_bio",
        "bio_sentiment_score", "followers_count", "follows_count", "friend_follower_ratio",
        "posts_count", "activity_score", "joined_recently", "is_verified"
    ]

    # Ensure only required features are passed (columns in DataFrame must match expected features)
    dmatrix = xgb.DMatrix(df[expected_features])

    # Get prediction probability (the model will output a probability)
    probability = model.predict(dmatrix)[0]

    # Apply threshold (0.5 is standard for binary classification)
    predicted_label = 1 if probability >= 0.5 else 0

    return predicted_label  # Returns 0 (Fake) or 1 (Legit)
