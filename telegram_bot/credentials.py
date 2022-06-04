import os
from dotenv import load_dotenv

load_dotenv()

APP_URL = os.environ["APP_URL"]

BOT_USERNAME = os.environ["BOT_USERNAME"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

DJANGO_SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]