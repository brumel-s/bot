from api.api_commands.base_command import BaseCommand
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

class Start(BaseCommand):

    CMD_NAME = '/start'

    def is_acceptable(self, text_cmd):
        if text_cmd.startswith(self.CMD_NAME):
            return True
        return False

    def run(self, bot, telegram_update, user):

        bot.sendMessage(telegram_update.chat_id, 'Предоставьте номер телефона',
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=[
                                [KeyboardButton(text='Share contact', request_contact=True)]
                            ],
                            one_time_keyboard=True
                        ))
