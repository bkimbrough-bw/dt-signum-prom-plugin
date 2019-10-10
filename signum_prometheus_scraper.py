import requests
from prometheus_client.parser import text_string_to_metric_families
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.data import PluginMeasurement
from ruxit.api.snapshot import parse_port_bindings


class SignumPrometheusScraper(BasePlugin):

    absolute_types = {
        'gauge',
        'summary',
        'histogram'
    }

    relative_types = {
        'counter'
    }

    per_second_types = {}

    def isSignumProcessGroup(self):
        return lambda pgi: 'com.bandwidth.identity.signum.SignumApplication' in pgi.group_name

    def query(self, **kwargs):
        # we probably should have more predictable process names some how
        pgi_list = self.find_all_process_groups(self.isSignumProcessGroup())
        for pgi in pgi_list:
            pgi_id = pgi.group_instance_id
            for (ip, port) in parse_port_bindings(pgi):
                if port == 8888:
                    stats_url = f"http://{ip}:{port}/actuator/prometheus"
                    stats = requests.get(stats_url).content

                    for family in text_string_to_metric_families(stats):
                        for sample in family.samples:
                            metric = PluginMeasurement(key=sample[0],
                                                       dimensions=sample[1],
                                                       value=sample[2],
                                                       entity_selector=pgi_id)

                            if family.type in self.per_second_types:
                                self.results_builder.add_per_second_result(metric)
                            elif family.type in self.relative_types:
                                self.results_builder.add_relative_result(metric)
                            else:
                                self.results_builder.add_absolute_result(metric)

