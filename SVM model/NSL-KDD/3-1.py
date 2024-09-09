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
data_Train.isnull().sum()
# 从data_Train数据集中删除'outcome'列
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
# 选择数据集中所有类型为'object'的列，并返回它们的列名
data_obj = data_Train.select_dtypes(['object']).columns
# 计算并返回训练数据集中“attack”列中各标签的出现次数
data_Train["attack"].value_counts()
# LabelEncoder用于将类别型标签数据转换为数值型，便于机器学习模型处理
from sklearn.preprocessing import LabelEncoder

# 初始化用于处理protocol_type字段的LabelEncoder实例
protocol_type_le = LabelEncoder()
# 初始化用于处理service字段的LabelEncoder实例
service_le = LabelEncoder()
# 初始化用于处理flag字段的LabelEncoder实例
flag_le = LabelEncoder()

# 1. 使用LabelEncoder对'protocol_type'特征进行编码
data_Train['protocol_type'] = protocol_type_le.fit_transform(data_Train['protocol_type'])
# 2. 使用LabelEncoder对'service'特征进行编码
data_Train['service'] = service_le.fit_transform(data_Train['service'])
# 3. 使用LabelEncoder对'flag'特征进行编码
data_Train['flag'] = flag_le.fit_transform(data_Train['flag'])

attack_n = []
for i in data_Train.attack :
  # Iterate through the attack types, marking 'normal' as 0 and other types as 1
  if i == 'normal':
    attack_n.append(0)
  else:
    attack_n.append(1)
# Add processed attack type data to data_Train dataset
data_Train['attack'] = attack_n
data_Train['attack'].value_counts()

# create 30* 30 canvas
plt.figure(figsize=(30,30))
# Heat mapping to show correlations in data sets
sns.heatmap(data_Train.corr(), annot= True,cmap='mako')
plt.show()

















