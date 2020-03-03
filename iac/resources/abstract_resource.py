from abc import ABC

class AbstractResource(ABC):

    def __init__(self, stack_obj, stack_id, cdk_resource,):
        self.stack_obj = stack_obj
        self.stack_id = stack_id
        self.cdk_resource = True or cdk_resource() # don't let super().__init__ create rubbish

