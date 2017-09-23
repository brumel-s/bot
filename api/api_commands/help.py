from api.api_commands.base_command import BaseCommand
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

class Help(BaseCommand):
    """
    Request user phone number to try setup api key
    """

    CMD_NAME = '/help'

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
        response = "\r\nДоступные команды:" \
                   "\r\n-------------" \
                   "\r\n*/start*" \
                   "\r\nУстановить API ключ автоматически " \
                   "(при совпадении номера телефона указаного при регистрации в UniSender)" \
                   "\r\n-------------" \
                   "\r\n*/setApiKey {ApiKey}*" \
                   "\r\nУстановить API вручную" \
                   "\r\nнапример" \
                   "\r\n/setApiKey qwerty123456qwerty" \
                   "\r\n-------------" \
                   "\r\n*/campaigns {dateFrom} {dateTo}*" \
                   "\r\nСписок рассылок. Без параметров выводятся рассылки за 30 дней." \
                   "\r\nНапример" \
                   "\r\n/campaigns 2017-01-01 2017-01-30" \
                   "\r\nили" \
                   "\r\n/campaigns 2017-01-01" \
                   "\r\n-------------" \
                   "\r\n*/campaignStats {campaignId}*" \
                   "\r\nнапример" \
                   "\r\n/campaignStats 12345678" \
                   "\r\n-------------" \
                   "\r\n*/getLists*" \
                   "\r\nВывести списки" \
                   "\r\n-------------" \
                   "\r\n*/subscribe {listId} {email}*" \
                   "\r\nПодписать емеил на рассылку" \
                   "\r\nнапример" \
                   "\r\n/subscribe 87654321 test@example.com" \

        bot.sendMessage(telegram_update.chat_id, response, parse_mode='Markdown')
