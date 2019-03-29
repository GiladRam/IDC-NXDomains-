class DomainMeasurementResult(object):
    TOTAL_NUMBER_OF_QUERIES = 4

    def __init__(self,
                 domain,
                 dns_server_ip,
                 probe_id,
                 cached_queries,
                 run_id):
        self.domain = domain
        self.dns_server_ip = dns_server_ip
        self.probe_id = probe_id
        self.cached_queries = cached_queries
        self.uncached_queries = self.TOTAL_NUMBER_OF_QUERIES - cached_queries
        self.run_id = run_id

    @staticmethod
    def translate_to_es_doc(index, item):
        doc = item.__dict__
        doc['_index'] = index
        doc['_type'] = 'doc'
        doc['pipeline'] = 'geoip'
        return doc

    @staticmethod
    def bulk_translate(index, bulk):
        doc_list = list()
        for item in bulk:
            doc_list.append(DomainMeasurementResult.translate_to_es_doc(index, item))
        return doc_list
