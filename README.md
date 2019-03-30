# IDC-NXDomains-

![alt text](https://imgur.com/oKb6twJ)

![alt text](https://imgur.com/rCnpOr4)


The Domain Name System is one of the most vital protocols of the modern internet.
The workflow of the protocol has been researched constantly due to his profound impact on the operation of the Internet. Since name resolution is a necessary step in almost any Internet activity. DNS query overload at authoritative servers has the potential to denial a service to major websites, especially at Public DNS services. One way to apply it is creating a DDOS Attack on the internet's DNS services like the huge October 2016 attack against Dyn [3] on it authoritative servers, resulting in disruptions at a number of prominent websites, including Twitter, Netflix and the New York Times [4].
There are many stages involved to fully resolve a DNS. The goal is to get an IP Address (A or AAAA record), but there is a variety of RR (resource records) to get the DNS hierarchy work (NS, MX, SOA records or DNSSEC records). Usually, a stub (resolver) ask for an IP Address in a form of an A record and then a hierarchy of recursive servers come into action and create multiple queries transaction to authoritative and root servers in order to complete the process.
 
In order to avoid unnecessary query overload to Root and authoritative servers, major DNS functionality is the DNS Caching on recursive servers. In the resolving process, the recursive server saves the answer in its cache memory for a time period distinguish by a TTL field given by the RR's response. For every valid record, we called it "positive cache"[5]. Let's take a look on a valid domain google.com. Getting an A answer for the domain will result with a response contains authoritative servers and TTL field for the recursive server to store.

What happens when a domain name does not exist? If domain name is unable to resolved using the DNS, a condition called the NXDOMAIN occurred. For example sending a query to foobar.google.com will result with the NXDomain answer.  

Since the domain name is the invalid domain, we got NXDomain response i.e an error message indicating that domain is either not registered or invalid. In this case, do we wish to save the response in the cache? (Yes!). Imagine what could have happened in the event there is no caching policy for NXDomain and its contribution to query load on authoritative servers. According to DNS Spec [6], this is called "negative cache". Negative answer gets their TTL value from the SOA minimum field (The TTL of the SOA record itself). This is required so that the response may be cached. Negative cache implementation, in reality, depend on the SOA minimum field configuration. Although there are default configuration in well-known resolvers [7] it can be change by IT managers for TLDs (ccTLD). A lower negative cache time is more user-friendly but, on the other hand, means a higher query load on the name server.
 
This paper explores the commonness of DNS caching over public DNS recursive resolvers located in multiple geographic locations containing load balancing functionality. Load balancing is a key feature of DNS efficiency [8] and has a direct contribution to the measurements outcome. The questions we examine were how long will the lack of DNS record hold on the internet? how many balancers effects the negative cache efficiency? Is there any difference between resolvers in different locations?
 
We used a fixed TTL field using the SOA minimum field of our authoritative server and a public DNS provider such as GoogleDNS, openDNS, cloudflare, quad9, Norton, etc, as targeted recursive resolver. This is crucial in order to measure negative cache with the same recursive resolver service.

Our first contribution is to set an end-to-end test measuring the mechanism of NXDomain queries to targeted public dns recursive resolvers. We aim to simplify the DNS workflow in order to gain a better understanding of negative cache process. A major outcome showed that 47% of the public DNS servers do implement the negative cache functionality.

Our second contribution is the combination of negative cache mechanism VS. load balancing functionality. We will show that load balancing is also crucial for security and has a direct effect on authoritative servers query load. Finally, although load balancing and negative cache can have an opposite correlation, implementing both of them is fundamental for the valid operation of DNS service. 
