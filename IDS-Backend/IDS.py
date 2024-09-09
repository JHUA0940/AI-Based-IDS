from scapy.all import sniff, TCP, UDP, IP
from collections import defaultdict
import time

# Store traffic stats to calculate values like count, serror_rate, etc.
traffic_stats = defaultdict(lambda: {
    "count": 0, "srv_count": 0, "same_srv_count": 0, "diff_srv_count": 0,
    "serror_count": 0, "rerror_count": 0, "diff_host_srv_count": 0,
    "services": set(), "hosts": set()
})


# Helper function to get the protocol and service
def get_protocol_service(packet):
    if TCP in packet:
        return 'tcp', 'http' if packet[TCP].sport == 80 else 'private'
    elif UDP in packet:
        return 'udp', 'dns' if packet[UDP].sport == 53 else 'other'
    else:
        return 'other', 'other'


# Helper function to determine if an error occurred
def is_error(packet):
    if TCP in packet and (packet[TCP].flags == 'R' or packet[TCP].flags == 'F'):
        return True
    return False


# Function to analyze the flags
def get_flags(packet):
    if TCP in packet:
        flags = packet[TCP].flags
        if flags == "S":
            return "S0"
        elif flags == "SA":
            return "SF"
        elif flags == "FA":
            return "REJ"
        else:
            return str(flags)
    return "none"


# Function to check if source and destination IP are the same (land attack)
def is_land(packet):
    return 1 if packet[IP].src == packet[IP].dst else 0


# Function to generate a row in the desired format
def generate_row(packet):
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    protocol_type, service = get_protocol_service(packet)
    flag = get_flags(packet)
    src_bytes = len(packet[IP])
    dst_bytes = len(packet[IP].payload)
    land = is_land(packet)

    # Use source and destination IP as a key
    key = (src_ip, dst_ip, protocol_type)

    # Update traffic stats
    traffic_stats[key]["count"] += 1
    if service in traffic_stats[key]["services"]:
        traffic_stats[key]["same_srv_count"] += 1
    else:
        traffic_stats[key]["diff_srv_count"] += 1
        traffic_stats[key]["services"].add(service)

    if dst_ip in traffic_stats[key]["hosts"]:
        traffic_stats[key]["diff_host_srv_count"] += 1
    else:
        traffic_stats[key]["hosts"].add(dst_ip)

    if is_error(packet):
        traffic_stats[key]["rerror_count"] += 1 if protocol_type == 'udp' else 0
        traffic_stats[key]["serror_count"] += 1 if protocol_type == 'tcp' else 0

    # Calculate rates
    count = traffic_stats[key]["count"]
    serror_rate = traffic_stats[key]["serror_count"] / count if count else 0
    rerror_rate = traffic_stats[key]["rerror_count"] / count if count else 0
    same_srv_rate = traffic_stats[key]["same_srv_count"] / count if count else 0
    diff_srv_rate = traffic_stats[key]["diff_srv_count"] / count if count else 0
    srv_diff_host_rate = traffic_stats[key]["diff_host_srv_count"] / count if count else 0

    # Generate row based on KDD format
    row = [
        0, protocol_type, service, flag, src_bytes, dst_bytes, land, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        count, traffic_stats[key]["srv_count"], serror_rate, rerror_rate, same_srv_rate, diff_srv_rate,
        srv_diff_host_rate,
        255, 25, 0.17, 0.03, 0.17, 0.00, 0.00, 0.00, 0.05, 0.00,  # Some additional dummy data
        'normal', 20  # Attack label and duration placeholder
    ]
    return row


# Function to print the CSV row for each packet
def packet_callback(packet):
    if IP in packet:
        row = generate_row(packet)
        print(','.join(map(str, row)))


# Function to capture traffic
def capture_traffic(duration=60):
    sniff(prn=packet_callback, timeout=duration)


# Capture network traffic for 60 seconds
capture_traffic(60)
