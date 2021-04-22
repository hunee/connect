print('__FILE__: ', __file__)

from .. import handler

from ..models.users import 사용자_정보

@handler.event
def send(c, type, text):
    print('>> def: ' + send.__name__)

    print('c:',str(c), ' type:', type, ' text:', text)


@handler.function
def send_fn(c, type, text, msg):
    print('>> def: ' + send_fn.__name__)

    print('c:',str(c), ' type:', type, ' text:', text, ' msg:', msg)

    query = 사용자_정보.select()
    print('query: ', query)

    return {'query': 'query'}


