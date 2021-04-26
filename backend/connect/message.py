import orjson

import base64
import hashlib

class Message:
    def __init__(self, T):
        self.T = T()

    @property
    def dict(self):
        #return base64.b64encode(str(dict(pid = type(self.T).__name__, kwargs = self.T.__dict__)).encode('utf-8'))
        return dict(pid = type(self.T).__name__, kwargs = self.T.__dict__)

    def dumps(self):
        json = dict(pid = type(self.T).__name__, args = self.T.__dict__)
        json_str = orjson.dumps(json)
        json_str.encode("utf-8")

        print('json: ' + json_str)

#request
#response

class RES_ERROR():
    def __init__(self):
        self.message = ''

class RES_Exception():
    def __init__(self):
        self.message = ''

class RES_ADD_USER():
    def __init__(self):
        self.type = 'body.idhkjfhdskfhkshkf'
        self.text = 'textfkdjsfhkjshkfjdshfskjh'
        self.uname = 'unameghfgjsdgfjhsfgsdjhfgs'

'''
#req = Message(add_user)
#req.T.uname = 'body.data'
json_str = ujson.dumps(req.dict)
json_str.encode("utf-8")
'''

'''
text = 'nowonbun';
binary = text.encode('utf-8');
enc = hashlib.md5();
enc.update(binary);
ret = enc.hexdigest();
print(ret);


import base64;
data = base64.b64encode(binary);
binary = base64.b64decode(data);
'''