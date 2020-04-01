from usecases import get_records_from_rds
from schemas.rds_db import rds_entry_schema


def main(event, context):
    db_entries = get_records_from_rds()
    return rds_entry_schema.dump(db_entries)
