"""
Kelvin's Agent
"""


class MetricsConfig:
    def __init__(self):
        self.submission_interval = 1.0

    def get_submission_interval(self):
        return self.submission_interval

    def set_submission_interval(self, interval):
        self.submission_interval = interval

metrics_config = MetricsConfig()
