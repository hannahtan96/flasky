"""empty message

Revision ID: cba8fad5691e
Revises: 480776d4cd74
Create Date: 2022-11-10 19:29:19.886708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cba8fad5691e'
down_revision = '480776d4cd74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('restaurant', sa.String(), nullable=True),
    sa.Column('meal', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('breakfast', sa.Column('menu_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'breakfast', 'menu', ['menu_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'breakfast', type_='foreignkey')
    op.drop_column('breakfast', 'menu_id')
    op.drop_table('menu')
    # ### end Alembic commands ###
