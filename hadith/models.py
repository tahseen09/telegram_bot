from django.db import models


class Chat(models.Model):
    class Language(models.TextChoices):
        ENGLISH = "en"

    chat_id = models.CharField(max_length=128, unique=True, db_index=True)
    language = models.CharField(max_length=32, choices=Language.choices, default=Language.ENGLISH)

    def __str__(self) -> str:
        return self.chat_id
