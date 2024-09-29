import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
import pickle
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

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
    raise ValueError(f"Length mismatch: Expected axis has {data_Train.shape[1]} elements, new values have {len(columns)} elements")

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

# Drop the specified columns but keep 'wrong_fragment' and 'urgent'
data_Train.drop(columns=[
    'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root',
    'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login', 'is_guest_login',
    'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
    'same_srv_rate', 'diff_srv_rate', 'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
    'dst_host_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'dst_host_same_src_port_rate', 'land'
], axis=1, inplace=True)

# Split the dataset into features (x) and target (y)
y = data_Train['attack']  # Target variable
x = data_Train.drop(['attack'], axis=1)  # Feature set

# Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=40)

# Standardize the data
scalar = StandardScaler()
x_train = scalar.fit_transform(x_train)
x_test = scalar.transform(x_test)

# Print the number of values used for training
num_samples, num_features = x_train.shape
total_values = num_samples * num_features
print(f"Total number of values used for training: {total_values}")

# Print the features used for training
features_used = x.columns
print("Features used for training:", features_used)

# Hyperparameter tuning for the Linear SVM model
param_grid = {
    'C': [0.1, 1, 10, 100],
    'max_iter': [100, 500, 1000]
}
grid_search = GridSearchCV(svm.LinearSVC(), param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(x_train, y_train)

# Get the best model from grid search
best_model = grid_search.best_estimator_

# Save the trained model, encoders, and scaler
with open('model.pkl', 'wb') as model_file:
    pickle.dump(best_model, model_file)

with open('scalar.pkl', 'wb') as scalar_file:
    pickle.dump(scalar, scalar_file)

with open('protocol_type_le.pkl', 'wb') as proto_file:
    pickle.dump(protocol_type_le, proto_file)

with open('service_le.pkl', 'wb') as service_file:
    pickle.dump(service_le, service_file)

with open('flag_le.pkl', 'wb') as flag_file:
    pickle.dump(flag_le, flag_file)

# Make predictions and evaluate the model
y_pred = best_model.predict(x_test)
print('The Training accuracy = ', best_model.score(x_train, y_train))
print('The Testing accuracy = ', best_model.score(x_test, y_test))
print("------------------------------------------------")
print("LinearSVC accuracy: " + str(np.round(accuracy_score(y_test, y_pred), 3)))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
