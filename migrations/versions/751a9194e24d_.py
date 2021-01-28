"""empty message

Revision ID: 751a9194e24d
Revises: 844994c1bcf8
Create Date: 2021-01-23 20:43:12.628847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '751a9194e24d'
down_revision = '844994c1bcf8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    roles_table = op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    op.bulk_insert(roles_table,
                   [
                       {'name': 'admin'},
                       {'name': 'weirdo'}
                   ])

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('group', sa.INTEGER(), nullable=True))
    op.drop_table('user_roles')
    op.drop_table('roles')
    # ### end Alembic commands ###