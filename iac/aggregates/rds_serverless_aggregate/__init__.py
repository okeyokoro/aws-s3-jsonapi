import os
from resources import AuroraServerless


class RdsServerlessAggregate:
    def __init__(self, stack, id, vpc, security_group) -> None:
        self.aurora = AuroraServerless(
            stack, id, vpc,
            subnet_type="private",
            peer_security_groups=[security_group]
        )
