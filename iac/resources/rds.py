from aws_cdk import (
    aws_ec2,
    aws_rds,
    core,
)

from abcs import AbstractResource

from utils import get_subnet_type

"""
NOTE: database names can only contain alphanumeric characters
i.e. no '-'

NOTE: 'database_name' cannot be 'db'

NOTE: 'master_user' cannot be 'admin'

NOTE: the lowest instance type you can use for aurora is 't2.medium'
"""

class AuroraServerless(AbstractResource):
    cdk_construct = aws_rds.DatabaseCluster

    PORTS = {
        "mysql": 3306,
        "postgres": 5432
    }

    ENGINE_TYPES = {
        "mysql": aws_rds.DatabaseClusterEngine.AURORA_MYSQL,
        "postgres": aws_rds.DatabaseClusterEngine.AURORA_POSTGRESQL,
    }

    def __init__(self, stack_obj, stack_id,
                 vpc,
                 subnet_type,
                 peer_security_groups=None,
                 db_name="s3jsonapi", # TODO: replace with env variables
                 username="s3jsonapi", # TODO: replace with env variables
                 password="s3jsonapi", # TODO: replace with env variables
                 engine_type="postgres",
                 engine_version=None,
                ):
        super().__init__(stack_obj, stack_id)

        if not peer_security_groups:
            peer_security_groups = []

        self.cdk_resource = self.cdk_construct(
            stack_obj,
            f"{stack_id}-aurora",

            default_database_name=db_name,

            master_user=aws_rds.Login(username=username,
                                      password=core.SecretValue.plain_text(password)
                                    ),

            engine_version="11.6",
            port=self.PORTS[engine_type],
            engine=self.ENGINE_TYPES[engine_type],
            # https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Updates.20180305.html

            instances=2,
            instance_props=aws_rds.InstanceProps(
                vpc=vpc,
                vpc_subnets=aws_ec2.SubnetSelection(
                    subnet_type=get_subnet_type(subnet_type)
                ),
                instance_type=aws_ec2.InstanceType(instance_type_identifier="t3.medium")
                # https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html
                # https://github.com/aws/aws-cdk/issues/5126
            ),

            parameter_group=aws_rds.ClusterParameterGroup.from_parameter_group_name(
                stack_obj,
                f"{stack_id}-aurora-parameter-group",
                parameter_group_name="default.aurora-postgresql11"
            ),

            removal_policy=core.RemovalPolicy.DESTROY,
        )

        for sg in peer_security_groups:
            self.cdk_resource.connections.allow_default_port_from(sg)


class RDS(AbstractResource):
    cdk_construct = aws_rds.DatabaseInstance

    ENGINE_TYPES = {
        "mysql": aws_rds.DatabaseInstanceEngine.MYSQL,
    }

    def __init__(self, stack_obj, stack_id,
                 vpc,
                 db_name: str,
                 password: str,
                 username="admin",
                 engine_type="mysql",
                 engine_version=None,
                ):
        super().__init__(stack_obj, stack_id)

        self.cdk_resource = self.cdk_construct(
            stack_obj,
            f"{stack_id}-rds",

            vpc=vpc,

            database_name=db_name,
            master_user_password=core.SecretValue.plain_text(password),
            master_username=username,

            engine=self.ENGINE_TYPES[engine_type],

            port=3306,
            # engine_version=engine_version,
            deletion_protection=False,
            removal_policy=core.RemovalPolicy.DESTROY,
            instance_class=aws_ec2.InstanceType.of(
                aws_ec2.InstanceClass.MEMORY4,
                aws_ec2.InstanceSize.LARGE
            ),
        )

"""
class DatabaseCluster(
    scope: aws_cdk.core.Construct,
    id: str,
    engine: "DatabaseClusterEngine",
    instance_props: "InstanceProps",
    master_user: "Login",
    backup: typing.Optional["BackupProps"]=None,
    cluster_identifier: typing.Optional[str]=None,
    default_database_name: typing.Optional[str]=None,
    engine_version: typing.Optional[str]=None, 
    instance_identifier_base: typing.Optional[str]=None, 
    instances: typing.Optional[jsii.Number]=None, 
    kms_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, 
    monitoring_interval: typing.Optional[aws_cdk.core.Duration]=None, 
    monitoring_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, 
    parameter_group: typing.Optional["IParameterGroup"]=None, 
    port: typing.Optional[jsii.Number]=None, 
    preferred_maintenance_window: typing.Optional[str]=None, 
    removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None, 
    storage_encrypted: typing.Optional[bool]=None
)
"""