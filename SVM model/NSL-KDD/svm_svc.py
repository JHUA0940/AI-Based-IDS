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
# Standardize data processing
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
# Evaluate model performance metrics
from sklearn.model_selection import train_test_split
# Dataset partitioning
import seaborn as sns
# Provide visualization capabilities
from sklearn.preprocessing import LabelEncoder
# Encode categorical data
from sklearn.model_selection import GridSearchCV
import matplotlib.gridspec as gridspec

data_Train = pd.read_csv('KDDTrain+.txt')
data_Train.columns
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
data_Train.isnull().sum()
# Delete the 'outcome' column from the data_Train dataset
data_Train.drop(columns='outcome', axis=1, inplace=True)

attack_n = []
for i in data_Train.attack:
    # Convert attack types to standardized strings
    if i == 'normal':
        attack_n.append("normal")
    else:
        attack_n.append("attack")
# Assign the converted attack type list back to the corresponding column in the original dataset
data_Train['attack'] = attack_n

# Select all columns in the dataset that are of type 'object' and return their names
data_obj = data_Train.select_dtypes(['object']).columns
# Calculate and return the count of occurrences of each label in the "attack" column of the training dataset
data_Train["attack"].value_counts()

# LabelEncoder is used to convert categorical label data into numerical format, which is easier for machine learning models to process
from sklearn.preprocessing import LabelEncoder

# Initialize a LabelEncoder instance for handling the protocol_type field
protocol_type_le = LabelEncoder()
# Initialize a LabelEncoder instance for handling the service field
service_le = LabelEncoder()
# Initialize a LabelEncoder instance for handling the flag field
flag_le = LabelEncoder()

# 1. Encode the 'protocol_type' feature using LabelEncoder
data_Train['protocol_type'] = protocol_type_le.fit_transform(data_Train['protocol_type'])
# 2. Encode the 'service' feature using LabelEncoder
data_Train['service'] = service_le.fit_transform(data_Train['service'])
# 3. Encode the 'flag' feature using LabelEncoder
data_Train['flag'] = flag_le.fit_transform(data_Train['flag'])

attack_n = []
for i in data_Train.attack:
    # Iterate through the attack types and label 'normal' as 0, and other types as 1
    if i == 'normal':
        attack_n.append(0)
    else:
        attack_n.append(1)
# Add the processed attack type data to the data_Train dataset
data_Train['attack'] = attack_n
data_Train['attack'].value_counts()

# Split the dataset into training and test sets
y = data_Train['attack'].copy()  # Copy the target variable (attack type) into y
x = data_Train.drop(['attack'], axis=1)  # Remove the target variable from the dataset to obtain the feature matrix x

# Use the train_test_split function to divide the training set and the test set
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=40)

# Import StandardScaler to standardize data
from sklearn.preprocessing import StandardScaler

# Initialize the StandardScaler object
scalar = StandardScaler()

# Apply standardization to the x_train dataset
x_train = scalar.fit_transform(x_train)

# Apply the same standardization to the x_test dataset
x_test = scalar.fit_transform(x_test)

lin_svc = svm.LinearSVC().fit(x_train, y_train)  # Train a linear support vector machine model
Y_pred = lin_svc.predict(x_test)  # Use the trained model to predict the test set
print('The Training accuracy = ', lin_svc.score(x_train, y_train))  # Print the training accuracy
print('The Testing accuracy = ', lin_svc.score(x_test, y_test))  # Print the testing accuracy
print("------------------------------------------------")
# Calculate and print the prediction accuracy of the linear SVC model
print("linearSVC accuracy : " + str(np.round(accuracy_score(y_test, Y_pred), 3)))
