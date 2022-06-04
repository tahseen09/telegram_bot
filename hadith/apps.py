import json
from django.apps import AppConfig


class HadithConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hadith"
    file_path = "fixtures/hadith.json"
    with open(file_path) as hadith_file:
        hadiths = json.load(hadith_file)
