from scapy.all import sniff, IP, DNS, DNSQR, DNSRR
import socket

ip_domain_cache = {}

def try_resolve(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown"

def process_packet(packet):
    # Track DNS queries and responses
    if packet.haslayer(DNS):
        dns_layer = packet[DNS]
        ip_layer = packet[IP]

        # DNS Query
        if dns_layer.qr == 0 and packet.haslayer(DNSQR):
            domain = dns_layer[DNSQR].qname.decode().strip(".")
            target_ip = ip_layer.dst
            ip_domain_cache[target_ip] = domain
            print(f"[DNS Query ] {domain} → {target_ip}")

        # DNS Answer
        elif dns_layer.qr == 1 and dns_layer.ancount > 0:
            for i in range(dns_layer.ancount):
                rr = dns_layer.an[i]
                if isinstance(rr, DNSRR) and rr.type == 1:  # A record
                    resolved_ip = rr.rdata
                    resolved_domain = rr.rrname.decode().strip(".")
                    ip_domain_cache[resolved_ip] = resolved_domain
                    print(f"[DNS Answer] {resolved_domain} ← {resolved_ip}")

    # IP traffic tracking
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        src_domain = ip_domain_cache.get(src_ip, try_resolve(src_ip))
        dst_domain = ip_domain_cache.get(dst_ip, try_resolve(dst_ip))

        print(f"[+] Traffic  : {src_ip} ({src_domain}) → {dst_ip} ({dst_domain})")

def main():
    print("🔎 Monitoring DNS + IP Traffic (Press Ctrl+C to stop)...\n")
    sniff(filter="ip or udp port 53", prn=process_packet, store=False)

if __name__ == "__main__":
    main()
