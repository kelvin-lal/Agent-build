"""
Kelvin's Agent
"""

import psutil

class Metrics:
    def __init__(self):
        self.metrics = {}

    def cpuMetrics(self):
        
        metrics =  {}

        metrics['test.metric.cpu_usage'] = psutil.cpu_percent()
        metrics['test.metric.cpu_count'] = psutil.cpu_count()

        return metrics

    def memoryMetrics(self):

        metrics =  {}

        metrics['test.metric.memory_usage'] = psutil.virtual_memory().percent
        metrics['test.metric.memory_available'] = psutil.virtual_memory().free

        return metrics

    def diskMetrics(self):
        metrics =  {}

        metrics['test.metric.disk_usage'] = psutil.disk_usage('/').percent

        return metrics



