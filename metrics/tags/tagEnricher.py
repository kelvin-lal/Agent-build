"""
Kelvin's Agent
"""

from datadog_api_client.v2.model.metric_resource import MetricResource


class TagEnricher:
    def __init__(self, tag_provider, custom_tag_store):
        self._tag_provider = tag_provider
        self._custom_tag_store = custom_tag_store

    def enrich(self, series_list):
        tags = self._tag_provider.get_tags() + self._custom_tag_store.get_tags()
        hostname = self._tag_provider.get_hostname()
        host_resource = MetricResource(name=hostname, type="host")

        for series in series_list:
            series.tags = tags
            series.resources = [host_resource]

        return series_list
