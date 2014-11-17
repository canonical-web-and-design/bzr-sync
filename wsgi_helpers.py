import re


class Logger:
    log = ''

    def update(self, explanation, command_output=None):
        self._log("=== {0} ===\n".format(explanation))

        if command_output:
            self._log(str(command_output) + "\n")

    def _log(self, message):
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
