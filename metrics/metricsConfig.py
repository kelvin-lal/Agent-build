"""
Kelvin's Agent
"""

from agent.settings import settings


class MetricsConfig:
    COLLECTION_INTERVAL = 1.0

    def __init__(self):
        saved = settings.load()
        self.submission_interval = saved.get("submission_interval", 1.0)

    def get_collection_interval(self):
        return self.COLLECTION_INTERVAL

    def get_submission_interval(self):
        return self.submission_interval

    def set_submission_interval(self, interval):
        self.submission_interval = max(interval, self.COLLECTION_INTERVAL)
        self._persist()

    def _persist(self):
        data = settings.load()
        data["submission_interval"] = self.submission_interval
        settings.save(data)

metrics_config = MetricsConfig()
