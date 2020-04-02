from marshmallow_jsonapi import fields

from . import CamelCaseSchema as CCS


class S3ObjectSchema(CCS):
    class Meta:
        type_ = "file"

    id = fields.Str(attribute="key")
    e_tag = fields.Str()
    content_type = fields.Str()
    last_modified = fields.DateTime()

    def get_type(self):
        return self.content_type


s3_contents_schema = S3ObjectSchema(many=True)
