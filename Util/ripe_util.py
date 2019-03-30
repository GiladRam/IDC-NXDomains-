import ast
import datetime
import time

import requests

from Domain.measurment import Measurement
from Util.data_util import load_dns_providers_from_csv

API_MEASUREMENT_BASE_REQ = '''{
         "definitions": [
          {
           "target": "%s",
           "af": 4,
           "query_class": "IN",
           "query_type": "A",
           "query_argument": "%s_$p_%d.nxdomain-test.live",
           "use_macros": true,
           "description": "DNS measurement round %d to %s",
           "interval": 120,
           "use_probe_resolver": false,
           "resolve_on_probe": false,
           "set_nsid_bit": false,
           "protocol": "UDP",
           "udp_payload_size": 512,
           "retry": 2,
           "skip_dns_check": false,
           "include_qbuf": false,
           "include_abuf": true,
           "prepend_probe_id": false,
           "set_rd_bit": true,
           "set_do_bit": false,
           "set_cd_bit": false,
           "timeout": 5000,
           "type": "dns"
          }
         ],
         "probes": [
          {
           "type": "area",
           "value": "WW",
           "requested": 3
          }
         ],
         "is_oneoff": false,
         "bill_to": "bremler@idc.ac.il",
         "stop_time": %s
        }'''

measurements = []
api_address = 'https://atlas.ripe.net/api/v2/measurements?key=b1b516d2-4259-4b01-be2c-6d0f26254b54'
headers = {'content-type': 'application/json', 'Accept': 'application/json'}


def run_experiment(experiment_num, size):
    dns_providers = load_dns_providers_from_csv(size=size)
    print("There will be %d new measurements" % (len(dns_providers)))
    # Loop over all choosen providers and measure them
    for dns_provider in dns_providers:
        start_time = time.time()
        stop_time = int(start_time + 600)

        # Our target dns primary ip
        target_ip = dns_provider.primary

        # The new measurement request api
        api_measurement_request = API_MEASUREMENT_BASE_REQ % (
            target_ip, target_ip, experiment_num, experiment_num, target_ip, stop_time)

        print("Round number %d - a new measurement for %s was created at %s"
              % (experiment_num, target_ip, datetime.datetime.now()))

        # Send a request to create a new measurement
        api_request = requests.post(api_address, data=api_measurement_request, headers=headers)
        response = ast.literal_eval(api_request.text)

        try:
            # Create a new measurement object and add it to the list
            measurement_id = response.get("measurements")[0]
            measurement = Measurement(dns_provider.name, measurement_id, target_ip, experiment_num)
            measurements.append(measurement)

        except:
            print("There was a problem creating a measurement")
            print(response)

    return measurements, stop_time


if __name__ == '__main__':
    run_experiment(12)
