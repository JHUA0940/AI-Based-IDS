import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import pickle

# Load the data
data_Train = pd.read_csv('KDDTrain+.txt')

# Set column names for the dataset
columns = (
    ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent',
     'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root',
     'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
     'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
     'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
     'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
     'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
     'dst_host_srv_rerror_rate', 'attack', 'outcome'])
data_Train.columns = columns

# Drop the 'outcome' column as it is not required
data_Train.drop(columns='outcome', axis=1, inplace=True)

# Convert the 'attack' column into 'normal' and 'attack' categories
data_Train['attack'] = data_Train['attack'].apply(lambda x: 0 if x == 'normal' else 1)

# Encode categorical variables 'protocol_type', 'service', and 'flag'
protocol_type_le = LabelEncoder()
service_le = LabelEncoder()
flag_le = LabelEncoder()

data_Train['protocol_type'] = protocol_type_le.fit_transform(data_Train['protocol_type'])
data_Train['service'] = service_le.fit_transform(data_Train['service'])
data_Train['flag'] = flag_le.fit_transform(data_Train['flag'])

# Split the dataset into features (x) and target (y)
y = data_Train['attack']  # Target variable
x = data_Train.drop(['attack'], axis=1)  # Feature set
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=40)

# Standardize the data
scalar = StandardScaler()
x_train = scalar.fit_transform(x_train)
x_test = scalar.transform(x_test)

# Train a linear SVM model
lin_svc = svm.LinearSVC(max_iter=10000).fit(x_train, y_train)

# Save the trained model, encoders, and scaler
with open('model.pkl', 'wb') as model_file:
    pickle.dump(lin_svc, model_file)

with open('scalar.pkl', 'wb') as scalar_file:
    pickle.dump(scalar, scalar_file)

with open('protocol_type_le.pkl', 'wb') as proto_file:
    pickle.dump(protocol_type_le, proto_file)

with open('service_le.pkl', 'wb') as service_file:
    pickle.dump(service_le, service_file)

with open('flag_le.pkl', 'wb') as flag_file:
    pickle.dump(flag_le, flag_file)

# Evaluate the model
y_pred = lin_svc.predict(x_test)
print(f"Training accuracy: {lin_svc.score(x_train, y_train):.3f}")
print(f"Testing accuracy: {lin_svc.score(x_test, y_test):.3f}")
