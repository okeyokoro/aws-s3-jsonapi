from abc import ABC


class AbstractResource(ABC):

    cdk_construct = None

    def __init__(self, stack_obj, stack_id,):
        self.stack_obj = stack_obj
        self.stack_id = stack_id
        self.cdk_resource = None

