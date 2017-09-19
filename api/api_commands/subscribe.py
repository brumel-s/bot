from api.api_commands.base_command import BaseCommand
import json
import pprint

class Subscribe(BaseCommand):

    CMD_NAME = '/subscribe'

    def is_acceptable(self, text_cmd):
        if text_cmd.startswith(self.CMD_NAME):
            return True
        return False

    def validate(self, text_cmd, user):
        return super(Subscribe, self).check_api_key(user)

    def run(self, telegram_update, user):
        text_cmd = telegram_update.message
        errors = self.validate(text_cmd, user)
        if errors:
            return super(Subscribe, self).prepare_error_response(errors.pop())

        api = super(Subscribe, self).get_api(user)

        subscribe_params = self.fetch_params(text_cmd)
        text_response = self.prepare_text_response(api.run("subscribe", subscribe_params))
        super(Subscribe, self).log_request_response(user, text_cmd, text_response)

        return text_response

    def fetch_params(self, text_cmd):
        if ' ' in text_cmd:
            parts = text_cmd.split(' ')
            return {"list_ids": parts[1], "fields[email]": parts[2]}

    def prepare_text_response(self, response):
        response = json.loads(response)
        if "error" in response.keys():
            return "Error: " + response['error']

        return response['result']

