from marshmallow_jsonapi import fields

from . import CamelCaseSchema


class S3ObjectSummarySchema(CamelCaseSchema):
    """ - https://jsonapi.org/
        - https://github.com/marshmallow-code/marshmallow-jsonapi
        - https://marshmallow.readthedocs.io/en/latest/api_reference.html#module-marshmallow.fields
    """
    class Meta:
        type_ = "s3-buckets"

    id = fields.Str(attribute="key")
    e_tag = fields.Str()
    last_modified = fields.DateTime()
    owner = fields.Dict(keys=fields.Str(), values=fields.Str())
    size = fields.Int()
    storage_class = fields.Str()


class S3ObjectSchema(CamelCaseSchema):
    class Meta:
        type_ = "file"

    id = fields.Str(attribute="key")
    e_tag = fields.Str()
    content_type = fields.Str()
    last_modified = fields.DateTime()

    def get_type(self):
        return self.content_type


s3_contents_schema = S3ObjectSchema(many=True)
