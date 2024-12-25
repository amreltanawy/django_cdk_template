from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ec2 as ec2,
)
from constructs import Construct

class MyDjangoCdkProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, ecr_repositories, rds_instance, monitoring_resources, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "MyVPC", max_azs=2)
        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc)

        # Django application
        django_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "DjangoService",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_ecr_repository(ecr_repositories['django']),
                container_port=8000,
                environment={
                    'DATABASE_URL': f"postgresql://{rds_instance.instance_endpoint.hostname}:{rds_instance.instance_endpoint.port}/mydb",
                    'MONITORING_URL': monitoring_resources['monitoring_url']
                }
            ),
        )

        # Celery worker
        celery_task = ecs.FargateTaskDefinition(
            self, "CeleryWorkerTask",
            cpu=256,
            memory_limit_mib=512,
        )
        celery_task.add_container(
            "CeleryWorkerContainer",
            image=ecs.ContainerImage.from_ecr_repository(ecr_repositories['celery']),
            environment={
                'DATABASE_URL': f"postgresql://{rds_instance.instance_endpoint.hostname}:{rds_instance.instance_endpoint.port}/mydb",
                'MONITORING_URL': monitoring_resources['monitoring_url']
            }
        )

        ecs.FargateService(
            self, "CeleryWorkerService",
            cluster=cluster,
            task_definition=celery_task,
            desired_count=1,
        )
