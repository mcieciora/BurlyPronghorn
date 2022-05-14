from bottle import request, route, run
from mongodb import MongoDb


@route('/<request_type>')
def index(request_type):
    requests = {
        'api': Api,
        'insert': Insert,
        'find': Find,
        'delete': Delete
    }
    payload = request.query.dict
    if verify_payload(request.query.dict):
        request_object = requests[request_type](payload)
        request_object.action()


def verify_payload(actual_dict):
    return_value = True
    expected_keys = ['object_name', 'note', 'related_tasks', 'active_days']
    if len(expected_keys) != len(actual_dict):
        return_value = False
    if sorted(actual_dict) != sorted(expected_keys):
        return_value = False
    return return_value


class Api:
    def __init__(self, payload_dict):
        self.payload_dict = payload_dict
        for key, value in self.payload_dict.items():
            self.payload_dict[key] = value[0]

    def action(self):
        return dict(data=[{"status": 'OK'}])


class Find(Api):
    def __init__(self, payload_dict):
        super().__init__(payload_dict=payload_dict)

    def action(self):
        pass


class Insert(Api):
    def __init__(self, payload_dict):
        super().__init__(payload_dict=payload_dict)

    def action(self):
        MongoDb().insert(self.payload_dict)
        return dict(data=[{"status": 'OK'}])


class Delete(Api):
    def __init__(self, payload_dict):
        super().__init__(payload_dict=payload_dict)

    def action(self):
        pass


run(host='localhost', port=7999)
