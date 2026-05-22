import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
    DB_NAME = os.getenv('DB_NAME', 'enterprise_mobile')

    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@'
        f'{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'pool_size': 10,
        'max_overflow': 20,
    }

    JWT_SECRET = os.getenv('JWT_SECRET', 'default-jwt-secret')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', 2))

    LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
