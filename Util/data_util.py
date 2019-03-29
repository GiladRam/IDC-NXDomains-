import csv
import random

from Domain.dns_provider import DnsProvider


def from_list_to_dict(list_of_ips):
    results = dict()
    for ip in list_of_ips:
        if ip in results:
            results[ip] += 1
        else:
            results[ip] = 1
    return results


def generate_list_with_random_numbers(size):
    return [int(13574 * random.random()) for i in range(size)]


def load_dns_providers_from_csv(path_to_csv=r"/home/ubuntu/NXDomian/resources/nameservers.csv", size=1000):
    # choose 1000 random numbers from 0 to 13574 to select dns providers randomly
    rand_indexies = generate_list_with_random_numbers(size)
    dns_providers = list()
    # Read the NameServers csv and choose randomly nameservers from it
    with open(path_to_csv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_rows = [r for r in csv_reader]
        line_count = 0

        for index in rand_indexies:
            row = csv_rows[index]
            if index != 0:  # Jump over headers line
                if ":" not in row[0]:  # Skip unwanted values
                    dns_provider = DnsProvider(row[1], row[0], "")
                    dns_providers.append(dns_provider)
                    line_count += 1
    return dns_providers
