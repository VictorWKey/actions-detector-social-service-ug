# Configuration settings for the application

# Camera settings
CAMERA_RESOLUTION = (640, 480)
FRAME_RATE = 30
CAPTURE_SECONDS = 5  # Duration for action capture

# Model settings
MODEL_PATH = "models/action_classifier.joblib"
FEATURES_CONFIG = {
    "use_velocity": True,
    "use_acceleration": True,
    "use_angles": True,
    "normalize": True
}

# Supported actions (extend as needed)
SUPPORTED_ACTIONS = [
    "wave",
    "clap", 
    "point",
    "raise_hand",
    "thumbs_up"
]

# Data paths
RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"
FEATURES_DATA_PATH = "data/features"

# GUI settings
WINDOW_SIZE = (1200, 800)
THEME = "default"