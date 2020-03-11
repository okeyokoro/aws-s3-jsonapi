from aws_cdk import (
    aws_ec2,
    aws_rds,
    core,
)

from abcs import AbstractResource

from utils import get_subnet_type


def get_engine(name:str):
    ENGINE_TYPES = {
        "mysql": aws_rds.DatabaseInstanceEngine.MYSQL,
        "postgres": None,
    }
    return ENGINE_TYPES[name]



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
                 engine_version="8.0.16",
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
            engine_version=engine_version,
            deletion_protection=False,
            removal_policy=core.RemovalPolicy.DESTROY,
            instance_class=aws_ec2.InstanceType.of(
                aws_ec2.InstanceClass.MEMORY4,
                aws_ec2.InstanceSize.LARGE
            ),
        )


class RDSCluster(AbstractResource):
    cdk_construct = aws_rds.DatabaseInstance

    def __init__(self, stack_obj, stack_id):
        # Ceate Aurora Cluster with 2 instances with CDK High Level API
        # Secrets Manager auto generate and keep the password, don't put password in cdk code directly
        self.cdk_resource = None


class AuroraServerless(AbstractResource):
    cdk_construct = aws_rds.DatabaseCluster

    def __init__(self, stack_obj, stack_id,
                 vpc,
                 subnet_type,
                 db_name=None,
                 username="admin",
                 engine_type="mysql",
                 engine_version="8.0.16",
                ):
        super().__init__(stack_obj, stack_id)

        """ Secrets Manager will auto generate and keep the password,
        don't put password in cdk code directly"""

        self.cdk_resource = self.cdk_construct(
            stack_obj,
            f"{stack_id}-aurora",

            default_database_name=f"{stack_id}-db",

            engine=aws_rds.DatabaseClusterEngine.AURORA_MYSQL,
            engine_version="5.7.12",

            master_user=aws_rds.Login(username=username),

            instance_props=aws_rds.InstanceProps(
                vpc=vpc,
                vpc_subnets=aws_ec2.SubnetSelection(
                    subnet_type=get_subnet_type(subnet_type)
                ),
                instance_type=aws_ec2.InstanceType(instance_type_identifier="t2.small")
            ),
            instances=2,

            parameter_group=aws_rds.ClusterParameterGroup.from_parameter_group_name(
                stack_obj,
                f"{stack_id}-aurora-parameter-group",
                parameter_group_name="default.aurora-mysql5.7"
            ),
        )

        # for asg_sg in asg_security_groups:
        #     self.cdk_resource.connections.allow_default_port_from(
        #         asg_sg,
        #         "EC2 Autoscaling Group access Aurora"
        #     )
