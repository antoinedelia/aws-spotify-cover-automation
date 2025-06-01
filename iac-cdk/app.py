#!/usr/bin/env python3

import aws_cdk as cdk
from iac_cdk.iac_cdk_stack import IacCdkStack

app = cdk.App()
IacCdkStack(
    app,
    "IacCdkStack",
    env=cdk.Environment(account="646082475080", region="eu-west-1"),
)

app.synth()
