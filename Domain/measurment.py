import ast
from datetime import datetime

import requests
from ripe.atlas.sagan import DnsResult

headers = {'content-type': 'application/json', 'Accept': 'application/json'}


class Measurement(object):
    def __init__(self, provider_name, id, ip, round_num):
        self.name = provider_name
        self.id = id
        self.dns_server_ip = ip
        self.round = round_num
        self.response_time = list()
        self.dns_questions = set()
        self.number_of_requests = 0
        self.number_of_uncached_requests = 0
        self.timestamp = datetime.now()

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
            doc_list.append(Measurement.translate_to_es_doc(index, item))
        return doc_list

    def validate_and_populate_measurement(self):
        api_address = 'https://atlas.ripe.net:443/api/v2/measurements/%s/results/' % self.id
        r = requests.get(api_address, headers=headers)
        res = ast.literal_eval(r.text)
        count_of_valid_responses = 0

        for request in res:
            current_dns_result = DnsResult(request)
            response_probe_id = current_dns_result.probe_id

            try:
                ret_code = current_dns_result.responses[0].abuf.header.return_code
                response_time = current_dns_result.responses[0].response_time
                dns_question_name = current_dns_result.responses[0].abuf.questions[0].name
                print("The request was sent from prob_id %d" % response_probe_id)
                print("The response_time is " + str(response_time))

                if ret_code != "NXDOMAIN":
                    print(ret_code)
                    print("At least one of the %s responses is not NXDOMAIN but %s" % (self.id, ret_code))
                else:
                    self.response_time.append(response_time)
                    self.dns_questions.add(str(dns_question_name))
                    count_of_valid_responses += 1
            except:
                print("The response of probe id %s was not valid" % response_probe_id)
        self.number_of_requests = count_of_valid_responses
        print("The number of requests is %s at %s" % (str(count_of_valid_responses), str(datetime.now())))


if __name__ == '__main__':
    m = Measurement("provider", "20402246", "8.8.8.8", 1)
    m.validate_and_populate_measurement()
    print(m.__dict__)
