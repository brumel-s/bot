from webhook.uni_api import UniApi


class BaseCommand():
    """
    Base command
    """
    def set_user(self, user):
        self.user = user

    def check_api_key(self):
        errors = []
        if not self.user.uni_api_key:
            errors.append("Set api key first! Use /set_api_key {api_key}")
        return errors

    def prepare_error_response(self, message):
        return message

    def get_api(self):
        return UniApi(self.user.uni_api_key)

    def parse_arguments(self, text_cmd):
        parts = text_cmd.split("_")
        parts.pop(0)

        return parts