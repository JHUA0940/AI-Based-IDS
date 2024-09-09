import os
import pickle
import numpy as np
import pandas as pd
from scapy.all import sniff, IP, TCP, UDP, ICMP
import time
from collections import defaultdict
from sklearn.exceptions import NotFittedError
import socket
from datetime import datetime
import netifaces

# Function to get the IP address of the default network interface
def get_interface_ip():
    """
    Returns the actual IP address of the network interface by creating
    a dummy socket connection.
    """
    try:
        # Create a dummy socket connection to an external address to get the IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Use Google's public DNS server to get an external connection (no actual connection made)
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print(f"Error getting interface IP: {e}")
        return None

# Get the IP address of the network interface
interface_ip = get_interface_ip()
print('interface ip: '+interface_ip)
if not interface_ip:
    print("Could not determine interface IP.")
    exit(1)

# Set the path relative to the script's directory
path = os.path.dirname(os.path.abspath(__file__))

print('load AI model')
# Load trained models and standardization tools
with open(os.path.join(path, 'model.pkl'), 'rb') as model_file:
    loaded_model = pickle.load(model_file)

with open(os.path.join(path, 'scalar.pkl'), 'rb') as scalar_file:
    scalar = pickle.load(scalar_file)

with open(os.path.join(path, 'protocol_type_le.pkl'), 'rb') as proto_file:
    protocol_type_le = pickle.load(proto_file)

with open(os.path.join(path, 'service_le.pkl'), 'rb') as service_file:
    service_le = pickle.load(service_file)

with open(os.path.join(path, 'flag_le.pkl'), 'rb') as flag_file:
    flag_le = pickle.load(flag_file)

# Track connection statistics
connection_info = defaultdict(lambda: {
    'count': 0, 'serror_count': 0, 'rerror_count': 0, 'same_srv_count': 0, 'diff_srv_count': 0, 'srv_count': 0
})
dst_host_info = defaultdict(lambda: {'count': 0, 'srv_count': 0, 'serror_count': 0})

# Start time to calculate duration
start_time = time.time()

# Dictionary to map common port numbers to services
service_mapping = {
    80: "http", 443: "http", 21: "ftp", 22: "ssh", 25: "smtp",
    110: "pop3", 143: "imap4", 23: "telnet", 20: "ftp_data"
}

# Protocol type mapping
protocol_type_mapping = {6: 'tcp', 17: 'udp', 1: 'icmp'}

# TCP flag mapping
flag_mapping = {
    'S': 'S0', 'SA': 'S1', 'SF': 'SF', 'REJ': 'REJ', 'RSTO': 'RSTO', 'RSTOS0': 'RSTOS0',
    'RSTR': 'RSTR', 'S2': 'S2', 'S3': 'S3', 'SH': 'SH', 'default': 'OTH'
}

# Initialize a counter for consecutive abnormal predictions
abnormal_counter = 0
ABNORMAL_THRESHOLD = 50  # Number of consecutive anomalies required for a warning

# Time tracking for normal traffic reminders
last_normal_traffic_time = time.time()

def get_flag(packet):
    if TCP in packet:
        flags = packet[TCP].flags
        if flags & 0x02:
            return flag_mapping['S']
        elif flags & 0x12:
            return flag_mapping['SA']
        elif flags & 0x10:
            return 'S1'
        elif flags & 0x14:
            return flag_mapping['RSTO']
        elif flags & 0x01:
            return flag_mapping['REJ']
        elif flags & 0x11:
            return flag_mapping['SF']
        elif flags & 0x18:
            return flag_mapping['S2']
        else:
            return flag_mapping.get('default', 'OTH')
    return 'OTH'

def safe_transform(label_encoder, value):
    """Safely transform labels using LabelEncoder and handle unknown labels."""
    try:
        return label_encoder.transform([value])[0]
    except ValueError:
        try:
            return label_encoder.transform(['other'])[0]
        except ValueError:
            return 0

print('start detection')
def process_packet(packet):
    global abnormal_counter, last_normal_traffic_time

    # Skip packets from the local IP address
    if IP in packet and packet[IP].src == interface_ip:
        return

    # Initialize all the fields to default values (zeros) to ensure 14 features
    default_feature_values = [0] * 14
    dport = None
    wrong_fragment = 0
    urgent = 0

    try:
        # Calculate dynamic features from packet if possible
        if IP in packet:
            protocol = packet[IP].proto
            protocol_type = protocol_type_mapping.get(protocol, "other")

            if protocol_type == 'tcp' and TCP in packet:
                dport = packet[TCP].dport
                service = service_mapping.get(dport, "private")
                flag = get_flag(packet)
                # Compute wrong_fragment and urgent
                wrong_fragment = 1 if packet[TCP].flags & 0x08 else 0
                urgent = 1 if packet[TCP].flags & 0x20 else 0
            elif protocol_type == 'udp' and UDP in packet:
                dport = packet[UDP].dport
                service = service_mapping.get(dport, "private")
                flag = "SF"
            elif protocol_type == 'icmp' and ICMP in packet:
                service = "eco_i"
                flag = "OTH"
            else:
                service = "other"
                flag = "OTH"

            if dport is None:
                dport = 0  # Assign a default value to avoid errors

            # Calculate other basic fields
            duration = time.time() - start_time
            src_bytes = len(packet[IP].payload) if IP in packet else 0
            dst_bytes = len(packet[IP].payload) if IP in packet else 0

            # Update the default feature list with computed values
            default_feature_values[0] = duration  # duration
            default_feature_values[1] = safe_transform(protocol_type_le, protocol_type)  # protocol_type
            default_feature_values[2] = safe_transform(service_le, service)  # service
            default_feature_values[3] = safe_transform(flag_le, flag)  # flag
            default_feature_values[4] = src_bytes  # src_bytes
            default_feature_values[5] = dst_bytes  # dst_bytes
            default_feature_values[6] = wrong_fragment  # wrong_fragment
            default_feature_values[7] = urgent  # urgent

            # Update connection and destination host statistics
            connection_key = (packet[IP].src, packet[IP].dst, dport)
            conn = connection_info[connection_key]
            conn['count'] += 1
            conn['srv_count'] += 1 if service == "private" else 0

            dst_host = packet[IP].dst
            dst_host_conn = dst_host_info[dst_host]
            dst_host_conn['count'] += 1
            dst_host_conn['srv_count'] += 1 if service == "private" else 0

            # Calculate statistics
            srv_diff_host_rate = conn['diff_srv_count'] / conn['count'] if conn['count'] > 0 else 0
            dst_host_srv_diff_host_rate = srv_diff_host_rate
            dst_host_srv_serror_rate = dst_host_conn['serror_count'] / dst_host_conn['srv_count'] if dst_host_conn[
                                                                                                         'srv_count'] > 0 else 0

            # Fill statistics into the feature vector
            default_feature_values[8:14] = [
                conn['count'], conn['srv_count'], srv_diff_host_rate, dst_host_conn['count'],
                dst_host_srv_diff_host_rate, dst_host_srv_serror_rate
            ]

            # Ensure all 14 features are accounted for
            features = pd.DataFrame([default_feature_values], columns=[
                'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
                'wrong_fragment', 'urgent', 'count', 'srv_count', 'srv_diff_host_rate', 'dst_host_count',
                'dst_host_srv_diff_host_rate', 'dst_host_srv_serror_rate'
            ])

            try:
                # Standardize features
                features_scaled = scalar.transform(features)

                # Make prediction using the trained model
                prediction = loaded_model.predict(features_scaled)

                # Check prediction and update the abnormal counter
                if prediction == 1:
                    abnormal_counter += 1
                    if abnormal_counter >= ABNORMAL_THRESHOLD:
                        # Output network flow information
                        src_ip = packet[IP].src if IP in packet else "unknown"
                        dst_ip = packet[IP].dst if IP in packet else "unknown"
                        protocol = protocol_type_mapping.get(packet[IP].proto, "unknown")
                        print(f"Abnormal traffic detected! Threshold met.")
                        print(f"Source IP: {src_ip}, Destination IP: {dst_ip}, Protocol: {protocol}, Service: {service}, Port: {dport}")
                        abnormal_counter = 0  # Reset counter after alert
                else:
                    # If normal traffic and 10 seconds have passed, print the message
                    current_time = time.time()
                    if current_time - last_normal_traffic_time >= 10:
                        print(f"Normal traffic. Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        last_normal_traffic_time = current_time
                    abnormal_counter = 0  # Reset counter if normal traffic

            except NotFittedError:
                print("Scaler or model is not properly fitted. Skipping detection.")
            except Exception as e:
                print(f"Error during detection: {e}")

    except Exception as e:
        print(f"Error processing packet: {e}")

# Set up the packet sniffing
sniff(prn=process_packet, store=0)
