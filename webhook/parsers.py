class ParserDefault():
    def parse(self, message):
        if "hi" in message.lower():
            return 'Hi bro!'
        return None
