from aws_cdk import (
    Stack,
    aws_ecr as ecr,
    RemovalPolicy,
)
from constructs import Construct

class ECRStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.repositories = {}
        
        for repo_name in ['django', 'celery']:
            repository = ecr.Repository(
                self, f"{repo_name.capitalize()}Repo",
                repository_name=f"{repo_name}-app",
                removal_policy=RemovalPolicy.DESTROY,
            )
            self.repositories[repo_name] = repository
