from django.core.management.base import BaseCommand
from bot import settings
import telepot, time, sys, logging, pprint
from api.command_factory import CommandFactory
from api.telegram_update import TelegramUpdate
from api.exceptions import CmdException
import django.db
from django.db.utils import OperationalError

from api.models import TeleUser


class Command(BaseCommand):
    """
    Process telegram updates
    """

    help = 'Process Telegram updates'

    def __init__(self, stdout=None, stderr=None, no_color=False):
        """
        Init Bot
        """
        super(Command, self).__init__(stdout, stderr, no_color)
        self.telegram_bot = telepot.Bot(settings.BOT_TOCKEN)

    def handle(self, *args, **options):
        """
        Handle telegram updates
        """
        self.telegram_bot.message_loop(self.process_updates)
        while 1:
            time.sleep(10)

    def process_updates(self, update):
        """
        Find acceptable command and run

        :param update: dict
        :return: void
        """
        try:
            update = TelegramUpdate(update)
            cmd_factory = CommandFactory()
            user = self.fetch_or_create_user(update)
            cmd = cmd_factory.create_cmd(update, user)

            if cmd is not None:
                cmd.run(self.telegram_bot, update, user)
                return

            raise CmdException('Команда не найдена')

        except CmdException as e:
            self.telegram_bot.sendMessage(update.chat_id, e.args[0])
        except OperationalError:
            log = logging.getLogger("bot_log")
            log.exception('Mysql error. Try to re-connect')
            django.db.close_old_connections()
            self.telegram_bot.sendMessage(update.chat_id, "Во время выполнения запроса произошла ошибка. Попробуйте повторитьзапрос.")
        except Exception:
            log = logging.getLogger("bot_log")
            log.exception('Error on run command')
            self.telegram_bot.sendMessage(update.chat_id, "Во время выполнения запроса произошла ошибка")

        return

    def fetch_or_create_user(self, update):
        """
        Find user in DB or create new

        :param update: TelegramUpdate
        :return:
        """
        try:
            user = TeleUser.objects.get(telegram_id=update.user_id)
        except TeleUser.DoesNotExist:
            user = TeleUser()
            user.telegram_id = update.user_id
            user.username = update.username
            user.save()

        return user
