from api.api_commands.base_command import BaseCommand
from bot import settings
from api.uni_api import UniApi
import json, pprint

class SavePhone(BaseCommand):
    """
    Save user phone
    """

    def run(self, telegram_update, user):

        api = UniApi(settings.UNI_GET_PHONE_USER_TOKEN)

        phoneResponse = api.run("getApiKey", {"phone": telegram_update.phone})
        phoneResponse = json.loads(phoneResponse)
        pprint.pprint(phoneResponse)

        user.phone = telegram_update.phone
        user.uni_api_key = phoneResponse['result']['api_key']
        user.save()

        response = 'Your phone has been saved'
        super(SavePhone, self).log_request_response(user, 'Phone request', response)

        return response
