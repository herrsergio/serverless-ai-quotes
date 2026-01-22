from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_ssm as ssm,
    aws_events as events,
    aws_events_targets as targets,
    aws_logs as logs,
    Duration,
    RemovalPolicy,
)
from constructs import Construct

class GenAIQuotes(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Ask OpenAI API to generate a quote
        self.gen_quote_function = _lambda.DockerImageFunction(
            self, "GenQuoteFunction",
            code=_lambda.DockerImageCode.from_image_asset(
                "../gen-quote-function",
                cmd=["lambda_genaiquote.handler"]
            ),
            timeout=Duration.minutes(1),
            memory_size=512,
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        # Manually create policy statement for SSM
        # Using already stored params from publishfeed
        from aws_cdk import aws_iam as iam
        ssm_policy = iam.PolicyStatement(
            actions=["ssm:GetParameter", "ssm:GetParameters"],
            resources=[
                "arn:aws:ssm:*:*:parameter/rss-feed/*",
                "arn:aws:ssm:*:*:parameter/serverless-ai-quotes/*"
            ]
        )
        self.gen_quote_function.add_to_role_policy(ssm_policy)


        # Scheduler
        # 1. Fetch Daily
        rule_fetch = events.Rule(
            self, "RuleGenQuoteDaily",
            schedule=events.Schedule.rate(Duration.days(1))
        )
        rule_fetch.add_target(targets.LambdaFunction(self.gen_quote_function))

