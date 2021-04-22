"""
pip3 install aiohttp
pip3 install aiomysql
pip3 install aiomcache
pip3 install aioredis

pip3 install aiohttp_jinja2

pip3 install sqlalchemy
pip3 install pyyaml
"""

import asyncio
import functools
import json
import logging
import pathlib

from pprint import pprint

import yaml

import aiohttp
from aiohttp import web

import aiohttp_jinja2
import jinja2

from aiomysql import create_pool

import aiohttp_debugtoolbar
from aiohttp_debugtoolbar import toolbar_middleware_factory

import sqlalchemy as sa

def print_r(the_object):
    print ("CLASS: ", the_object.__class__.__name__, " (BASE CLASS: ", the_object.__class__.__bases__,")")
    pprint(vars(the_object))



"""
"""
PROJ_ROOT = pathlib.Path(__file__).parent.parent
TEMPLATES_ROOT = pathlib.Path(__file__).parent.parent / 'templates'

print('PROJ_ROOT: ', str(PROJ_ROOT))
print('TEMPLATES_ROOT: ', str(TEMPLATES_ROOT))


"""
"""
__all__ = ['question_sa', 'choice_sa']

meta = sa.MetaData()

question_sa = sa.Table(
        'question', meta,
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('question_text', sa.String(200), nullable=False),
        sa.Column('pub_date', sa.Date, nullable=False),

        # Indexes #
        sa.PrimaryKeyConstraint('id', name='question_id_pkey'))

choice_sa = sa.Table(
        'choice', meta,
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('question_id', sa.Integer, nullable=False),
        sa.Column('choice_text', sa.String(200), nullable=False),
        sa.Column('votes', sa.Integer, server_default="0", nullable=False),

        # Indexes #
        sa.PrimaryKeyConstraint('id', name='choice_id_pkey'),
        sa.ForeignKeyConstraint(['question_id'], [question_sa.c.id],
                                name='choice_question_id_fkey',
                                ondelete='CASCADE'),
)

class RecordNotFound(Exception):
    """Requested record in database was not found"""

def json_renderer(func):
    assert asyncio.iscoroutinefunction(func), func

    @asyncio.coroutine
    def wrapper(request):
        response = web.HTTPOk()
        context = yield from func(request)
        try:
            text = json.dumps(context)
        except TypeError:
            raise RuntimeError("{!r} result {!r} is not serializable".format(
                    func, context))
        response.content_type = 'application/json'
        response.text = text
        return response

    return wrapper


@json_renderer
async def store_mp3(request):
    print('>> func: ', store_mp3.__name__)

    data = await request.post()

    mp3 = data['mp3']

    # .filename contains the name of the file in string format.
    filename = mp3.filename

    # .file contains the actual file data that needs to be stored somewhere.
    mp3_file = data['mp3'].file

    content = mp3_file.read()

    #return web.Response(body=content,
    #                    headers=MultiDict(
    #                            {'CONTENT-DISPOSITION': mp3_file}))
    return {'ajax': 'success'}


class MyView(web.View):

    @json_renderer
    async def get(self):
        return {
            'method': 'get',
            'args': dict(self.request.GET),
            'headers': dict(self.request.headers),
        }

    async def post(self):
        print('>> func: ', type(self).__name__, ':', type(self).post.__name__)

        data = await self.request.post()

        mp3 = data['mp3']
        if mp3:
            for v in data.values():
                # .file contains the actual file data that needs to be stored somewhere.
                content = v.file.read()

                with open(str(PROJ_ROOT / 'tmp' / v.filename), 'wb') as out:
                    out.write(content)

        return web.json_response({
            'method': 'post',
            'args': dict(self.request.GET),
            'data': str(data),
            'headers': dict(self.request.headers),
        }, dumps=functools.partial(json.dumps, indent=4))


class router:
    def __init__(self, app, pconn):
        print('func: ', type(self).__name__, ':', type(self).__init__.__name__)

        self.pconn = pconn

        self.add_route(app)

    def __call__(self):
        print('>> func: ')

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        print('>> func: ', type(self).__name__, ':', type(self).index.__name__)

        questions = [{'id':'[dict(q) for q in records]', 'question_text': 'question_text'}]
        return {'questions': questions}

    @aiohttp_jinja2.template('detail.html')
    async def poll(self, request):
        print('>> func: ', type(self).__name__, ':', type(self).poll.__name__)

        question_id = request.match_info['question_id']

        question = {'id':'1', 'question_text': 'question_text'}
        choices = [{'choice_text':'[dict(q) for q in records]', 'votes': 'question_text'}]
        return {
            'question': question,
            'choices': choices
        }

    @aiohttp_jinja2.template('results.html')
    async def results(self, request):
        print('>> func: ', type(self).__name__, ':', type(self).results.__name__)

        question_id = request.match_info['question_id']
        print('question_id: ', question_id)

        #try:
        #    question, choices = await db.get_question(self.postgres,
        #                                              question_id)
        #except db.RecordNotFound as e:


        query = question_sa.select()
        print('query: ', query)

        async with self.pconn.get() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SHOW TABLES")
                value = await cur.fetchone()
                print(value)

        #e = 'db_record_not_found'
        #raise web.HTTPNotFound(text=str(e))

        #print('eeeeee', e)

        question = {'id':'1', 'question': 'question_text'}
        choices = [{'choice_text':'[dict(q) for q in records]', 'votes': 'question_text'}]
        return {
            'question': question,
            'choices': choices
        }

    async def vote(self, request):
        print('>> func: ', type(self).__name__, ':', type(self).vote.__name__)

        question_id = int(request.match_info['question_id'])
        data = await request.post()

        router = request.app.router
        url = router['results'].url(parts={'question_id': question_id})
        return web.HTTPFound(location=url)

    async def handle(self, request):
        print('>> func: ', type(self).__name__, ':', type(self).handle.__name__)

        name = request.match_info.get('name', "Anonymous")
        text = "Hello, " + name
        #return web.Response(body=text.encode('utf-8'))
        return web.json_response({'foo': 42})

    def add_route(self, app):
        print('>> func: ', type(self).__name__, '->', type(self).add_route.__name__)


        """
        """
        aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(TEMPLATES_ROOT)))


        """
        """
        app.router.add_static('/static/',
                              path=str(PROJ_ROOT / 'static'),
                              name='static')

        app.router.add_route('GET', '/', self.index)
        app.router.add_route('GET', '/poll/{question_id}', self.poll, name='poll')
        app.router.add_route('GET', '/poll/{question_id}/results', self.results, name='results')
        app.router.add_route('POST', '/poll/{question_id}/vote', self.vote, name='vote')

        #app.router.add_route('POST', '/store_mp3', store_mp3, name='store_mp3')
        app.router.add_route('*', '/store_mp3', MyView)


async def __init__():
    print('>> func: ', __init__.__name__)

    # load config from yaml file
    pathname = str(PROJ_ROOT / 'config' / 'app.yaml')
    with open(pathname, 'rt') as f:
        conf = yaml.load(f)

    """
    """
    dbconfig = conf['mysql']
    pconn = await create_pool(host=dbconfig['host'],
                              port=dbconfig['port'],
                              user=dbconfig['user'],
                              password=dbconfig['password'],
                              db=dbconfig['database'])


    """
    """
    app = web.Application(middlewares=[toolbar_middleware_factory])

    aiohttp_debugtoolbar.setup(app, intercept_exc='debug')


    """
    """
    async def close_pool(app):
        pconn.close()
        await pconn.wait_closed()

    app.on_cleanup.append(close_pool)


    """
    """
    router(app, pconn)


    """
    """
    host, port = conf['host'], conf['port']

    return app, host, port


def main():
    print('>> func: ', main.__name__)

    # init logging
    logging.basicConfig(level=logging.DEBUG)

    """
    """
    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(__init__())


    """
    """
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()