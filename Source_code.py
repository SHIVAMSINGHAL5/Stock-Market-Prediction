# -*- coding: utf-8 -*-
"""stock market.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f-St051oHFt52DfgKKtv8A_JUF59sN1U

**Data Import**
"""

!pip install yfinance
!pip install finta
!pip install catboost

import math
import datetime
import numpy as np
import pandas as pd
from finta import TA
import yfinance as yf
from sklearn import svm
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from xgboost import XGBClassifier
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier 
from sklearn.metrics import confusion_matrix, classification_report, mean_squared_error, accuracy_score
from catboost import CatBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier

"""**Data Collection and Processing**"""

date_range = 10000
gap = '1d'
symbol = 'AAPL'      
INDICATORS = ['RSI', 'MACD', 'STOCH','ADL', 'ATR', 'MOM', 'MFI', 'ROC', 'OBV', 'CCI', 'EMV', 'VORTEX']

start = (datetime.date.today() - datetime.timedelta( date_range ) )
end = datetime.datetime.today()

data = yf.download(symbol, start=start, end=end, interval=gap)
data.rename(columns={"Close": 'close', "High": 'high', "Low": 'low', 'Volume': 'volume', 'Open': 'open'}, inplace=True)
print(len(data))

tmp = data.iloc[-60:]
tmp['close'].plot()

def smooth(data, alpha):
    return data.ewm(alpha=alpha).mean()

data = smooth(data, 0.75)
tmp1 = data.iloc[-60:]
tmp1['close'].plot()

""" **Feature Engineering**"""

def feature_eng(data):

    for indicator in INDICATORS:
        ind_data = eval('TA.' + indicator + '(data)')
        if not isinstance(ind_data, pd.DataFrame):
            ind_data = ind_data.to_frame()
        data = data.merge(ind_data, left_index=True, right_index=True)
    data.rename(columns={"14 period EMV.": '14 period EMV'}, inplace=True)
    data['ema50'] = data['close'] / data['close'].ewm(50).mean()
    data['ema21'] = data['close'] / data['close'].ewm(21).mean()
    data['ema15'] = data['close'] / data['close'].ewm(14).mean()
    data['ema5'] = data['close'] / data['close'].ewm(5).mean()
    data['normVol'] = data['volume'] / data['volume'].ewm(5).mean()
    del (data['open'])
    del (data['high'])
    del (data['low'])
    del (data['volume'])
    del (data['Adj Close'])
    return data

data = feature_eng(data)
print(data.columns)

live_pred_data = data.iloc[-16:-11]
def predi(data, window):
    prediction = (data.shift(-window)['close'] >= data['close'])
    prediction = prediction.iloc[:-window]
    data['pred'] = prediction.astype(int)
    return data

data = predi(data, window=15)
#del (data['close'])
data = data.dropna()
data.tail()
print(len(data))

"""**Building the Ensemble Model**"""

count = 0
total = 0
num_train = 10
len_train = 40
rf_RESULTS = []
knn_RESULTS = []
#cat_RESULTS = []
xg_RESULTS = []
gb_RESULTS = []
ensemble_RESULTS = []

i = 0

rf = RandomForestClassifier()
knn = KNeighborsClassifier()
#xg = XGBClassifier()
#cat = CatBoostClassifier()
gb= GradientBoostingClassifier()
estimators=[('knn', knn), ('rf', rf) , ('gb',gb) ]
ensemble = VotingClassifier(estimators, voting='soft')

while True:
    df = data.iloc[i * num_train : (i * num_train) + len_train]
    i += 1
    if len(df) < 40:
        break
    y = df['pred']
    features = [x for x in df.columns if x not in ['pred']]
    X = df[features]
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size= 0.8 ,shuffle = False)
    
    rf.fit(X_train, y_train)
    rf_prediction = rf.predict(X_test)
    rf_accuracy = accuracy_score(y_test.values, rf_prediction)
    rf_RESULTS.append(rf_accuracy)

    knn.fit(X_train, y_train)
    knn_prediction = knn.predict(X_test)
    knn_accuracy = accuracy_score(y_test.values, knn_prediction)
    knn_RESULTS.append(knn_accuracy)
    try:
      gb.fit(X_train, y_train)
      gb_prediction = gb.predict(X_test)
    except:
      total+=1
      continue
    gb_accuracy = accuracy_score(y_test.values, gb_prediction)
    gb_RESULTS.append(gb_accuracy)
    ensemble.fit(X_train, y_train)
    ensemble_prediction = ensemble.predict(X_test)
    ensemble_accuracy = accuracy_score(y_test.values, ensemble_prediction)
    ensemble_RESULTS.append(ensemble_accuracy)
    count+=1
    """ try:
      
      xg.fit(X_train, y_train)
      xg_prediction = xg.predict(X_test)
      gb_accuracy = accuracy_score(y_test.values, xg_prediction)
      xg_RESULTS.append(xg_accuracy)
      per_X_train = X_train
      per_y_train = y_train

      

    except:
      if 'per_X_train' in locals():
        gb.fit(per_X_train, per_y_train)
        ensemble.fit(per_X_train, per_y_train)
        ensemble_prediction = ensemble.predict(X_test)
        ensemble_accuracy = accuracy_score(y_test.values, ensemble_prediction)
        ensemble_RESULTS.append(ensemble_accuracy)   
        count+=1
        
    cat.fit(X_train, y_train)
    cat_prediction = cat.predict(X_test)
    cat_accuracy = accuracy_score(y_test.values, cat_prediction)
    cat_RESULTS.append(cat_accuracy)
    """       

print('RF Accuracy = ' + str( sum(rf_RESULTS) / len(rf_RESULTS)))
print('KNN Accuracy = ' + str( sum(knn_RESULTS) / len(knn_RESULTS)))
#print('XG Accuracy = ' + str( sum(xg_RESULTS) / len(xg_RESULTS)))
#print('CAT Accuracy = ' + str( sum(cat_RESULTS) / len(cat_RESULTS)))
print('GB Accuracy = ' + str( sum(gb_RESULTS) / len(gb_RESULTS)))
print('ENSEMBLE Accuracy = ' + str( sum(ensemble_RESULTS) / len(ensemble_RESULTS)))

import pickle
pkl_filename = "ensemble.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(ensemble, file)

!gdown --id 11BF0tz9cvT4obG-voKWSmRLe9Ru9TN_M

pkl_filename = "ensemble.pkl"
with open(pkl_filename, 'rb') as file:
    ensemble = pickle.load(file)

"""**Results Prediction**"""

df = data.iloc[-200:]
y = df['pred']
features = [x for x in df.columns if x not in ['pred']]
X = df[features]
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size= 0.8 ,shuffle = False)
ensemble_prediction = ensemble.predict(X_test)
accuracy_score(y_test.values, ensemble_prediction)

"""**Confusion Matrix**"""

from sklearn.metrics import confusion_matrix
import seaborn as sns
cf_matrix = confusion_matrix(ensemble_prediction, y_test)
cf_matrix
sns.heatmap(cf_matrix, annot=True, cmap='Blues')

"""**Closing Price Prediction using LSTM**

**Importing and Reading the Dataset**
"""

!gdown --id 1xpvtmyzeG7BPvqxqI0qlq9qEzFyUOVu4

data = pd.read_csv('prices-split-adjusted.csv')
data.isnull().sum()
data = data.loc[(data['symbol'] == 'AAPL')]
data = data.drop(columns=['symbol'])
data = data[['date','open','close','low','volume','high']]
data

data.shape

"""**Plotting the Dataset**"""

plt.figure(figsize=(16,8))
plt.title('Closing Price of the Stock Historically')
plt.plot(data['close'])
plt.xlabel('Year', fontsize=20)
plt.ylabel('Closing Price Historically ($)', fontsize=20)
plt.show()

data = data.filter(['close'])
dataset = data.values

#Find out the number of rows that are present in this dataset in order to train our model.
training_data_len = math.ceil(len(dataset)* .9)
training_data_len
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)
scaled_data

train_data = scaled_data[0:training_data_len , :]
x_train = []
y_train = []

for j in range(60, len(train_data)):
    x_train.append(train_data[j-60:j,0])
    y_train.append(train_data[j,0])
    if j<=60:
        print(x_train)
        print(y_train)
        print()

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_train.shape

"""**Building The LSTM Model**"""

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape = (x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(x_train, y_train, batch_size=10, epochs=2)

test_data = scaled_data[training_data_len - 60: , :]
x_test = []
y_test = dataset[training_data_len:, :]

for j in range(60, len(test_data)):
    x_test.append(test_data[j-60:j, 0])
x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)
predictions

"""**RMSE Analysis**"""

rmse = np.sqrt( np.mean( (predictions - y_test)**2))
rmse

"""**Results Prediction**"""

train = data[:training_data_len]
val = data[training_data_len:]
val['Predictions'] = predictions

plt.figure(figsize=(16,8))
plt.title('LSTM Model Data')
plt.xlabel('Date', fontsize=16)
plt.ylabel('Close Price', fontsize=16)
plt.plot(train['close'])
plt.plot(val[['close', 'Predictions']])
plt.legend(['Trained Dataset', 'Actual Value', 'Predictions'])
plt.show()

































ensemble_prediction = 0

def cross_Validation(data):
    count = 0
    total = 0
    num_train = 10
    len_train = 40
    rf_RESULTS = []
    knn_RESULTS = []
    #cat_RESULTS = []
    xg_RESULTS = []
    gb_RESULTS = []
    ensemble_RESULTS = []
    
    i = 0
    
    rf = RandomForestClassifier()
    knn = KNeighborsClassifier()
    xg = XGBClassifier()
    #cat = CatBoostClassifier()
    gb= GradientBoostingClassifier()
    estimators=[('knn', knn), ('rf', rf) , ('xg',xg) ]
    ensemble = VotingClassifier(estimators, voting='hard')
    
    while True:
        df = data.iloc[i * num_train : (i * num_train) + len_train]
        i += 1
        if len(df) < 20:
            break
        y = df['pred']
        features = [x for x in df.columns if x not in ['pred']]
        X = df[features]
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size= 0.8,shuffle = False)
        rf.fit(X_train, y_train)
        rf_prediction = rf.predict(X_test)
        rf_accuracy = accuracy_score(y_test.values, rf_prediction)
        rf_RESULTS.append(rf_accuracy)

        knn.fit(X_train, y_train)
        knn_prediction = knn.predict(X_test)
        knn_accuracy = accuracy_score(y_test.values, knn_prediction)
        knn_RESULTS.append(knn_accuracy)
        
        xg.fit(X_train, y_train)
        xg_prediction = xg.predict(X_test)
        xg_accuracy = accuracy_score(y_test.values, xg_prediction)
        xg_RESULTS.append(xg_accuracy)
        ensemble.fit(X_train, y_train)
        ensemble_prediction = ensemble.predict(X_test)
        ensemble_accuracy = accuracy_score(y_test.values, ensemble_prediction)
        ensemble_RESULTS.append(ensemble_accuracy)
        """ try:
          
          gb.fit(X_train, y_train)
          gb_prediction = gb.predict(X_test)
          gb_accuracy = accuracy_score(y_test.values, gb_prediction)
          gb_RESULTS.append(gb_accuracy)
          per_X_train = X_train
          per_y_train = y_train

          

        except:
          if 'per_X_train' in locals():
            gb.fit(per_X_train, per_y_train)
            ensemble.fit(per_X_train, per_y_train)
            ensemble_prediction = ensemble.predict(X_test)
            ensemble_accuracy = accuracy_score(y_test.values, ensemble_prediction)
            ensemble_RESULTS.append(ensemble_accuracy)   
            count+=1
            
        cat.fit(X_train, y_train)
        cat_prediction = cat.predict(X_test)
        cat_accuracy = accuracy_score(y_test.values, cat_prediction)
        cat_RESULTS.append(cat_accuracy)
        """       
    
    print('RF Accuracy = ' + str( sum(rf_RESULTS) / len(rf_RESULTS)))
    print('KNN Accuracy = ' + str( sum(knn_RESULTS) / len(knn_RESULTS)))
    print('XG Accuracy = ' + str( sum(xg_RESULTS) / len(xg_RESULTS)))
    #print('CAT Accuracy = ' + str( sum(cat_RESULTS) / len(cat_RESULTS)))
    #print('GB Accuracy = ' + str( sum(gb_RESULTS) / len(gb_RESULTS)))
    print('ENSEMBLE Accuracy = ' + str( sum(ensemble_RESULTS) / len(ensemble_RESULTS)))
    return ensemble
    
ensemble = cross_Validation(data)