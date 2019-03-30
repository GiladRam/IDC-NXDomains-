from elasticsearch import Elasticsearch
from Util import data_util
from Domain.measurment import *
import copy


class DNSESDataCollector(object):
    BASE_RESOURCE_AND_CLIENT_IP_FILTER_SCRIPT = \
        "%s.contains(doc['resource'].value) && !doc['resource'].value.contains(doc['client_ip'].value)"
    BASE_TEST_ROUND_REG = "[0-9]*\\.[0-9]*\\.[0-9]*\\.[0-9]*_[0-9]*_%s.nxdomain-test.*"
    BASE_DISCOVER_DNS_SERVERS = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "type": {
                                "value": "dns"
                            }
                        }
                    },
                    {
                        "regexp": {
                            "resource": "[0-9]*\\.[0-9]*\\.[0-9]*\\.[0-9]*_[0-9]*_1.nxdomain-test.*"
                        }

                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": 1553545080724,
                                "lte": 1553548680724,
                                "format": "epoch_millis"
                            }
                        }
                    }
                ],
                "filter": {
                    "script": {
                        "script": {
                            "source": "doc['resource'].value.contains(doc['client_ip'].value)",
                            "lang": "painless"
                        }
                    }
                }
            }
        }
    }

    BASE_DNS_RESULT_BY_IP_QUERY = {
        "query": {
            "bool": {
                "must": [
                    {"term": {
                        "type": {
                            "value": "dns"
                        }
                    }},
                    {"term": {
                        "client_ip": {
                            "value": "ip_add"
                        }
                    }}
                ]
            }
        }
    }

    BASE_SHOULD_IDENTICAL = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "type": "dns"
                        }
                    },
                    {
                        "script": {
                            "script": {
                                "inline": "boolean compare(Supplier s, def v) {return s.get() == v;}compare(() -> { doc['resource'].value.contains(doc['client_ip'].value) }, params.value);",
                                "lang": "painless",
                                "params": {
                                    "value": True
                                }
                            }
                        }
                    },
                    {
                        "bool": {
                            "should": []
                        }
                    }
                ]
            }
        }
    }

    BASE_TERM = {"term": {"resource": "requested_domain_name"}}

    def __init__(self, hosts, index_name):
        self.es_client = Elasticsearch(hosts=hosts)
        self.index = index_name

    def collect_dns_result_data(self, dns_server_ip):
        base_query = self.BASE_DNS_RESULT_BY_IP_QUERY.copy()
        base_query["query"]["bool"]["must"][1]["term"]["client_ip"]["value"] = dns_server_ip
        result = self.es_client.search(self.index, body=base_query)
        if "hits" in result:
            return result['hits']
        else:
            return None

    def collect_identical_dns_servers(self, round_id=1):
        base_query = self.BASE_DISCOVER_DNS_SERVERS.copy()
        base_query['query']['bool']['must'][1]['regexp']['resource'] = self.BASE_TEST_ROUND_REG % round_id
        result = self.es_client.search(self.index, body=self.BASE_DISCOVER_DNS_SERVERS, size=10000)
        relevant_dns_servers = list()
        if "hits" in result:
            for hit in result['hits']['hits']:
                relevant_dns_servers.append(hit['_source']["client_ip"])
        return relevant_dns_servers

    def collect_data_on_measurement(self, measurement):
        base_should_query = copy.deepcopy(self.BASE_SHOULD_IDENTICAL)
        for dns_query_name in measurement.dns_questions:
            base_term_query = copy.deepcopy(self.BASE_TERM)
            base_term_query['term']['resource'] = dns_query_name
            base_should_query['query']['bool']['must'][2]['bool']['should'].append(base_term_query)

        result = self.es_client.search(self.index, body=base_should_query, size=10000)
        if "hits" in result:
            measurement.number_of_uncached_requests = result['hits']['total']

    def update_document(self, document_id, data_to_merge):
        update_res = self.es_client.update(index=self.index,
                                           doc_type='doc',
                                           id=document_id,
                                           body=data_to_merge)
        return update_res


if __name__ == '__main__':
    dnsES = DNSESDataCollector(["localhost"], "packetbeat*")
    res_a = data_util.from_list_to_dict(dnsES.collect_identical_dns_servers(1))
    res_b = data_util.from_list_to_dict(dnsES.collect_identical_dns_servers(2))
    res_c = data_util.from_list_to_dict(dnsES.collect_identical_dns_servers(3))
    round_a = set(res_a.keys())
    round_b = set(res_b.keys())
    round_c = set(res_c.keys())
    round_a.__contains__(round_b)

    m = Measurement("provider", 20402246, "8.8.8.8", 1)
    m.validate_and_populate_measurement()

    dnsES.collect_data_on_measurement(m)
    print(m.__dict__)
