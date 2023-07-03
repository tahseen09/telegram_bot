from django.db import models


class Chat(models.Model):
    class Language(models.TextChoices):
        ENGLISH = "en"
        URDU = "ur"

    chat_id = models.CharField(max_length=128, unique=True, db_index=True)
    language = models.CharField(max_length=32, choices=Language.choices, default=Language.ENGLISH)
    name = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self) -> str:
        return self.chat_id
