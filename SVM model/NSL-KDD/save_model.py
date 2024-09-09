import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
import matplotlib.gridspec as gridspec
import joblib  # For saving and loading the model
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
attack_n = []
for i in data_Train.attack:
    if i == 'normal':
        attack_n.append("normal")
    else:
        attack_n.append("attack")
data_Train['attack'] = attack_n

# Encode categorical variables 'protocol_type', 'service', and 'flag'
protocol_type_le = LabelEncoder()
service_le = LabelEncoder()
flag_le = LabelEncoder()
data_Train['protocol_type'] = protocol_type_le.fit_transform(data_Train['protocol_type'])
data_Train['service'] = service_le.fit_transform(data_Train['service'])
data_Train['flag'] = flag_le.fit_transform(data_Train['flag'])

# Convert the 'attack' column to binary labels (0 for 'normal', 1 for 'attack')
attack_n = []
for i in data_Train.attack:
    if i == 'normal':
        attack_n.append(0)
    else:
        attack_n.append(1)
data_Train['attack'] = attack_n

# Split the dataset into features (x) and target (y)
y = data_Train['attack'].copy()  # Target variable
x = data_Train.drop(['attack'], axis=1)  # Feature set
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=40)

# Standardize the data
from sklearn.preprocessing import StandardScaler
scalar = StandardScaler()
x_train = scalar.fit_transform(x_train)
x_test = scalar.transform(x_test)

# Train a linear SVM model
lin_svc = svm.LinearSVC().fit(x_train, y_train)

with open('model.pkl', 'wb') as file:
    pickle.dump(lin_svc, file)

with open('model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)


# Use the loaded model to make predictions on the test set
Y_pred = loaded_model.predict(x_test)

# Print model performance
print('The Training accuracy = ', loaded_model.score(x_train, y_train))
print('The Testing accuracy = ', loaded_model.score(x_test, y_test))
print("------------------------------------------------")
print("linearSVC accuracy : " + str(np.round(accuracy_score(y_test, Y_pred), 3)))
