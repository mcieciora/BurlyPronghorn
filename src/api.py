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
    try:
        request_object = requests[request_type](payload)
    except ValueError:
        return HTTPResponse(status=400, body=dict(data=[{'status': 'Incorrect payload'}]))
    if request_object.verify_payload():
        return request_object.action()
    else:
        return HTTPResponse(status=400, body=dict(data=[{'status': 'Incorrect payload'}]))


class Api:
    def __init__(self, payload_dict):
        self.payload_dict = payload_dict
        for key, value in self.payload_dict.items():
            key_value = self.payload_dict[key]
            if type(key_value) is list and len(key_value) > 1:
                raise ValueError
            self.payload_dict[key] = value[0]

    def verify_payload(self):
        pass

    def action(self):
        return dict(data=[{'status': 'OK'}])


class Find(Api):
    def __init__(self, payload_dict):
        super().__init__(payload_dict=payload_dict)

    def verify_payload(self):
        # TODO refactor and simplify
        return_value = True
        expected_keys = ['object_name']
        for key, value in self.payload_dict.items():
            if key not in expected_keys:
                return_value = False
            if value == '':
                return_value = False
        return return_value

    def action(self):
        return_value = MongoDb().find(self.payload_dict)
        return dict(data=return_value)


class Insert(Api):
    def __init__(self, payload_dict):
        super().__init__(payload_dict=payload_dict)

    def verify_payload(self):
        # TODO refactor and simplify
        return_value = True
        expected_keys = ['object_name', 'note', 'related_tasks', 'active_days']
        if len(expected_keys) != len(self.payload_dict):
            return_value = False
        if sorted(self.payload_dict) != sorted(expected_keys):
            return_value = False
        if not all([False if not value else True for value in self.payload_dict.values()]):
            return_value = False
        return return_value

    def action(self):
        if MongoDb().insert(self.payload_dict):
            return dict(data=[{'status': 'OK'}])
        else:
            return HTTPResponse(status=400, body=dict(data=[{'status': 'Object already exists'}]))


class Delete(Api):
    def __init__(self, payload_dict):
        super().__init__(payload_dict=payload_dict)

    def verify_payload(self):
        # TODO refactor and simplify
        return_value = True
        expected_keys = ['object_name']
        for key, value in self.payload_dict.items():
            if key not in expected_keys:
                return_value = False
            if value == '':
                return_value = False
        return return_value

    def action(self):
        MongoDb().delete(self.payload_dict)
        return dict(data=[{"status": 'OK'}])


if __name__ == '__main__':
    run(host='0.0.0.0', port=7999)
