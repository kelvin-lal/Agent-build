"""
Kelvin's Agent
"""

import os
import time
from metrics.metrics import Metrics
from metrics.metricSubmission import metric_submission, metric_batch_submission
from metrics.metricBuffer import MetricBuffer
from metrics.metricsConfig import metrics_config
from checks.checkRun import Check
from agent.config import config
from checks.customCheck import CustomCheck
from metrics.tags.tagProvider import HostTagProvider
from metrics.tags.tagEnricher import TagEnricher


agent_running = False
agent_error_count = 0
agent_last_error = None
MAX_ERRORS = 10


def _flush_buffer(buffer, enricher):
    series_list = buffer.flush()
    if series_list:
        enriched = enricher.enrich(series_list)
        metric_batch_submission(enriched)


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
        buffer = MetricBuffer()
        tag_provider = HostTagProvider()
        tag_enricher = TagEnricher(tag_provider)
    except Exception as e:
        print(f"[ERROR] Failed to initialize collectors: {e}")
        agent_running = False
        return

    last_flush_time = time.monotonic()

    while agent_running:
        try:
            cpu_metrics = metrics.cpuMetrics()
            for metric_name, metric_value in cpu_metrics.items():
                buffer.add(metric_name, metric_value)
                Check.metric_counts["cpu"] += 1
        except Exception as e:
            agent_error_count += 1
            agent_last_error = f"CPU metric collection failed: {e}"
            print(f"[ERROR] ({agent_error_count}/{MAX_ERRORS}) {agent_last_error}")
            if agent_error_count >= MAX_ERRORS: break

        try:
            memory_metrics = metrics.memoryMetrics()
            for metric_name, metric_value in memory_metrics.items():
                buffer.add(metric_name, metric_value)
                Check.metric_counts["memory"] += 1
        except Exception as e:
            agent_error_count += 1
            agent_last_error = f"Memory metric collection failed: {e}"
            print(f"[ERROR] ({agent_error_count}/{MAX_ERRORS}) {agent_last_error}")
            if agent_error_count >= MAX_ERRORS: break

        try:
            disk_metrics = metrics.diskMetrics()
            for metric_name, metric_value in disk_metrics.items():
                buffer.add(metric_name, metric_value)
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

        elapsed = time.monotonic() - last_flush_time
        if elapsed >= metrics_config.get_submission_interval():
            try:
                _flush_buffer(buffer, tag_enricher)
            except Exception as e:
                agent_error_count += 1
                agent_last_error = f"Metric flush failed: {e}"
                print(f"[ERROR] ({agent_error_count}/{MAX_ERRORS}) {agent_last_error}")
            last_flush_time = time.monotonic()

        time.sleep(metrics_config.get_collection_interval())

    try:
        _flush_buffer(buffer, tag_enricher)
    except Exception as e:
        print(f"[ERROR] Final flush failed: {e}")

    agent_running = False
    if agent_error_count < MAX_ERRORS:
        print("Agent stopped.")
    else:
        print("\nPress Enter to return to the menu.")


