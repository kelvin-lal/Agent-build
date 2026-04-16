"""
Kelvin's Agent
"""

import os
import time
from metrics.metrics import Metrics
from metrics.metricSubmission import metric_submission
from metrics.metricsConfig import metrics_config
from checks.checkRun import Check
from agent.config import config
from checks.customCheck import CustomCheck


agent_running = False
agent_error_count = 0
agent_last_error = None
MAX_ERRORS = 10


def agent():
    global agent_running, agent_error_count, agent_last_error
    agent_error_count = 0
    agent_last_error = None
    try:
        os.environ["DD_API_KEY"] = config.get_DD_API_KEY()
        os.environ["DD_SITE"] = config.get_DD_SITE()
    except Exception as e:
        print(f"[ERROR] Failed to set environment variables: {e}")
        agent_running = False
        return

    print("Agent starting...")
    try:
        metrics = Metrics()
        custom_check = CustomCheck()
    except Exception as e:
        print(f"[ERROR] Failed to initialize collectors: {e}")
        agent_running = False
        return
    
    while agent_running:
        try:
            cpu_metrics = metrics.cpuMetrics()
            for metric_name, metric_value in cpu_metrics.items():
                metric_submission(metric_name, metric_value)
                Check.metric_counts["cpu"] += 1
        except Exception as e:
            agent_error_count += 1
            agent_last_error = f"CPU metric collection failed: {e}"
            print(f"[ERROR] ({agent_error_count}/{MAX_ERRORS}) {agent_last_error}")
            if agent_error_count >= MAX_ERRORS: break

        try:
            memory_metrics = metrics.memoryMetrics()
            for metric_name, metric_value in memory_metrics.items():
                metric_submission(metric_name, metric_value)
                Check.metric_counts["memory"] += 1
        except Exception as e:
            agent_error_count += 1
            agent_last_error = f"Memory metric collection failed: {e}"
            print(f"[ERROR] ({agent_error_count}/{MAX_ERRORS}) {agent_last_error}")
            if agent_error_count >= MAX_ERRORS: break

        try:
            disk_metrics = metrics.diskMetrics()
            for metric_name, metric_value in disk_metrics.items():
                metric_submission(metric_name, metric_value)
                Check.metric_counts["disk"] += 1 
        except Exception as e:
            agent_error_count += 1
            agent_last_error = f"Disk metric collection failed: {e}"
            print(f"[ERROR] ({agent_error_count}/{MAX_ERRORS}) {agent_last_error}")
            if agent_error_count >= MAX_ERRORS: break

        try:
            custom_check.run()
            Check.metric_counts["custom"] += 1
        except Exception as e:
            agent_error_count += 1
            agent_last_error = f"Custom check failed: {e}"
            print(f"[ERROR] ({agent_error_count}/{MAX_ERRORS}) {agent_last_error}")

        if agent_error_count >= MAX_ERRORS:
            break
        
        time.sleep(metrics_config.get_submission_interval())

    agent_running = False
    if agent_error_count < MAX_ERRORS:
        print("Agent stopped.")
    else:
        print("\nPress Enter to return to the menu.")


