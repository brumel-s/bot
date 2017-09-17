from api.api_commands.base_command import BaseCommand
import json

class GetLists(BaseCommand):

    CMD_NAME = '/getLists'

    def is_acceptable(self, text_cmd):
        if text_cmd.startswith(self.CMD_NAME):
            return True
        return False

    def validate(self, text_cmd, user):
        return super(GetLists, self).check_api_key(user)

    def run(self, telegram_update, user):
        text_cmd = telegram_update.message
        errors = self.validate(text_cmd, user)
        if errors:
            return super(GetLists, self).prepare_error_response(errors.pop())

        api = super(GetLists, self).get_api(user)

        text_response = self.prepare_text_response(api.run("getLists", {}))
        super(GetLists, self).log_request_response(user, text_cmd, text_response)

        return text_response

    def prepare_text_response(self, response):
        response = json.loads(response)
        if "error" in response.keys():
            return "Error: " + response['error']
        results = response['result']
        text_response = ""
        for result in results:
            text_response += "\r\n Id: {}, Title: {}".format(result["id"], result["title"])
            text_response += "\r\n----------"
        return text_response

