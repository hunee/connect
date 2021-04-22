
"""
TCP 로 text 전송시 base64 로 인코딩 해서 전송 하면 \n 이 검출 되지 않아서
StreamReader.read_line()  에서 원하는 결과겂을 얻을수 있다.
"""

import logging
import json
import base64

class parser():
    def __init__(self, buffer):
        pass

args_ = {'type':'type', 'msg':'fn', 'text':'b'}
name_ = 'main.send_fn'
type_ = 'fn\n\n'
id_ = 'iid'

# to json
payload = json.dumps(dict(type=type_, name=name_, id=id_, args=args_))
print("org:   ", payload)

# encode base64
encode = base64.b64encode(payload.encode('ascii'))
print('encode: ' + encode.decode("utf-8"))

# decode base64
decode = base64.b64decode(encode)
print('decode: ' + decode.decode("utf-8"))
