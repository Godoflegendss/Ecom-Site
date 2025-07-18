import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'  # or use MySQL/Postgres in prod
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get("EMAIL_USER")
MAIL_PASSWORD = os.environ.get("EMAIL_PASS")
