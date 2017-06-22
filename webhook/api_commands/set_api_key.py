from webhook.api_commands.base_command import BaseCommand


class SetApiKey(BaseCommand):
    """
    Show user campaigns
    """

    CMD_NAME = '/setApiKey'

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

    def run(self, text_cmd):
        errors = self.validate(text_cmd)
        if errors:
            return super(SetApiKey, self).prepare_error_response(errors.pop())
        api_key = self.fetch_api_key(text_cmd)
        self.user.uni_api_key = api_key
        self.user.save()

        return "Done!"
