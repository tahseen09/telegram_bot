import random
from hadith.apps import HadithConfig
from hadith.models import Chat


def get_random_hadith():
    hadiths = HadithConfig.hadiths
    hadith = random.choice(hadiths)
    return f"{hadith['En_Sanad']} \n {hadith['En_Text']}"


def create_chat(chat_id: str):
    chat = Chat(chat_id=chat_id)
    chat.save()
