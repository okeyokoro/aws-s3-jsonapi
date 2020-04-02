from aws_cdk import aws_ec2

from abcs import AbstractResource


class VPC(AbstractResource):
    cdk_construct = aws_ec2.Vpc

    def __init__(self, stack_obj, stack_id,
                 subnet_config_builder,
                 max_number_of_availability_zones=2,
                ):
        super().__init__(stack_obj, stack_id)

        self.cdk_resource = self.cdk_construct(
            stack_obj,
            f"{stack_id}-vpc",
            max_azs=max_number_of_availability_zones,
            cidr="10.10.0.0/16",
            subnet_configuration=subnet_config_builder.subnet_configs,
            nat_gateways=subnet_config_builder.nat_gateways,
        )


class SubnetConfigBuilder():

    cdk_construct = aws_ec2.SubnetConfiguration

    SUBNET_TYPE = {
        "public" : aws_ec2.SubnetType.PUBLIC,
        "private" : aws_ec2.SubnetType.PRIVATE,
        "isolated" : aws_ec2.SubnetType.ISOLATED
    }

    def __init__(self):
        self.subnet_configs = []
        self.nat_gateways = 0 # we add a NAT gateway for every non-public subnet

    def make_public(self, name):
        public_subnet_config = self.cdk_construct(
            name=f"{name}-public",
            subnet_type=self.SUBNET_TYPE["public"],
            cidr_mask=24,
        )

        self.subnet_configs.append(
            public_subnet_config
        )

    def _make_non_public(self, name, subnet_type_key):
        non_public_subnet_config = self.cdk_construct(
            name=f"{name}-{subnet_type_key}",
            subnet_type=self.SUBNET_TYPE[subnet_type_key],
            cidr_mask=24,
        )

        self.subnet_configs.append(
            non_public_subnet_config
        )

        self.nat_gateways += 1

    def make_private(self, name):
        self._make_non_public(name, "private")

    def make_isolated(self, name):
        self._make_non_public(name, "isolated")
