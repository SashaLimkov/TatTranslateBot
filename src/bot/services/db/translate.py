from asgiref.sync import sync_to_async

from src.app.models import TelegramUser, OriginalString


@sync_to_async
def add_original(string, str_lenght):
    try:
        r = OriginalString(string=string, length=str_lenght).save()
        return r
    except Exception as e:
        print(e)

