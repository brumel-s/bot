from api.api_commands.base_command import BaseCommand

class SavePhone(BaseCommand):
    """
    Save user phone
    """

    def run(self, telegram_update, user):

        user.phone = telegram_update.phone
        user.save()

        response = 'Your phone has been saved'
        super(SavePhone, self).log_request_response(user, 'Phone request', response)

        return response
