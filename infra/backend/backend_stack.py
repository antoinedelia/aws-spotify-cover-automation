from aws_cdk import Duration, Stack
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_python_alpha as lambda_python
from constructs import Construct


class BackendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        get_playlists_function = lambda_python.PythonFunction(
            self,
            "GetPlaylistsFunction",
            entry="../src",
            runtime=_lambda.Runtime.PYTHON_3_13,
            index="handlers/get_playlists.py",
            handler="lambda_handler",
            timeout=Duration.seconds(29),
        )

        generate_cover_function = lambda_python.PythonFunction(
            self,
            "GenerateCoverFunction",
            entry="../src",
            runtime=_lambda.Runtime.PYTHON_3_13,
            index="handlers/main.py",
            handler="lambda_handler",
            timeout=Duration.seconds(29),
        )

        headers = [h for h in apigw.Cors.DEFAULT_HEADERS]
        headers.append("X-Spotify-Token")

        api = apigw.RestApi(
            self,
            "SpotifyCoverAutomationAPI",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=headers,
            ),
        )

        playlists_resource = api.root.add_resource("playlists")
        playlists_resource.add_method("GET", apigw.LambdaIntegration(get_playlists_function))

        generate_cover_resource = api.root.add_resource("cover")
        generate_cover_resource.add_method("POST", apigw.LambdaIntegration(generate_cover_function))
