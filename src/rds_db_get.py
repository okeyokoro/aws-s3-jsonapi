from usecases import get_records_from_rds
from schemas.rds_db import rds_entry_schema

from . import session


def main(event, context):
    db_entries = get_records_from_rds(session)
    return rds_entry_schema.dump(db_entries)
