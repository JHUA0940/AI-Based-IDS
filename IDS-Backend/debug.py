import pandas as pd

# Load the data without header
data_Train = pd.read_csv('KDDTrain+.txt', header=None)

# Set column names for the dataset (ensure this list matches the number of columns in the data)
columns = (
    ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent',
     'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root',
     'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
     'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
     'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
     'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
     'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
     'dst_host_srv_rerror_rate', 'attack', 'outcome'])

# Ensure the number of columns matches
if len(columns) != data_Train.shape[1]:
    raise ValueError(
        f"Length mismatch: Expected axis has {data_Train.shape[1]} elements, new values have {len(columns)} elements")

data_Train.columns = columns

# Drop the 'outcome' column as it is not required
data_Train.drop(columns='outcome', axis=1, inplace=True)

# Drop the specified columns from the dataset, including 'dst_host_same_src_port_rate'
data_Train.drop(columns=[
    'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
    'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files',
    'num_outbound_cmds', 'is_host_login', 'is_guest_login', 'dst_host_same_src_port_rate', 'land'
], axis=1, inplace=True)

# Get the remaining features after drop
features = data_Train.drop(columns=['attack']).columns.tolist()
print(f"Number of features: {len(features)}")
print("Features used for training:", features)
