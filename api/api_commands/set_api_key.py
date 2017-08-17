from api.api_commands.base_command import BaseCommand


class SetApiKey(BaseCommand):
    """
    Set user api key
    """

    CMD_NAME = '/set_api_key'

    def is_acceptable(self, text_cmd):
        if text_cmd.startswith(self.CMD_NAME):
            return True
        return False

    def validate(self, text_cmd):
        api_key = self.fetch_api_key(text_cmd)
        errors = []
        if not api_key:
            errors.append("Api key is not provided")
        return errors

    def fetch_api_key(self, text_cmd):
        parts = text_cmd.partition(' ')
        return parts[2]

    def run(self, telegram_update, user):
        text_cmd = telegram_update.message
        errors = self.validate(text_cmd)
        if errors:
            return super(SetApiKey, self).prepare_error_response(errors.pop())
        api_key = self.fetch_api_key(text_cmd)
        user.uni_api_key = api_key
        user.save()

        return "Done!"
