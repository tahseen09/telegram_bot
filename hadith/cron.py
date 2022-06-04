def send_daily_hadith():
    from hadith.services import send_hadith_to_all_users
    send_hadith_to_all_users()


if __name__ == "__main__":
    send_daily_hadith()
