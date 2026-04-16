"""
Kelvin's Agent
"""

from datadog_api_client.v2.model.metric_resource import MetricResource


class TagEnricher:
    def __init__(self, tag_provider):
        self._tag_provider = tag_provider

    def enrich(self, series_list):
        tags = self._tag_provider.get_tags()
        hostname = self._tag_provider.get_hostname()
        host_resource = MetricResource(name=hostname, type="host")

        for series in series_list:
            series.tags = tags
            series.resources = [host_resource]

        return series_list
