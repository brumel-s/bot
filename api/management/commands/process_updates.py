from django.core.management.base import BaseCommand
from bot import settings
import telepot, time
from api.command_factory import CommandFactory
from api.telegram_update import TelegramUpdate

from api.models import TeleUser

TelegramBot = telepot.Bot(settings.BOT_TOCKEN)


class Command(BaseCommand):
    help = 'Process Telegram updates'

    def handle(self, *args, **options):
        TelegramBot.message_loop(self.process_updates)
        while 1:
            time.sleep(10)

    def process_updates(self, update):

        update = TelegramUpdate(update)
        cmd_factory = CommandFactory()
        user = self.fetch_or_create_user(update)
        cmd = cmd_factory.create_cmd(update, user)

        if cmd is not None:
            cmd.run(TelegramBot, update, user)
            return

        TelegramBot.sendMessage(update.chat_id, self.get_help_str())

        return

    def fetch_or_create_user(self, telegram_update):
        """
        Fetch or create user
        :param telegram_user_id: int
        :return: TeleUser
        """
        try:
            user = TeleUser.objects.get(telegram_id=telegram_update.user_id)
        except TeleUser.DoesNotExist:
            user = TeleUser()
            user.telegram_id = telegram_update.user_id
            user.username = telegram_update.username
            user.save()

        return user


    def get_help_str(self):
        """
        Get list of commands

        :return: string
        """
        response = "\r\n Доступные команды:"
        response += "\r\n -------------"
        response += "\r\n /start"
        response += "\r\n Установить API ключ автоматически (при совпадении номера телефона указаного при регистрации в UniSender)"
        response += "\r\n -------------"
        response += "\r\n /set_api_key {ApiKey}"
        response += "\r\n Установить API вручную"
        response += "\r\n например"
        response += "\r\n /set_api_key qwerty123456qwerty"
        response += "\r\n -------------"
        response += "\r\n /campaigns {dateFrom} {dateTo}"
        response += "\r\n Список рассылок. Без параметров выводятся рассылки за 30 дней."
        response += "\r\n Можно указать даты \"от\" и \"до\" или только \"от\""
        response += "\r\n Например"
        response += "\r\n /campaigns 2017-01-01 2017-01-30"
        response += "\r\n или"
        response += "\r\n /campaigns 2017-01-01"
        response += "\r\n -------------"
        response += "\r\n /campaignStats_{campaignId}"
        response += "\r\n например"
        response += "\r\n /campaignStats_12345678"
        response += "\r\n -------------"
        response += "\r\n /getLists"
        response += "\r\n Вывести списки"
        response += "\r\n -------------"
        response += "\r\n /subscribe {listId} {email}"
        response += "\r\n Подписать емеил на рассылку"
        response += "\r\n например"
        response += "\r\n /subscribe 87654321 test@example.com"

        return response
