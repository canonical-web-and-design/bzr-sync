import re


class Logger:
    log = ''

    def update(self, explanation, command_output):
        title = "=== {0} ===\n".format(explanation)
        print title
        self.log += title

        command = str(command_output) + "\n"
        print command
        self.log += command


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
