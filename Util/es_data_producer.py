from elasticsearch import Elasticsearch
from elasticsearch import helpers

from Domain.measurment import Measurement
from Util.es_data_collector import DNSESDataCollector
from elasticsearch.serializer import JSONSerializer


class ESDataProducer(object):

    def __init__(self, run_id, hosts, index_name="measurement_results"):
        self.run_id = run_id
        self.index = index_name + "_" + str(run_id)
        self.client = Elasticsearch(hosts, serializer=SetEncoder())

    def index_data(self, list_of_measurement):
        return helpers.bulk(self.client,
                            Measurement.bulk_translate(self.index, list_of_measurement),
                            chunk_size=1000,
                            request_timeout=200)


class SetEncoder(JSONSerializer):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONSerializer.default(self, obj)


if __name__ == '__main__':
    dnsES = DNSESDataCollector(["localhost"], "packetbeat*")
    producer = ESDataProducer(1, ["localhost"])
    m = Measurement("provider", 20402246, "8.8.8.8", 1)
    m.validate_and_populate_measurement()

    dnsES.collect_data_on_measurement(m)
    producer.index_data([m])
