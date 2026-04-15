"""
Kelvin's Agent
"""

import os
import time
from metrics.metrics import Metrics
from metrics.metricSubmission import metric_submission
from checks.checkRun import Check
from agent.config import config
from checks.customCheck import CustomCheck


agent_running = False


def agent():
    global agent_running
    os.environ["DD_API_KEY"] = config.get_DD_API_KEY()
    os.environ["DD_SITE"] = config.get_DD_SITE()
    
    print("Agent starting...")
    metrics = Metrics()
    custom_check = CustomCheck()
    
    while agent_running:
        cpu_metrics = metrics.cpuMetrics()
        for metric_name, metric_value in cpu_metrics.items():
            metric_submission(metric_name, metric_value)
            Check.metric_counts["cpu"] += 1
        
        memory_metrics = metrics.memoryMetrics()
        for metric_name, metric_value in memory_metrics.items():
            metric_submission(metric_name, metric_value)
            Check.metric_counts["memory"] += 1
        
        disk_metrics = metrics.diskMetrics()
        for metric_name, metric_value in disk_metrics.items():
            metric_submission(metric_name, metric_value)
            Check.metric_counts["disk"] += 1 
        
        custom_check.run()
        Check.metric_counts["custom"] += 1
        
        time.sleep(1)
    
    print("Agent stopped.")

