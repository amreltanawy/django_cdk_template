from aws_cdk import (
    Stack,
    aws_ecr as ecr,
    aws_ecr_assets as ecr_assets,
    RemovalPolicy,
)
from constructs import Construct

class ECRStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.django_repo = ecr.Repository.from_repository_name(self, "DjangoRepo", "carvinu/django/app")
