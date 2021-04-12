"""Illustrates the asyncio engine / connection interface.

In this example, we have an async engine created by
:func:`_engine.create_async_engine`.   We then use it using await
within a coroutine.

"""

#print('__FILE__: ', __file__)

import asyncio

import sqlalchemy as sa

from sqlalchemy.ext.asyncio import create_async_engine


#from ..config import config
import app

mysql = app.env['mysql']

#mysql+pymysql://root:password@db:3309/sqlalchemy'
#docker-compose 'db'

# engine is an instance of AsyncEngine
#engine = create_async_engine("mysql+aiomysql://user:pass@hostname/dbname")
DATABASE_URL = '{0}/{1}'.format(app.env['DATABASE_URL'], mysql['database'])
engine = create_async_engine(DATABASE_URL, connect_args={'auth_plugin': 'mysql_native_password'})#, echo=True)

meta = sa.MetaData()

question_sa = sa.Table(
        'question', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('question_text', sa.String(200), nullable=False),
        sa.Column('pub_date', sa.DateTime, server_default=sa.func.now()),

        # Indexes #
        sa.PrimaryKeyConstraint('id', name='question_id_pkey'),

        mysql_partitions="16",
        mysql_partition_by="LINEAR HASH(id)",

)


choice_sa = sa.Table(
        'choice', meta,
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('question_id', sa.Integer, nullable=False),
        sa.Column('choice_text', sa.String(200), nullable=False),
        sa.Column('votes', sa.Integer, server_default="0", nullable=False),

        # Indexes #
        sa.PrimaryKeyConstraint('id', name='choice_id_pkey'),
#        sa.ForeignKeyConstraint(['question_id'], [question_sa.c.id],
#                                name='choice_question_id_fkey',
#                                ondelete='CASCADE'),
)

t1 = sa.Table(
    "t1", meta, 
    sa.Column("id", sa.Integer, primary_key=True), 
    sa.Column("name", sa.String(200)),

    mysql_partitions="16",
    mysql_partition_by="LINEAR HASH(id)",

)

async def connect():
    print('------------ connect')

    # conn is an instance of AsyncConnection
    async with engine.begin() as conn:

        # to support SQLAlchemy DDL methods as well as legacy functions, the
        # AsyncConnection.run_sync() awaitable method will pass a "sync"
        # version of the AsyncConnection object to any synchronous method,
        # where synchronous IO calls will be transparently translated for
        # await.
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)

        # for normal statement execution, a traditional "await execute()"
        # pattern is used.
        await conn.execute(
            t1.insert(), [{"name": "1"}, {"name": "some name 2"}]
        )

        await conn.execute(
            question_sa.insert(), [{"question_text": "some name 1"}, {"question_text": "some name 2"}]
        )

    async with engine.connect() as conn:

        # the default result object is the
        # sqlalchemy.engine.Result object
        result = await conn.execute(t1.select().where(t1.c.name =='1'))
        #result = await conn.execute(sa.text("SHOW DATABASES;"))

        # the results are buffered so no await call is necessary
        # for this case.
        print('ppp: ' , result.fetchall())

        # for a streaming result that buffers only segments of the
        # result at time, the AsyncConnection.stream() method is used.
        # this returns a sqlalchemy.ext.asyncio.AsyncResult object.
        async_result = await conn.stream(t1.select())

        # this object supports async iteration and awaitable
        # versions of methods like .all(), fetchmany(), etc.
        async for row in async_result:
            print(row)        