from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ec2 as ec2,
)
from constructs import Construct
import os

DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')

class MyDjangoCdkProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, ecr_repository, monitoring_resources, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "MyDjangoVPC", max_azs=2)
        cluster = ecs.Cluster(self, "MyDjangoCluster", vpc=vpc)

        # Django application
        django_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "DjangoService",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_ecr_repository(ecr_repository),
                container_port=8000,
                )
            )

        # Celery worker
        celery_task = ecs.FargateTaskDefinition(
            self, "CeleryWorkerTask",
            cpu=256,
            memory_limit_mib=512,
        )
        celery_task.add_container(
            "CeleryWorkerContainer",
            image=ecs.ContainerImage.from_ecr_repository(ecr_repository),
        )

        ecs.FargateService(
            self, "CeleryWorkerService",
            cluster=cluster,
            task_definition=celery_task,
            desired_count=1,
        )
