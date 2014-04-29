"""alter db

Revision ID: 12c18b2f59ac
Revises: a921de174d7
Create Date: 2014-04-28 23:46:39.165577

"""

# revision identifiers, used by Alembic.
revision = '12c18b2f59ac'
down_revision = 'a921de174d7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('touroperator_bank_detail',
    sa.Column('touroperator_id', sa.Integer(), nullable=False),
    sa.Column('bank_detail_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bank_detail_id'], ['bank_detail.id'], onupdate='cascade', ondelete='cascade'),
    sa.ForeignKeyConstraint(['touroperator_id'], ['touroperator.id'], onupdate='cascade', ondelete='cascade'),
    sa.PrimaryKeyConstraint('touroperator_id', 'bank_detail_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('touroperator_bank_detail')
    ### end Alembic commands ###