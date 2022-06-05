import json
import os
from django.apps import AppConfig
from telegram_bot.credentials import BASE_DIR


def load_hadiths_fixtures() -> dict:
    return {
        "en": load_english_hadiths(),
        "ur": load_urdu_hadiths(),
    }


def load_hadiths(file_path: str) -> list:
    with open(file_path) as hadith_file:
        return json.load(hadith_file)


def load_urdu_hadiths() -> list:
    file_path = os.path.join(BASE_DIR, "fixtures/hadith_ur.json")
    return load_hadiths(file_path)


def load_english_hadiths() -> list:
    file_path = os.path.join(BASE_DIR, "fixtures/hadith_en.json")
    return load_hadiths(file_path)


class HadithConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hadith"
    hadiths = load_hadiths_fixtures()
