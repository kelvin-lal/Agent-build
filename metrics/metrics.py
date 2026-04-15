"""
Kelvin's Agent
"""

import psutil

class Metrics:
    def __init__(self):
        self.metrics = {}

    def cpuMetrics(self):
        metrics = {}
        try:
            metrics['test.metric.cpu_usage'] = psutil.cpu_percent()
            metrics['test.metric.cpu_count'] = psutil.cpu_count()
        except Exception as e:
            print(f"[ERROR] Failed to collect CPU metrics: {e}")
        return metrics

    def memoryMetrics(self):
        metrics = {}
        try:
            metrics['test.metric.memory_usage'] = psutil.virtual_memory().percent
            metrics['test.metric.memory_available'] = psutil.virtual_memory().free
        except Exception as e:
            print(f"[ERROR] Failed to collect memory metrics: {e}")
        return metrics

    def diskMetrics(self):
        metrics = {}
        try:
            metrics['test.metric.disk_usage'] = psutil.disk_usage('/').percent
        except Exception as e:
            print(f"[ERROR] Failed to collect disk metrics: {e}")
        return metrics



