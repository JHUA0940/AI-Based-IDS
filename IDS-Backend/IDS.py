import scapy.all as scapy
import time

# Define a global variable to store the session start time
start_time = {}


# Packet processing function
def process_packet(packet):
    try:
        # Extract basic network traffic features
        if packet.haslayer(scapy.IP):
            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst
            protocol = packet[scapy.IP].proto  # Protocol number
            length = len(packet)

            # If it's a TCP/UDP packet, extract additional information
            src_port = packet[scapy.TCP].sport if packet.haslayer(scapy.TCP) else (
                packet[scapy.UDP].sport if packet.haslayer(scapy.UDP) else None)
            dst_port = packet[scapy.TCP].dport if packet.haslayer(scapy.TCP) else (
                packet[scapy.UDP].dport if packet.haslayer(scapy.UDP) else None)
            flag = packet.sprintf("%TCP.flags%") if packet.haslayer(scapy.TCP) else None

            # Record the session start time
            key = (src_ip, dst_ip)
            if key not in start_time:
                start_time[key] = time.time()

            duration = time.time() - start_time[key]  # Duration of the session

            # Print features similar to the NSL-KDD dataset
            print(
                f"Duration: {duration}, Protocol: {protocol}, Src_IP: {src_ip}, Dst_IP: {dst_ip}, Src_Port: {src_port}, Dst_Port: {dst_port}, Length: {length}, Flag: {flag}")

    except Exception as e:
        # If there is an error processing the packet, print the error
        print(f"Error processing packet: {e}")


# Use scapy to sniff network traffic
def start_sniffing():
    print("Starting to capture network traffic...")
    scapy.sniff(prn=process_packet, store=False)


if __name__ == "__main__":
    start_sniffing()
