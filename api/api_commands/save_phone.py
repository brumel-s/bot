from api.api_commands.base_command import BaseCommand
from bot import settings
from api.uni_api import UniApi
import json
from api.exceptions import CmdException

class SavePhone(BaseCommand):
    """
    Save user phone
    """

    def run(self, bot, telegram_update, user):
        """
        Run command and send response to user

        :param bot: Bot
        :param telegram_update: TelegramUpdate
        :param user: TeleUser
        :return: void
        """
        api = UniApi(settings.UNI_GET_PHONE_USER_TOKEN)
        phoneResponse = api.run("getApiKey", {"phone": telegram_update.phone})
        phoneResponse = json.loads(phoneResponse)

        if "error" in phoneResponse.keys():
            error = "Во время выполнения запроса произошла ошибка: {}" \
                    "\r\nУстановите API ключ с помощью команды:" \
                    "\r\n/setApiKey {}".format(phoneResponse['error'], '{ApiKey}')
            error += ""
            error += ""
            raise CmdException(error)

        user.phone = telegram_update.phone
        user.uni_api_key = phoneResponse['result']['api_key']
        user.save()

        bot.sendMessage(telegram_update.chat_id, 'API ключ установлен')
