from aws_cdk import CfnOutput, RemovalPolicy, Stack
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from constructs import Construct


class FrontendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, domain_name: str, subdomain: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        full_domain = f"{subdomain}.{domain_name}"

        # Get the existing hosted zone
        zone = route53.HostedZone.from_lookup(self, "HostedZone", domain_name=domain_name)

        # Certificate in us-east-1 (required for CloudFront)
        certificate = acm.DnsValidatedCertificate(
            self, "SiteCertificate", domain_name=full_domain, hosted_zone=zone, region="us-east-1"
        )

        # S3 Bucket (private)
        bucket = s3.Bucket(
            self,
            "FrontendBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            website_index_document="index.html",
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )

        # CloudFront Distribution
        distribution = cloudfront.Distribution(
            self,
            "FrontendDistribution",
            default_root_object="index.html",
            certificate=certificate,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin(bucket), viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
        )

        # Deploy files to S3
        s3deploy.BucketDeployment(
            self,
            "DeployFrontend",
            sources=[s3deploy.Source.asset("../web")],
            destination_bucket=bucket,
            distribution=distribution,
            distribution_paths=["/*"],  # Invalidate CloudFront cache
        )

        # Route53 Alias A Record
        route53.ARecord(
            self,
            "FrontendAliasRecord",
            zone=zone,
            record_name=subdomain,
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)),
        )

        # Output the URL
        CfnOutput(self, "WebsiteURL", value=f"https://{full_domain}", export_name="MyFrontendURL")
