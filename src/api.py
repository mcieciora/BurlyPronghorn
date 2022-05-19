from bottle import request, route, run, HTTPResponse
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
    if verify_payload(payload):
        request_object = requests[request_type](payload)
        return request_object.action()
    else:
        return HTTPResponse(status=400, body=dict(data=[{'status': 'Incorrect payload'}]))


def verify_payload(actual_dict):
    return_value = True
    expected_keys = ['object_name', 'note', 'related_tasks', 'active_days']
    if len(expected_keys) != len(actual_dict):
        return_value = False
    if sorted(actual_dict) != sorted(expected_keys):
        return_value = False
    if all([False if not value[0] else True for value in actual_dict.values()]):
        return_value = False
    return return_value


class Api:
    def __init__(self, payload_dict):
        self.payload_dict = payload_dict
        for key, value in self.payload_dict.items():
            self.payload_dict[key] = value[0]

    def action(self):
        return dict(data=[{'status': 'OK'}])


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
        return dict(data=[{'status': 'OK'}])


class Delete(Api):
    def __init__(self, payload_dict):
        super().__init__(payload_dict=payload_dict)

    def action(self):
        pass


run(host='0.0.0.0', port=7999)
