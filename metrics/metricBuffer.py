"""
Kelvin's Agent - In-memory metric buffer

Inspired by the Datadog agent's TimeSampler.metricsByTimestamp pattern:
metrics are collected into a buffer and flushed (drained) on a separate
submission interval.
"""
import threading
from datetime import datetime
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_resource import MetricResource
from datadog_api_client.v2.model.metric_series import MetricSeries


class MetricBuffer:
    def __init__(self):
        self._buffer = []
        self._lock = threading.Lock()

    def add(self, metric_name, metric_value):
        series = MetricSeries(
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
        )
        with self._lock:
            self._buffer.append(series)

    def flush(self):
        with self._lock:
            flushed = self._buffer
            self._buffer = []
        return flushed

    def is_empty(self):
        with self._lock:
            return len(self._buffer) == 0
