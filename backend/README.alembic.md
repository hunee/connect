#
# DB 마이그레이션 도구
#
$ mysql -u root -p P9 < P9_2014-02-20.sql 


$ pip3 install alembic

# 로컬 프로젝트를 생성
$ alembic init migrations

$ vi alembic.ini
script_location = ./app/db/migrations

sqlalchemy.url = sqlite:///db_file.db
sqlalchemy.url = postgresql://username:password@127.0.0.1:5432


# 새로운 revision을 생성
$ alembic revision -m "0"

# 테이블과 컬럼들 생성
$ alembic upgrade head


# 두번째 revision 파일 생성
$ alembic revision -m "1"

def upgrade():
    op.add_column('customer', sa.Column('middlename', sa.String(50)))

def downgrade():
    #sqlite
    with op.batch_alter_table('customer') as batch_op:
        batch_op.drop_column('middlename')

    #mysql
    op.drop_column('customer', 'middlename')

# migration 진행
$ alembic upgrade head

# migration 기록(history)
$ alembic history

# downgrade
$ alembic downgrade -1 
$ alembic downgrade <down_revision>
