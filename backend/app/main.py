#print('__FILE__: ', __file__)

import asyncio

import logging
import sys


###
import message


from app import api
from app import models

from app.models import user

'''
class User(Model):
    meta = {
        'tablename': 'tbl_users'
    }

    email = StringField()
    name = StringField()
    age = IntField()
    
    @property
    def json(self):
        return {
            'email': self.email,
            'name': self.name,
            'age': self.age
        }
    
    
def get_user_list(age_matches):
    results = User.query(age=age_matches).all()
    
    return [res.json for res in results]

    
#message = "success" if score >= 60 else "failure"
#조건문이 참인 경우 if 조건문 else 조건문이 거짓인 경우

return [res.json for res in results]
'''



###
logger = logging.getLogger(__name__)

class server(message.post):
    def __init__(self, debug: bool = False) -> None:
        
        super().__init__(debug)

        asyncio.ensure_future(user.connect())
        asyncio.ensure_future(models.battle_connect())

def main():
    app = server(debug=True)
    return app

app = main()
