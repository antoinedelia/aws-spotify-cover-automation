#!/usr/bin/env python3

import aws_cdk as cdk
from backend.backend_stack import BackendStack
from frontend.frontend_stack import FrontendStack

app = cdk.App()

BackendStack(app, "BackendStack", env=cdk.Environment(account="646082475080", region="eu-west-1"))
FrontendStack(
    app,
    "FrontendStack",
    domain_name="antoinedelia.fr",
    subdomain="spotify-cover",
    env=cdk.Environment(account="646082475080", region="eu-west-1"),
)

app.synth()
