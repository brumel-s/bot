from api.api_commands.base_command import BaseCommand
from bot import settings
from api.uni_api import UniApi
import json, pprint

class SavePhone(BaseCommand):
    """
    Save user phone
    """

    def run(self, bot, telegram_update, user):

        api = UniApi(settings.UNI_GET_PHONE_USER_TOKEN)

        phoneResponse = api.run("getApiKey", {"phone": telegram_update.phone})
        phoneResponse = json.loads(phoneResponse)
        pprint.pprint(phoneResponse)

        if "error" in phoneResponse.keys():
            error = "Во время выполнения запроса произошла ошибка: " + phoneResponse['error']
            error += "\r\nУстановите API ключ с помощью команды:"
            error += "\r\n/setApiKye {ApiKey}"
            bot.sendMessage(telegram_update.chat_id, error)
            return

        user.phone = telegram_update.phone
        user.uni_api_key = phoneResponse['result']['api_key']
        user.save()

        response = 'API ключ установлен'
        super(SavePhone, self).log_request_response(user, 'Phone request', response)

        bot.sendMessage(telegram_update.chat_id, response)
