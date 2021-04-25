import orjson

class Message:
    def __init__(self, T):
        self.T = T()

    @property
    def dict(self):
        return dict(method = type(self.T).__name__, kwargs = self.T.__dict__)

    def dumps(self):
        json = dict(method = type(self.T).__name__, args = self.T.__dict__)
        json_str = orjson.dumps(json)
        json_str.encode("utf-8")

        print('json: ' + json_str)

class reqBody():
    def __init__(self):
        self.id = 'body.id'
        self.data = ''

class add_user():
    def __init__(self):
        self.type = 'body.idhkjfhdskfhkshkf'
        self.text = 'textfkdjsfhkjshkfjdshfskjh'
        self.uname = 'unameghfgjsdgfjhsfgsdjhfgs'


#req = Message(add_user)
#req.T.uname = 'body.data'
