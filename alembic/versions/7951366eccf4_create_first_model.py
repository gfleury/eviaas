"""create first model

Revision ID: 7951366eccf4
Revises: 
Create Date: 2018-03-28 16:35:39.581892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7951366eccf4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'plan',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.String(250), nullable=False)
    )
    op.create_table(
        'env',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('key', sa.String(250), nullable=False, unique=True),
        sa.Column('value', sa.Binary(500), nullable=False),
        sa.Column('plan_id', sa.Integer, sa.ForeignKey('plan.id'), nullable=False)
    )
    op.create_table(
        'instance',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('team', sa.String(50), nullable=False),
        sa.Column('user', sa.String(50), nullable=False),
        sa.Column('plan_id', sa.Integer, sa.ForeignKey('plan.id'), nullable=False)
    )

def downgrade():
    op.drop_table('plan')
    op.drop_tables('env')
    op.drop_tables('instance')
