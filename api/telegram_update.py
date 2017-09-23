class TelegramUpdate:
    def __init__(self, update):
        """
        Prepare TelegramUpdate from raw telegram update
        :param update: dict
        """
        self.id = update['message_id']

        if 'text' in update.keys():
            self.message = update['text']
        self.phone = None
        if 'contact' in update.keys():
            self.phone = update['contact']['phone_number']
        self.chat_id = update['chat']['id']

        try:
            first_name = update['from']['first_name']
        except KeyError:
            first_name = ''
        try:
            last_name = update['from']['last_name']
        except KeyError:
            last_name = ''
        try:
            username = update['from']['username']
        except KeyError:
            username = ''

        self.username = "%s %s (%s)" % (first_name, last_name, username)
        self.user_id = update['from']['id']
