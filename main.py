from datetime import datetime
from time import sleep

from Util import es_data_producer, es_data_collector
from Util import ripe_util

if __name__ == '__main__':
    collector = es_data_collector.DNSESDataCollector(["localhost"], "packetbeat*")
    producer = es_data_producer.ESDataProducer(1, ["localhost"])
    measurements, experiment_end_time = ripe_util.run_experiment(8, 10)
    experiment_end_time = datetime.fromtimestamp(experiment_end_time)
    now = datetime.now()

    print("Waiting until experiment end...")
    while experiment_end_time > now:
        print("The experiment will end in %s seconds" % (experiment_end_time - now).seconds)
        sleep(30)
        now = datetime.now()

    print("----------------------------------------------------------------------")
    print("starting data enrichment!")
    print("----------------------------------------------------------------------")
    for measurement in measurements:
        print("collecting data on experiment measurements from ripe atlas.")
        measurement.validate_and_populate_measurement()
        print("----------------------------------------------------------------------")
        print("Merging measurement results with data from ES.")
        print("----------------------------------------------------------------------")
        collector.collect_data_on_measurement(measurement)
        producer.index_data(measurements)
