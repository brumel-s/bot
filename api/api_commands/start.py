from api.api_commands.base_command import BaseCommand
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

class Start(BaseCommand):
    """
    Request user phone number to try setup api key
    """

    CMD_NAME = '/start'

    def is_acceptable(self, text_cmd):
        if text_cmd.startswith(self.CMD_NAME):
            return True
        return False

    def run(self, bot, telegram_update, user):
        """
        Run command and send response to user

        :param bot: Bot
        :param telegram_update: TelegramUpdate
        :param user: TeleUser
        :return: void
        """
        message = "Для начала работы с ботом необходимо установить API ключ." \
                   "\r\nНажмите кнопку \"Предоставить номер\" и мы сделаем это автоматически " \
                   "(при совпадении с номером телефона указаным при регистрации в UniSender). " \
                   "\r\nТакже установить ключ Вы можете самостоятельно, используя команду" \
                   "\r\n/setApiKey {ApiKey}"

        bot.sendMessage(telegram_update.chat_id, message,
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=[
                                [KeyboardButton(text='Предоставить номер', request_contact=True)]
                            ],
                            one_time_keyboard=True
                        ))
