#!/usr/bin/env python3

import aws_cdk as cdk
from backend.backend_stack import BackendStack

app = cdk.App()
BackendStack(
    app,
    "BackendStack",
    env=cdk.Environment(account="646082475080", region="eu-west-1"),
)

app.synth()
