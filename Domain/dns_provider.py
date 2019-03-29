

class DnsProvider(object):
    def __init__(self, provider_name, primary_dns, secondary_dns, round_num=1):
        self.name = provider_name
        self.primary = primary_dns
        self.second = secondary_dns
        self.round = round_num


def from_list_to_dns_providers(ips):
    dns_providers = []
    for ip in ips:
        dns_provider = DnsProvider("", ip, "")
        dns_providers.append(dns_provider)

    return dns_providers
