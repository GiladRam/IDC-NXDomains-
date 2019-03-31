# IDC-NXDomains-

![alt text](https://i.imgur.com/oKb6twJ.png)

![alt text](https://i.imgur.com/rCnpOr4.png)

##### This project explores the commonness of DNS caching over public DNS recursive resolvers located in multiple geographic locations containing load balancing functionality. Load balancing is a key feature of DNS efficiency and has a direct contribution to the measurements outcome. The questions we examine were how long will the lack of DNS record hold on the internet? how many balancers effects the negative cache efficiency? Is there any difference between resolvers in different locations?
 
We used a fixed TTL field within the SOA minimum field of our authoritative server and a public DNS provider such as GoogleDNS, openDNS, cloudflare, quad9, Norton  as targeted recursive resolver. This is crucial in order to measure negative cache with the same recursive resolver service.

Our first contribution is to set an end-to-end test measuring the mechanism of NXDomain queries to targeted public dns recursive resolvers. We aim to simplify the DNS behaviour in order to gain a better understanding of negative cache process. A major outcome showed that 47% of the public DNS servers do implement the negative cache functionality.

Our second contribution is the combination of negative cache mechanism VS. load balancing functionality. We will show that load balancing is also crucial for security and has a direct effect on authoritative servers query load. Finally, although load balancing and negative cache can have an opposite correlation, implementing both of them is fundamental for the valid operation of DNS service. 

##                                                   Related work

We reviewed the work of lagerholm and rolelli for Microsoft called "negative caching of DNS record".  at the Spring 2015 DNS-OARC workshop which aimed to examine negative cache behavior and to see whether it complaint to the RFC. Their experiment include a comparison between the SOA TTL to the real "negative TTL" on 1M top ALEXA domains. Their major contribution was that about 45% of the domains has negative TTL value between one hour and 1 day, which is very high, so an accidental deletion of a record will have an impact on the internet for more than one hour. This could potentially slowing full internet-wide recovery times for mistakenly removed records. 
Another work we reviewed was the work of Moura, Heidemann and Muller on May 2018, "When the Dike Breaks: Dissecting DNS Defenses During DDos". Their assessment was on DNS resilience during DDoS attacks, with the goal of explaining different outcomes from different attacks (authoritative VS root servers) through understanding the role of DNS Caching, retries and the use of multiple DNS Recursive resolvers. Their first conclusion was that caching (positive and negative) behave as expected although 30% of the time clients have not benefit from it. Their main outcome was that DNS mechanism of caching and retries provide significant resilience client user experience during DDoS attacks. With very heavy query loss (90%) on all authoritatives, full caches protect half of the clients, and retries protect 30%.  
 
##                                                 Technical details

In this section, we suggest a novel experiment, based on Moure and Giovane experiment, to evaluate the percentage of DNS servers that cache NXDomain responses. In the experiment, we target 100 random DNS servers using a worldwide collection of ~13k public DNS servers from 239 countries. The experiment is as follow:

Set up a DNS authoritative server on port 53 and configure it to response a TTL of 604800 seconds (7 days)
Set up an ELK stack with packetbeat to record all ingress traffic  
Randomly select 100 DNS servers from a csv file that contains ~13K public DNS servers 
Using the enormous strength of ripe atlas vantage points in order to perform DNS queries to the chosen servers.
 We make 100 unique DNS measurements using ripe atlas API. At each measurement we use 3 different vantage points to send a total of 12 DNS queries (4 queries for each vantage point). In order to perform unique queries, we structure the request domain name as follow [target ip]_[test round]_[prob id].nxdomain-test.live. By that, each one of the vantage points sends a different domain request which further on help us to test the target domain cache behavior.
All the queries eventually lead to our pre-setup authoritative server* and index into ES.
Analyze data and perform data enrichment using ES. 
Once all measurements end, collect measurements results from Ripe Atlas.
Merge Ripe Atlas measurements results and the captured traffic from the authoritative server. The merge is done by differentiating the amount of valid (where the src IP is identical to the tested target IP) incoming queries recorded on the authoritative server and the number of valid (queries that got an NXDomain replay) queries that were actually sent by the each one of the relevant measurements 
Index merged results in results index on ES. 
In the final stage,  we use collected data and our acquired knowledge in order to present the research findings in different sorts of related graphs using Kibana (data visualization tool over Elasticsearch).
