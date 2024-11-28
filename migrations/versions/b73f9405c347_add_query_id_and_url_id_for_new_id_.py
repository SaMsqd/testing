"""Add query_id and url_id, for new id column in query and url table

Revision ID: b73f9405c347
Revises: 5a94ef525b78
Create Date: 2024-10-07 12:57:33.292522

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = 'b73f9405c347'
down_revision = '5a94ef525b78'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    
    op.add_column('metrics', sa.Column('url_id', sa.Integer(), nullable=True))
    op.add_column('metrics_query', sa.Column('query_id', sa.Integer(), nullable=True))

    op.add_column('query', sa.Column('id', sa.Integer(), autoincrement=True, nullable=True, unique=True))
    op.add_column('url', sa.Column('id', sa.Integer(), autoincrement=True, nullable=True, unique=True))

    op.create_foreign_key(None, 'metrics', 'url', ['url_id'], ['id'])
    op.create_foreign_key(None, 'metrics_query', 'query', ['query_id'], ['id'])
    

    # Обновляем данные: заполняем id в query и url
    conn = op.get_bind()

    # Заполнение столбца id в таблице query
    conn.execute(
        text(
            """
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'query_id_seq') THEN 
                    CREATE SEQUENCE query_id_seq; 
                END IF;
            END $$;
            UPDATE query
            SET id = nextval('query_id_seq');
            """
        )
    )

    # Заполнение столбца id в таблице url
    conn.execute(
        text(
            """
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'url_id_seq') THEN 
                    CREATE SEQUENCE url_id_seq; 
                END IF;
            END $$;
            UPDATE url
            SET id = nextval('url_id_seq');
            """
        )
    )

    # Обновляем столбец url_id в таблице metrics
    conn.execute(
        text(
            """
            UPDATE metrics
            SET url_id = (SELECT id FROM url WHERE url.url = metrics.url);
            """
        )
    )

    # Обновляем столбец query_id в таблице metrics_query
    conn.execute(
        text(
            """
            UPDATE metrics_query
            SET query_id = (SELECT id FROM query WHERE query.query = metrics_query.query);
            """
        )
    )

    # Делаем столбцы id в query и url NOT NULL
    op.alter_column('query', 'id', nullable=False)
    op.alter_column('url', 'id', nullable=False)

    # После заполнения делаем столбцы NOT NULL
    op.alter_column('metrics', 'url_id', nullable=False)
    op.alter_column('metrics_query', 'query_id', nullable=False)
    
    # Удаляем старые столбцы url и query
    #op.drop_column('metrics', 'url')
    #op.drop_column('metrics_query', 'query')
    # ### end Alembic commands ###
def downgrade() -> None:

    print('downgrade')
    # Восстанавливаем удаленные столбцы
    #op.add_column('metrics', sa.Column('url', sa.String(), nullable=False))
    #op.add_column('metrics_query', sa.Column('query', sa.String(), nullable=False))

    # ### commands auto generated by Alembic - please adjust! ###
    #op.drop_column('url', 'id')
    #op.drop_column('query', 'id')
    #op.drop_constraint(None, 'metrics_query', type_='foreignkey')
    #op.drop_column('metrics_query', 'query_id')
    #op.drop_constraint(None, 'metrics', type_='foreignkey')
    #op.drop_column('metrics', 'url_id')
    # ### end Alembic commands ###
