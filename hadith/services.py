import random
from typing import Optional, Union
import telegram

from hadith.apps import HadithConfig
from hadith.constants import (
    LANGUAGE_COMMAND,
    START_COMMAND,
    SUBSCRIBE_COMMAND,
    SUPPORTED_COMMANDS,
    SUPPORTED_LANGUAGES,
)
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


def update_language_preference(
    chat_id: str, language: Union[Chat.Language, str]
) -> None:
    chat = get_chat(chat_id)
    if chat:
        chat.language = language
        chat.save()


def identify_command(text: str) -> Optional[str]:
    command = text.split()[0]
    return command.lower()


def handle_start_command(text: str, chat_id: str) -> str:
    return [
        f"Assalamu-aliakum! I am Tahseen Rahman, the creator of this bot.\nUse this bot to read Hadiths and make your day better.\n To receive hadiths daily, message {SUBSCRIBE_COMMAND}.\nTo receive a hadith right away, message hadith.\nJazakallah."
    ]


def get_available_languages_response_copy() -> str:
    supported_languages = [
        f"{name}({code})" for code, name in SUPPORTED_LANGUAGES.items()
    ]

    supported_languages = ", ".join(supported_languages)
    return f"We currently support {supported_languages}.\n To change your language preference, message /language <code>. For example, if you want to change your language of hadeeth to URDU, message /language ur."


def handle_subscribe_command(text: str, chat_id: str) -> list:
    response = "Jazakallah. You have been subscribed to daily hadiths. To read a hadith right now, message anything"
    lang_response = get_available_languages_response_copy()
    return [response, lang_response]


def handle_language_command(text: str, chat_id: str) -> list:
    language = text.split()[-1].lower()
    if language not in SUPPORTED_LANGUAGES:
        response = get_available_languages_response_copy()
    else:
        create_chat(chat_id)
        update_language_preference(chat_id, language)
        response = f"Your preferred language of hadiths has been changed to {SUPPORTED_LANGUAGES[language]}"
    return [response]


def handle_unknown_command(text: str, chat_id: str) -> list:
    supported_commands = ", ".join(SUPPORTED_COMMANDS)
    return [
        f"Uh-Oh! Looks like you have used a command that we don't support.\nThe only commands we support are {supported_commands}. If you are confused, let's try again with the /start command."
    ]


def handle_no_command(text: str, chat_id: str):
    chat = get_chat(chat_id)
    language = Chat.Language.ENGLISH
    if chat:
        language = chat.language
    return [get_random_hadith(language)]


def get_responses(text: str, chat_id: str) -> list:
    if not text.startswith("/"):
        return handle_no_command(text, chat_id)

    command = identify_command(text)
    if command not in SUPPORTED_COMMANDS:
        return handle_unknown_command()

    command_handler_map = {
        START_COMMAND: handle_start_command,
        SUBSCRIBE_COMMAND: handle_subscribe_command,
        LANGUAGE_COMMAND: handle_language_command,
    }

    return command_handler_map[command](text, chat_id)


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
        Chat.Language.URDU: get_random_hadith(Chat.Language.URDU),
    }
    for chat in chats:
        hadith = random_hadits_map[chat.language]
        send_message(chat.chat_id, hadith)


def get_chat(chat_id: str) -> Optional[Chat]:
    try:
        return Chat.objects.get(chat_id=chat_id)
    except Chat.DoesNotExist:
        return None
