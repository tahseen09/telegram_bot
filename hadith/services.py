import random
import telegram

from hadith.apps import HadithConfig
from hadith.models import Chat
from telegram_bot.credentials import BOT_TOKEN, APP_URL


bot = telegram.Bot(token=BOT_TOKEN)


def get_random_hadith() -> str:
    hadiths = HadithConfig.hadiths
    hadith = random.choice(hadiths)
    return f"{hadith['En_Sanad']} \n {hadith['En_Text']}"


def create_chat(chat_id: str) -> None:
    chat = Chat(chat_id=chat_id)
    chat.save()


def get_response(text: str) -> str:
    text_response_map = {
        "/start": "Assalamu-aliakum! I am Tahseen Rahman.\nUse this bot to read Hadiths and make your day better. You can message anything and you shall receive a hadith in response. Or you can also message /subscribe to receive Hadiths Daily. Jazakallah.",
        "/subscribe": "Jazakallah. You have been subscribed to daily hadiths. To read a hadith right now, message anything.",
    }
    return text_response_map.get(text, get_random_hadith())


def send_message(chat_id: str, message: str) -> bool:
    try:
        bot.sendMessage(chat_id=chat_id, text=message)
        return True
    except Exception:
        return False


def get_telegram_update_object(request_body: dict) -> telegram.Update:
    return telegram.Update.de_json(request_body, bot)


def set_telegram_webhook():
    return bot.setWebhook(f"{APP_URL}{BOT_TOKEN}")


def send_hadith_to_all_users():
    chats = Chat.objects.all()
    hadith = get_random_hadith()
    for chat in chats:
        send_message(chat.chat_id, hadith)
