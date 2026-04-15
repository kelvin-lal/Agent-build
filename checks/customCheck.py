"""
Kelvin's Agent
"""
from metrics.metricSubmission import metric_submission


class CustomCheck:
    def gauge(self, metric_name, value):
        try:
            metric_submission(metric_name, value)
        except Exception as e:
            raise Exception(f"Custom check gauge failed for '{metric_name}': {e}")

    def run(self):
        self.gauge('custom.check.metric', 1)
