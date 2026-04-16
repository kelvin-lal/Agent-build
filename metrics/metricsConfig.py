"""
Kelvin's Agent
"""


class MetricsConfig:
    COLLECTION_INTERVAL = 1.0

    def __init__(self):
        self.submission_interval = 1.0

    def get_collection_interval(self):
        return self.COLLECTION_INTERVAL

    def get_submission_interval(self):
        return self.submission_interval

    def set_submission_interval(self, interval):
        self.submission_interval = max(interval, self.COLLECTION_INTERVAL)

metrics_config = MetricsConfig()
