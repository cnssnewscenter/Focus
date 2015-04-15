class APIError(Exception):
    status_code = 500

    def __init__(self, err_code, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.err_code = err_code
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        ret = dict(self.payload or ())
        ret["message"] = self.message
        ret["err"] = self.status_code
        return ret


class WrongPostData(APIError):
    status_code = 400
