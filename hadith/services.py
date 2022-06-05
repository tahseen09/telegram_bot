import random
from typing import Optional, Union
import telegram

from hadith.apps import HadithConfig
from hadith.constants import LANGUAGE_COMMAND, START_COMMAND, SUBSCRIBE_COMMAND, SUPPORTED_LANGUAGES
from hadith.models import Chat
from telegram_bot.credentials import BOT_TOKEN, APP_URL

bot = telegram.Bot(token=BOT_TOKEN)


def get_random_hadith(language: Chat.Language = Chat.Language.ENGLISH) -> str:
    hadiths_map = HadithConfig.hadiths
    hadiths = hadiths_map[language]
    hadith = random.choice(hadiths)
    return hadith["title"]

def create_chat(chat_id: str) -> Chat:
    chat, _ = Chat.objects.get_or_create(chat_id=chat_id)
    return chat

def update_language_preference(chat_id: str, language: Union[Chat.Language, str]) -> None:
    chat = get_chat(chat_id)
    if chat:
        chat.language = language
        chat.save()

def get_response(text: str, chat_id: str) -> str:
    text_response_map = {
        START_COMMAND: f"Assalamu-aliakum! I am Tahseen Rahman.\nUse this bot to read Hadiths and make your day better.\nYou can message anything and you shall receive a hadith in response. Or you can also message {SUBSCRIBE_COMMAND} to receive Hadiths Daily. Jazakallah.",
        SUBSCRIBE_COMMAND: "Jazakallah. You have been subscribed to daily hadiths. To read a hadith right now, message anything.",
        LANGUAGE_COMMAND: "Your preferred language of hadees has been changed to {language}"
    }
    if LANGUAGE_COMMAND in text:
        language = text.split()[-1]
        text = text.split()[0]
        if language.lower() not in SUPPORTED_LANGUAGES:
            return f"We currently support only English(en) and Urdu(ur). For example - to choose english language type {LANGUAGE_COMMAND} en and send."
        return text_response_map[LANGUAGE_COMMAND].format(language=SUPPORTED_LANGUAGES[language])

    language = Chat.Language.ENGLISH
    chat = get_chat(chat_id)
    if chat:
        language = chat.language

    return text_response_map.get(text, get_random_hadith(language))


def send_message(chat_id: str, message: str) -> bool:
    try:
        bot.sendMessage(chat_id=chat_id, text=message)
        return True
    except Exception:
        return False


def get_telegram_update_object(request_body: dict) -> telegram.Update:
    return telegram.Update.de_json(request_body, bot)


def set_telegram_webhook() -> bool:
    return bot.setWebhook(f"{APP_URL}{BOT_TOKEN}")


def send_hadith_to_all_users() -> None:
    # TODO: Optimise it to send multiple messages at once (Probably using threading)
    chats = Chat.objects.all()
    random_hadits_map = {
        Chat.Language.ENGLISH: get_random_hadith(Chat.Language.ENGLISH),
        Chat.Language.URDU: get_random_hadith(Chat.Language.URDU)
    }
    for chat in chats:
        hadith = random_hadits_map[chat.language]
        send_message(chat.chat_id, hadith)


def get_chat(chat_id: str) -> Optional[Chat]:
    try:
        return Chat.objects.get(chat_id=chat_id)
    except Chat.DoesNotExist:
        return None
