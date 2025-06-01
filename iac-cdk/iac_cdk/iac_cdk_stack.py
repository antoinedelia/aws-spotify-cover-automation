from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_python_alpha as lambda_python
from constructs import Construct


class IacCdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        get_playlists_function = lambda_python.PythonFunction(
            self,
            "GetPlaylistsFunction",
            entry="../src/handlers",
            runtime=_lambda.Runtime.PYTHON_3_13,
            index="get_playlists.py",
            handler="lambda_handler",
            bundling=lambda_python.BundlingOptions(
                build_args={
                    "PIP_INDEX_URL": "https://your.index.url/simple/",
                }
            ),
        )

        api = apigateway.LambdaRestApi(
            self,
            "SpotifyCoverAutomationAPI",
            handler=get_playlists_function,
            proxy=False,
        )

        playlists_resource = api.root.add_resource("playlists")
        playlists_resource.add_method("GET")
