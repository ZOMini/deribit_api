import runpy
import sys

from sqlalchemy import create_engine

from core.config import settings


def migrate():
    engine = create_engine(settings.data_base_sync)
    if not engine.dialect.has_table(engine.connect(), 'currencies'):
        sys.argv = ['', 'upgrade', 'head']
        runpy.run_module('alembic', run_name='__main__')
