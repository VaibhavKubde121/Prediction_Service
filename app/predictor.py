import xgboost as xgb
import pandas as pd

def predict_profile(profile_data):
    # Define the expected model features
    expected_features = [
        "username_length", "num_digits_in_username", "profile_has_picture",
        "profile_has_bio", "bio_word_count", "spam_word_count", "suspicious_words_in_bio",
        "bio_sentiment_score", "followers_count", "follows_count", "friend_follower_ratio",
        "posts_count", "activity_score", "joined_recently", "is_verified"
    ]

    # Filter out only the expected features for the model
    filtered_data = {key: profile_data[key] for key in expected_features if key in profile_data}
    df = pd.DataFrame([filtered_data])

    # Load the trained XGBoost model
    model = xgb.Booster()
    model.load_model("models/fake_profile_model.json")

    # Convert to DMatrix format for prediction
    dmatrix = xgb.DMatrix(df[expected_features])

    # Predict probability
    probability = model.predict(dmatrix)[0]

    # Binary classification with 0.5 threshold
    predicted_label = 1 if probability >= 0.5 else 0

    return predicted_label  # 0: Fake, 1: Legit