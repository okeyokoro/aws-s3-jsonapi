from marshmallow_jsonapi import fields

from . import CamelCaseSchema as CCS


class S3BucketsSchema(CCS):
    class Meta:
        type_ = "s3-bucket"

    id = fields.Str()
    name = fields.Str()
    was_default = fields.Boolean()
    last_updated = fields.DateTime()

rds_entry_schema = S3BucketsSchema(many=True)
