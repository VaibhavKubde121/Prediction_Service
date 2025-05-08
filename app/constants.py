# General Success Message
SUCCESS = {"code": 200, "message": "Success"}

# Error Codes and Messages
ERRORS = {
    "BAD_REQUEST": {"code": 2001, "message": "Invalid request format. Please check the input data"},
    "NOT_FOUND": {"code": 2002, "message": "Resource not found."},
    "INTERNAL_ERROR": {"code": 2003, "message": "Internal Server Error."},
    "DB_ERROR": {"code": 2004, "message": "Database error. Please try again later."},
    "VALIDATION_ERROR": {"code": 2005, "message": "Validation failed. Check input data."},

    # Added new error types for fake profile detection
    "FAKE_PROFILE_DETECTION_ERROR": {"code": 2006, "message": "Error in fake profile detection process."},
    "PROFILE_STORAGE_ERROR": {"code": 2007, "message": "Error storing profile in the database."},
    "PREDICTION_ERROR": {"code": 2008, "message": "Error in profile prediction process."},

    # Additional error types could go here
}
