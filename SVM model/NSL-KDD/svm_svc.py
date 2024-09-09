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
  # 遍历攻击类型，将'normal'标记为0，其他类型标记为1
  if i == 'normal':
    attack_n.append(0)
  else:
    attack_n.append(1)
# 将处理后的攻击类型数据添加到data_Train数据集中
data_Train['attack'] = attack_n
data_Train['attack'].value_counts()

#将数据集划分为训练集和测试集
y = data_Train['attack'].copy()  # 复制目标变量（攻击类型）到y
x = data_Train.drop(['attack'], axis=1)  # 从数据集中移除目标变量，得到特征矩阵x

# 使用train_test_split函数划分训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(x,y , test_size=0.3, random_state=40)

# 导入StandardScaler类以实现数据的标准化处理
from sklearn.preprocessing import StandardScaler

# 初始化StandardScaler对象
scalar=StandardScaler()

# 对训练数据集x_train进行标准化处理
x_train=scalar.fit_transform(x_train)

# 对测试数据集x_test应用相同的标准化处理
x_test = scalar.fit_transform(x_test)

lin_svc = svm.LinearSVC().fit(x_train, y_train)  # 训练线性支持向量机模型
Y_pred = lin_svc.predict(x_test)  # 使用训练好的模型对测试集进行预测
print('The Training accuracy = ', lin_svc.score(x_train, y_train))  # 打印训练集的准确率
print('The Testing accuracy = ', lin_svc.score(x_test, y_test))  # 打印测试集的准确率
print("------------------------------------------------")
# 计算并打印线性SVC模型的预测准确率
print( "linearSVC accuracy : " + str(np.round(accuracy_score(y_test,Y_pred),3)))




