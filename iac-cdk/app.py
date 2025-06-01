#!/usr/bin/env python3

import aws_cdk as cdk
from backend.backend_stack import BackendStack
from frontend.frontend_acm_stack import FrontendAcmStack
from frontend.frontend_stack import FrontendStack

app = cdk.App()

BackendStack(
    app,
    "BackendStack",
    env=cdk.Environment(account="646082475080", region="eu-west-1"),
)
frontend_acm_stack = FrontendAcmStack(
    app,
    "FrontendAcmStack",
    domain_name="antoinedelia.fr",
    subdomain="spotify-cover",
    env=cdk.Environment(account="646082475080", region="us-east-1"),
    cross_region_references=True,
)
FrontendStack(
    app,
    "FrontendStack",
    domain_name="antoinedelia.fr",
    subdomain="spotify-cover",
    certificate=frontend_acm_stack.certificate,
    env=cdk.Environment(account="646082475080", region="eu-west-1"),
    cross_region_references=True,
)

app.synth()
