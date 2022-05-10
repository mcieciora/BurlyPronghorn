from bottle import request, route, run
from mongodb import MongoDb


@route('/<request_type>')
def index(request_type):
    pass


def verify_payload():
    pass


class Api:
    def __init__(self, payload_dict):
        self.payload_dict = payload_dict

    def action(self):
        pass


class Find(Api):
    def __init__(self, payload_dict):
        super().__init__(payload_dict=payload_dict)

    def action(self):
        pass


class Insert(Api):
    def __init__(self, payload_dict):
        super().__init__(payload_dict=payload_dict)

    def action(self):
        pass


class Delete(Api):
    def __init__(self, payload_dict):
        super().__init__(payload_dict=payload_dict)

    def action(self):
        pass


run(host='localhost', port=8000)
