#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import (
    aws_secretsmanager as secretsmanager,
)
from django_cdk_template.django_cdk_template_stack import MyDjangoCdkProjectStack
from django_cdk_template.rds_stack import RDSStack
from django_cdk_template.ecr_stack import ECRStack
from django_cdk_template.monitoring_stack import MonitoringStack
from django_cdk_template.shared_resource_stack import SharedResourcesStack
app = cdk.App()

ecr_stack = ECRStack(app, "ECRStack")
rds_stack = RDSStack(app, "RDSStack")
monitoring_stack = MonitoringStack(app, "MonitoringStack")
MyDjangoCdkProjectStack(app, "MyDjangoCdkProjectStack",
    ecr_repository=ecr_stack.django_repo,
    monitoring_resources=monitoring_stack.resources,
)

app.synth()
