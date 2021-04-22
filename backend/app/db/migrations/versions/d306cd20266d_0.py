"""0

Revision ID: d306cd20266d
Revises: 
Create Date: 2021-04-18 04:58:37.731634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd306cd20266d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.drop_table('계정_정보')
    except Exception as e:
        pass

    ###
    op.create_table(
        '계정_정보',
        sa.Column('id', sa.Integer, autoincrement=True, primary_key=True, comment='사용자_계정정보'),
        sa.Column('uuid', sa.String(255), nullable=False),
        sa.Column('사용자', sa.String(255), nullable=False),
        sa.Column('비밀번호', sa.String(255), nullable=False),
        sa.Column('마켓', sa.String(255), nullable=False),
        sa.Column('단말기', sa.String(255), nullable=False),
        sa.Column('운영체제', sa.String(255), nullable=False),
        sa.Column('운영체제_버전', sa.String(255), nullable=False),
        sa.Column('푸시_token', sa.String(255), nullable=False),
        sa.Column('비밀번호_찾기_재시도시간', sa.String(255), nullable=False),

        # Indexes #
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid', name='uniq_registry0uuid'),

        mysql_engine='InnoDB',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_charset='utf8mb4',
        #mysql_partitions="16",
        #mysql_partition_by="LINEAR HASH(id)",
    )    

    try:
        op.drop_table('계정_생성_정보')
    except Exception as e:
        pass

    ###
    op.create_table(
        '계정_생성_정보',
        sa.Column('id', sa.Integer, autoincrement=True, primary_key=True, comment='사용자_계정정보'),
        sa.Column('날짜', sa.DateTime, server_default=sa.func.now()),
        sa.Column('마켓', sa.String(255), nullable=False),
        sa.Column('단말기', sa.String(255), nullable=False),
        sa.Column('운영체제', sa.String(255), nullable=False),
        sa.Column('운영체제_버전', sa.String(255), nullable=False),
        sa.Column('fk_계정_정보_id', sa.Integer),

        # Indexes #
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['fk_계정_정보_id'], ['계정_정보.id'], name='fk_계정_정보_id'),

        mysql_engine='InnoDB',
        mysql_collate='utf8mb4_unicode_ci',
        mysql_charset='utf8mb4',
        #mysql_partitions="16",
        #mysql_partition_by="LINEAR HASH(id)",

    )    

def downgrade():
    pass
