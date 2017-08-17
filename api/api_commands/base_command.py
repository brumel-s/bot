from api.uni_api import UniApi
from api.models import ChatLog

class BaseCommand():
    """
    Base command
    """

    def check_api_key(self, user):
        errors = []
        if not user.uni_api_key:
            errors.append("Set api key first! Use /set_api_key {api_key}")
        return errors

    def prepare_error_response(self, message):
        return message

    def get_api(self, user):
        return UniApi(user.uni_api_key)

    def parse_arguments(self, text_cmd):
        parts = text_cmd.split("_")
        parts.pop(0)

        return parts

    def log_request_response(self, user, text_request, text_response):
        chat_log = ChatLog()
        chat_log.telegram_user = user
        chat_log.request = text_request
        chat_log.response = text_response
        chat_log.save()
