import json
import os
from django.apps import AppConfig
from telegram_bot.credentials import BASE_DIR


class HadithConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hadith"
    file_path = os.path.join(BASE_DIR, "fixtures/hadith.json")
    with open(file_path) as hadith_file:
        hadiths = json.load(hadith_file)
