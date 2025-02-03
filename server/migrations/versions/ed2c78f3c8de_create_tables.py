"""create tables

Revision ID: ed2c78f3c8de
Revises: 
Create Date: 2025-02-03 10:27:53.241607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed2c78f3c8de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dealers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('dealer_id', sa.Integer(), nullable=False),
    sa.Column('picture_url', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['dealer_id'], ['dealers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('car_features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.Column('feature_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['feature_id'], ['features.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('car_features')
    op.drop_table('cars')
    op.drop_table('features')
    op.drop_table('dealers')
    # ### end Alembic commands ###
