import psutil
from scapy.all import sniff, get_working_ifaces, IP, TCP, UDP, ICMP
import time
from collections import defaultdict

# Global start time to calculate duration
start_time = time.time()

# Dictionary to map common port numbers to services (you can expand this as needed)
service_mapping = {
    80: "http",
    443: "https",
    21: "ftp",
    22: "ssh",
    25: "smtp",
    110: "pop3",
    143: "imap4",
    53: "dns",
    23: "telnet",
    # Add other services here based on the @attribute 'service' list
    20: "ftp_data",
    113: "auth",
    179: "bgp",
    9: "discard",
    37: "time",
    19: "chargen",
    514: "shell",
    513: "login",
    79: "finger"
}

# Possible protocol types
protocol_type_mapping = {
    6: 'tcp',
    17: 'udp',
    1: 'icmp'
}

# TCP flags to match the @attribute 'flag' list
flag_mapping = {
    'S': 'SF',  # SYN flag set, similar to "SF"
    'R': 'REJ',  # RST flag set, maps to "REJ"
    'F': 'S0',  # No SYN but FIN or RST, used as an example
    'P': 'SH',  # SYN+FIN flag, "SH" (used as an example for simplification)
    # Add more mappings as needed
}

# Store connection and packet info for calculating fields
connection_info = defaultdict(
    lambda: {'count': 0, 'srv_count': 0, 'serror_count': 0, 'rerror_count': 0, 'start_time': None,
             'same_srv_count': 0, 'diff_srv_count': 0})

# Store destination host metrics (dst_host_* fields)
dst_host_info = defaultdict(
    lambda: {'count': 0, 'srv_count': 0, 'serror_count': 0, 'rerror_count': 0})

# Function to process each packet and immediately print the results
def process_packet(packet):
    if IP in packet:  # Ensure the packet has an IP layer
        # Identify the protocol and set service based on port
        protocol = packet[IP].proto
        protocol_type = protocol_type_mapping.get(protocol, "other")  # Use protocol type mapping

        if protocol_type == "tcp" and TCP in packet:
            sport = packet[TCP].sport
            dport = packet[TCP].dport
            service = service_mapping.get(dport, "private")  # Map the destination port to a service
            flags = packet[TCP].sprintf("%TCP.flags%")  # Extract the TCP flags
            flag = flag_mapping.get(flags, "OTH")  # Map flags to appropriate value
            connection_key = (packet[IP].src, packet[IP].dst, dport)
        elif protocol_type == "udp" and UDP in packet:
            sport = packet[UDP].sport
            dport = packet[UDP].dport
            service = service_mapping.get(dport, "private")  # Map the destination port to a service
            flag = "SF"  # Since UDP doesn't have TCP flags, default to "SF"
            connection_key = (packet[IP].src, packet[IP].dst, dport)
        elif protocol_type == "icmp" and ICMP in packet:
            service = "eco_i"  # For ICMP, default to "eco_i"
            flag = "OTH"  # ICMP doesn't have TCP flags, default to "OTH"
            connection_key = (packet[IP].src, packet[IP].dst, protocol)
        else:
            service = "other"
            flag = "OTH"
            connection_key = (packet[IP].src, packet[IP].dst, protocol)

        # Update connection statistics
        conn = connection_info[connection_key]
        if conn['start_time'] is None:
            conn['start_time'] = time.time()  # Record the start time for this connection

        # Calculate duration from connection start time to current packet's time
        duration = time.time() - conn['start_time']

        conn['count'] += 1
        if protocol_type == "tcp" and TCP in packet and packet[TCP].flags == "S":
            conn['serror_count'] += 1
        if protocol_type == "tcp" and TCP in packet and packet[TCP].flags == "R":
            conn['rerror_count'] += 1
        srv_count = conn['count']

        # Update dst_host metrics
        dst_host = packet[IP].dst
        dst_host_conn = dst_host_info[dst_host]
        dst_host_conn['count'] += 1
        if service == "private":  # Simple assumption that private services are treated as errors
            dst_host_conn['serror_count'] += 1
        dst_host_conn['srv_count'] += 1

        # Calculate same_srv_rate and diff_srv_rate
        for other_conn in connection_info.values():
            if other_conn != conn:
                if other_conn['srv_count'] == conn['srv_count']:
                    conn['same_srv_count'] += 1
                else:
                    conn['diff_srv_count'] += 1

        # Source and destination bytes
        src_bytes = len(packet[IP].payload)  # Source bytes
        dst_bytes = len(packet[IP].payload)  # Destination bytes

        # Calculate additional fields
        wrong_fragment = 1 if packet[IP].frag > 0 else 0
        urgent = 1 if TCP in packet and packet[TCP].urgptr > 0 else 0
        hot = 0  # This requires application layer data to compute
        num_failed_logins = 0  # Needs to track login attempts at application layer
        logged_in = 0  # Application layer state
        num_compromised = 0  # Requires tracking security states over time
        root_shell = 0  # Can only be detected with privilege escalation attempts in application layer
        su_attempted = 0  # Needs application level data
        num_root = 0  # Also needs privileged commands tracking
        num_file_creations = 0  # Requires file system access tracking
        num_shells = 0  # Tracking shell access attempts in application layer
        num_access_files = 0  # Requires application level data for file access
        num_outbound_cmds = 0  # Could track outbound connections made via command shell
        is_host_login = 0  # Needs higher level context
        is_guest_login = 0  # Similar, requires login state tracking

        # Error rates based on TCP flags
        serror_rate = conn['serror_count'] / conn['count'] if conn['count'] > 0 else 0
        srv_serror_rate = conn['serror_count'] / srv_count if srv_count > 0 else 0
        rerror_rate = conn['rerror_count'] / conn['count'] if conn['count'] > 0 else 0
        srv_rerror_rate = conn['rerror_count'] / srv_count if srv_count > 0 else 0

        # Same service rates
        same_srv_rate = conn['same_srv_count'] / conn['count'] if conn['count'] > 0 else 0
        diff_srv_rate = conn['diff_srv_count'] / conn['count'] if conn['count'] > 0 else 0

        # Host-based metrics
        dst_host_count = dst_host_conn['count']
        dst_host_srv_count = dst_host_conn['srv_count']
        dst_host_same_srv_rate = same_srv_rate
        dst_host_diff_srv_rate = diff_srv_rate
        dst_host_same_src_port_rate = 1.0  # Assuming the same source port for all packets
        dst_host_serror_rate = dst_host_conn['serror_count'] / dst_host_conn['count'] if dst_host_conn['count'] > 0 else 0
        dst_host_srv_serror_rate = dst_host_conn['serror_count'] / dst_host_srv_count if dst_host_srv_count > 0 else 0
        dst_host_rerror_rate = rerror_rate
        dst_host_srv_rerror_rate = srv_rerror_rate

        # Define attack type as normal (for now, no real attack detection)
        attack = "normal"

        # Format the result as a comma-separated string
        result = [
            f"{duration:.2f}", protocol_type, service, flag, src_bytes, dst_bytes, 0, wrong_fragment, urgent, hot,
            num_failed_logins, logged_in, num_compromised, root_shell, su_attempted, num_root,
            num_file_creations, num_shells, num_access_files, num_outbound_cmds, is_host_login,
            is_guest_login, conn['count'], srv_count, f"{serror_rate:.2f}", f"{srv_serror_rate:.2f}",
            f"{rerror_rate:.2f}", f"{srv_rerror_rate:.2f}", f"{same_srv_rate:.2f}", f"{diff_srv_rate:.2f}", 0.00,
            dst_host_count, dst_host_srv_count, f"{dst_host_same_srv_rate:.2f}", f"{dst_host_diff_srv_rate:.2f}",
            f"{dst_host_same_src_port_rate:.2f}", f"{dst_host_serror_rate:.2f}", f"{dst_host_srv_serror_rate:.2f}",
            f"{dst_host_rerror_rate:.2f}", f"{dst_host_srv_rerror_rate:.2f}"]

        # Convert the result to a comma-separated string without brackets or quotes
        result_str = ','.join(map(str, result))
        print(result_str)


# Ask the user to specify the network interface
interface = input("Please enter the network interface you want to use (e.g., en0): ")

# Start sniffing and processing packets in real-time
print(f"Capturing packets on interface {interface}")
sniff(iface=interface, prn=process_packet, store=False)  # store=False means we don't keep the packets in memory
