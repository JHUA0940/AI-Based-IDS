import numpy as np
# Provide efficient numerical calculations and array operations 所需的函数包
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
from sklearn. metrics import classification_report, confusion_matrix, accuracy_score
# evaluate model performance parameters
from sklearn. model_selection import train_test_split
# Dataset partitioning
import seaborn as sns
# Provide visualized results
from sklearn. preprocessing import LabelEncoder
# Encode categorical data
from sklearn.model_selection import GridSearchCV
import matplotlib.gridspec as gridspec
data_Train =pd.read_csv('KDDTrain+.txt')
# read datasets
data_Train.columns
columns = (['duration','protocol_type','service','flag','src_bytes','dst_bytes','land','wrong_fragment','urgent'
            ,'hot','num_failed_logins','logged_in','num_compromised','root_shell','su_attempted','num_root'
            ,'num_file_creations','num_shells','num_access_files','num_outbound_cmds','is_host_login'
            ,'is_guest_login','count','srv_count','serror_rate','srv_serror_rate','rerror_rate','srv_rerror_rate'
            ,'same_srv_rate','diff_srv_rate','srv_diff_host_rate','dst_host_count','dst_host_srv_count'
            ,'dst_host_same_srv_rate','dst_host_diff_srv_rate','dst_host_same_src_port_rate'
            ,'dst_host_srv_diff_host_rate','dst_host_serror_rate','dst_host_srv_serror_rate','dst_host_rerror_rate'
            ,'dst_host_srv_rerror_rate','attack','outcome'])
data_Train.columns=columns
#Replaced column names
data_Train.isnull().sum()
# Remove 'outcome' column from data_Train dataset , data cleansing
data_Train.drop(columns='outcome',axis=1, inplace=True )
attack_n = []
for i in data_Train.attack :
  # 将攻击类型转换为标准化的字符串
  if i == 'normal':
    attack_n.append("normal")
  else:
    attack_n.append("attack")
# 将转换后的攻击类型列表赋值回原数据集的对应列
data_Train['attack'] = attack_n
data_Train['attack'].value_counts()
pro_t = data_Train['protocol_type']
pro_count = Counter(pro_t)
udp_Num= pro_count['udp']
tcp_Num= pro_count['tcp']
icmp_Num= pro_count['icmp']
categories = ['udp','tcp','icmp']
counts = [udp_Num,tcp_Num,icmp_Num]
plt.bar(categories,counts)
plt.title('protocol_type Counts')
plt.xlabel('Type')
plt.ylabel('count')
plt.show()