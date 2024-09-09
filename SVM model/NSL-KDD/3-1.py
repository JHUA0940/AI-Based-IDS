import numpy as np
# Provide efficient numerical calculations and array operations
import pandas as pd
# Provide functions for data processing and analysis
from pandas import Timestamp
# Used for processing timestamps
from collections import Counter
import matplotlib.pyplot as plt
# Provide data visualization functionality
from sklearn import svm
# Support Vector Machine Algorithm
from sklearn.svm import SVC
# SVC is a support vector classifier
from sklearn.preprocessing import MinMaxScaler
# In order to standardize data processing
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
# Evaluate model performance parameters
from sklearn.model_selection import train_test_split
# Dataset partitioning
import seaborn as sns
# Provide visualized results
from sklearn.preprocessing import LabelEncoder
# Encode categorical data
from sklearn.model_selection import GridSearchCV
import matplotlib.gridspec as gridspec
data_Train = pd.read_csv('KDDTrain+.txt')
data_Train.columns
columns = (['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent',
            'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root',
            'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
            'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
            'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
            'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
            'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
            'dst_host_srv_rerror_rate', 'attack', 'outcome'])
data_Train.columns = columns
data_Train.isnull().sum()
# Drop the 'outcome' column from the data_Train dataset
data_Train.drop(columns='outcome', axis=1, inplace=True)

attack_n = []
for i in data_Train.attack:
    # Convert the attack types into standardized strings
    if i == 'normal':
        attack_n.append("normal")
    else:
        attack_n.append("attack")
# Assign the converted attack types list back to the corresponding column in the original dataset
data_Train['attack'] = attack_n
data_Train['attack'].value_counts()
# Select all columns in the dataset that are of type 'object' and return their column names
data_obj = data_Train.select_dtypes(['object']).columns
# Count and return the occurrences of each label in the "attack" column of the training dataset
data_Train["attack"].value_counts()
# LabelEncoder is used to convert categorical label data into numerical data for machine learning models to process
from sklearn.preprocessing import LabelEncoder

# Initialize a LabelEncoder instance for handling the protocol_type field
protocol_type_le = LabelEncoder()
# Initialize a LabelEncoder instance for handling the service field
service_le = LabelEncoder()
# Initialize a LabelEncoder instance for handling the flag field
flag_le = LabelEncoder()

# 1. Use LabelEncoder to encode the 'protocol_type' feature
data_Train['protocol_type'] = protocol_type_le.fit_transform(data_Train['protocol_type'])
# 2. Use LabelEncoder to encode the 'service' feature
data_Train['service'] = service_le.fit_transform(data_Train['service'])
# 3. Use LabelEncoder to encode the 'flag' feature
data_Train['flag'] = flag_le.fit_transform(data_Train['flag'])

attack_n = []
for i in data_Train.attack:
    # Iterate through the attack types, marking 'normal' as 0 and other types as 1
    if i == 'normal':
        attack_n.append(0)
    else:
        attack_n.append(1)
# Add processed attack type data to the data_Train dataset
data_Train['attack'] = attack_n
data_Train['attack'].value_counts()

# Create a 30x30 canvas
plt.figure(figsize=(30,30))
# Heatmap to show correlations in the datasets
sns.heatmap(data_Train.corr(), annot=True, cmap='mako')
plt.show()
