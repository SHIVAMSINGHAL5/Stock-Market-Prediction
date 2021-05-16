# Stock-Market-Prediction Using ML Algorithms

The stock market prediction system proposed in this paper emphasises on using an ensemble model to make accurate predictions. While an individual algorithm-based model might have higher accuracy, however, an ensemble model boosts the overall confidence and reliability of the system. The proposed system has the following characteristics:

**1. Buy/sell decision for stocks** 
   
   A combination of Random Forest classifier, K-Nearest Neighbours classifier, and Gradient Boosting classifier forms an ensemble model which predicts whether an investor should buy/sell stocks on a particular day.

**2. Closing price prediction**
   
  An LSTM model predicts the closing prices of the stock using historical datasets. The general stock direction trends can also be extracted from the dataset to predict the future behaviour of the stocks.

## Index

## Installation

## Architecture


Data Processing Module :

Data Import:
yfinance API is used to collect the historical stock data.  
Libraries such as numpy, pandas, and FINTA are used.

Data Collection:
The stock data is retrieved for the specified number of days for a specified company.
A list of technical indicators extracted from the FINTA library are used to generate more features.
The closing prices column of the dataset is plotted.

Data Smoothening and Plotting:
The plotted dataset has a lot of troughs and spikes which makes it difficult to make predictions or observe the trends.
The data is exponentially smoothened to make it easier to compute the technical indicators.

Feature Engineering Module:
The feature engineering module is used to engineer the following features:
'close‘
'14 period RSI',
'14 period STOCH %K',
'14 period ATR', 
'14 period MFI', 
'20 period CCI', 
'14 period EMV', 
'ema50', 'ema21', 'ema15', 'ema5', 'normVol'


 Ensemble Model Building:
 The following algorithms are utilized to form an ensemble model:
Random Forest (RF)
K-Nearest Neighbor (KNN)
Gradient Boosting (GB)

 LSTM Model Building:

Following the processing of data, the dataset is plotted for depicting the closing prices of the historical stock data.
An LSTM model is trained on this historical stock data.
After building the LSTM model, an RMSE analysis is done to check the deviations between the actual and predicted prices.



 Results Prediction:
The ensemble model along with the LSTM model predicts the buy/sell call, closing prices, and stock trend.
A confusion matrix is generated which shows the accuracy of the tested data.
The RMSE value depicts the deviation between the actual and predicted prices.


