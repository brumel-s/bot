class TelegramUpdate:
    def __init__(self, update):
        self.id = update['message_id']

        if 'text' in update.keys():
            self.message = update['text']
        self.phone = None
        if 'contact' in update.keys():
            self.phone = update['contact']['phone_number']
        self.chat_id = update['chat']['id']
        self.username = "%s %s (%s)" % (update['from']['first_name'], update['from']['last_name'], update['from']['username'])
        self.user_id = update['from']['id']
