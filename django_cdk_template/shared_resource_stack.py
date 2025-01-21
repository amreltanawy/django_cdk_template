import json
from aws_cdk import (
    Stack,
    aws_secretsmanager as secretsmanager,
)

from constructs import Construct
class SharedResourcesStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create DB credentials that can be used by both RDS and application
        self.db_credentials = secretsmanager.Secret(self, "DBCredentials",
        generate_secret_string=secretsmanager.SecretStringGenerator(
            secret_string_template=json.dumps({"username":"django"}),
            generate_string_key="password",
            exclude_characters="/@\"'\\",
            password_length=30,
            exclude_punctuation=True
        )
)
