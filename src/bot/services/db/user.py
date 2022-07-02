from asgiref.sync import sync_to_async

from app.models import TelegramUser, UserAnswers


@sync_to_async
def get_user(user_id) -> TelegramUser:
    user = TelegramUser.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def add_user(user_id, name):
    user = TelegramUser(user_id=user_id, name=name)
    user.save()
    return user


@sync_to_async
def get_user_answers(user):
    return UserAnswers.objects.filter(user=user).all()


@sync_to_async
def update_user_answers(user, original):
    return UserAnswers(user=user, original=original).save()
