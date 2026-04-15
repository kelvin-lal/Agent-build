"""
Metric Submission - Handles sending metrics to Datadog
"""
from datetime import datetime
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_resource import MetricResource
from datadog_api_client.v2.model.metric_series import MetricSeries


def metric_submission(metric_name, metric_value):
  try:
    body = MetricPayload(
        series=[
            MetricSeries(
                metric=metric_name,
                type=MetricIntakeType.UNSPECIFIED,
                points=[
                    MetricPoint(
                        timestamp=int(datetime.now().timestamp()),
                        value=metric_value,
                    ),
                ],
                resources=[
                    MetricResource(
                        name="dummyhost",
                        type="host",
                    ),
                ],
            ),
        ],
    )

    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        response = api_instance.submit_metrics(body=body)
  except Exception as e:
    raise Exception(f"Failed to submit metric '{metric_name}': {e}")