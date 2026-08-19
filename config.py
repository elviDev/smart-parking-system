import os
from dotenv import load_dotenv


# Load environment variables from .env when present (not committed)
load_dotenv()

class Config:
    # SECRET_KEY should be set in environment for production. Keep .env out of VCS.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, 'instance', 'parking.db')
    # Allow overriding via DATABASE_URL, but normalize relative sqlite paths to absolute
    env_db = os.environ.get('DATABASE_URL')
    if env_db and env_db.startswith('sqlite:///'):
        # get path portion after sqlite:///
        sqlite_path = env_db[len('sqlite:///'):]
        if not os.path.isabs(sqlite_path):
            sqlite_path = os.path.abspath(sqlite_path)
            SQLALCHEMY_DATABASE_URI = f'sqlite:///{sqlite_path}'
        else:
            SQLALCHEMY_DATABASE_URI = env_db
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{DB_PATH}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CAMERA_SOURCE = 0
    PARKING_THRESHOLD = 0.5
    MIN_PARKING_AREA = 1000
