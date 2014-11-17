import re


class ShLogger:
    log = ''

    def update_for_command(self, explanation, command_output=None):
        self.update("=== {0} ===\n".format(explanation))

        if command_output:
            self.update(str(command_output) + "\n")

    def update(self, message):
        print message
        self.log += message


def query_params(environ):
    """
    Splits a query string into a dictionary
    "hello=world&fish=chips;yin=yang"
    to:
    {'hello': 'world', 'fish': 'chips', 'yin': 'yang'}
    """

    query_params = {}

    query_items = re.split('[&;]', environ['QUERY_STRING'])

    for query_item in filter(len, query_items):
        (name, value) = query_item.split('=')

        query_params[name] = value

    return query_params
