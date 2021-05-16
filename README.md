# Stock-Market-Prediction Using ML Algorithms

This stock market prediction system emphasises on using an ensemble model to make accurate stock price predictions. While an individual algorithm-based model might have higher accuracy, however, an ensemble model boosts the overall confidence and reliability of the system. The system has the following characteristics:

**1. Buy/sell decision for stocks** 
   
   A combination of Random Forest classifier, K-Nearest Neighbours classifier, and Gradient Boosting classifier forms an ensemble model which predicts whether an investor should buy/sell stocks on a particular day.

**2. Closing price prediction**
   
  An LSTM model predicts the closing prices of the stock using historical datasets. The general stock direction trends can also be extracted from the dataset to predict the future behaviour of the stocks.

## Index
* [Index](#Index)
* [Installation](#Installation)
* [Datasets used](#Datasets-used)
* [Architecture](#Architecture)
* [Models used for implementation](#Models-used-for-implementation)
* [Ensemble Model](#Ensemble-model)
* [LSTM Model](#LSTM-model)
* [Results](#Results)
* [Publication](#Publication)
* [Project Organization](#Project-Organization)

## Installation
Prerequisites:
```
1. Jupyter Notebook
2. Python
```
Install the libraries using the following commands:
```
!pip install yfinance
!pip install finta
!pip install keras
!pip install sklearn
```
Run the project using the following command:
```
```
## Datasets used

Historical stock [dataset](https://github.com/SHIVAMSINGHAL5/Stock-Market-Prediction/blob/main/Dataset.zip).

Source: [yfinance API](https://finance.yahoo.com/)

## Architecture
![Architecture flowchart](https://user-images.githubusercontent.com/82075703/118400236-66b1e080-b67e-11eb-9f9a-be4f3a4c3a08.png)

## Models used for implementation
```
1. Ensemble Model (Buy/sell decision prediction)
     a. Random Forest Classifier (RF)
     b. K-Nearest Neighbors Classifier (KNN)
     c. Gradient Boosting (GBM)
     d. Voting Classifier: soft voting
     
2. LSTM Model (Closing stock price prediction)
```
## Ensemble Model
**Inputs:** Dataset taken from yfinance API. The following technical indicators, obtained from the FINTA library, are used - [RSI, MACD, STOCH, ADL, ATR, MOM, MFI, ROC, OBV, CCI, EMV, VI].

**Output:** Predicts whether investor should buy/sell stock on a particular day.
```
count = 0
total = 0
num_train = 10
len_train = 40
rf_RESULTS = []
knn_RESULTS = []
gb_RESULTS = []
ensemble_RESULTS = []

i = 0

rf = RandomForestClassifier()
knn = KNeighborsClassifier()
gb= GradientBoostingClassifier()
estimators=[('knn', knn), ('rf', rf) , ('gb',gb) ]
ensemble = VotingClassifier(estimators, voting='soft')
```
The ensemble model consists of RF, KNN, and GBM classsifier.

The voting classifier (set to soft voting) is used to make the final prediction.

The following confusion matrix depicts the result of the 40 sample dataset entries taken for testing the accuracy of the model:

![Confusion matrix](https://github.com/SHIVAMSINGHAL5/Stock-Market-Prediction/blob/main/Images/Result1.png)

## LSTM Model
**Input:** Dataset taken from yfinance API.

**Output:** Closing stock price prediction.
```
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape = (x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')
```
The Adam optimization algorithm is used along with the mean squared error as the loss function while compiling the model.

An RMSE analysis is done to check for the accuracy of the predicted prices, and the results are plotted graphically along with the actual prices:

![LSTM Model Data](https://github.com/SHIVAMSINGHAL5/Stock-Market-Prediction/blob/main/Images/Result2.png)
## Results
```
RF Accuracy = 71.54%
KNN Accuracy = 67.33%
GBM Accuracy = 70.26%
ENSEMBLE Accuracy = 71.59%
Accuracy of the sample dataset = 95.00%

RMSE value for LSTM model's predictions = 4.12
```

## Publication

### Title - [Stock Market Prediction Using ML Algorithms](https://github.com/SHIVAMSINGHAL5/Stock-Market-Prediction/blob/main/Research_Paper.pdf)

**Abstract -** The stock market has been a topic of great deliberation due to its diverse and convoluted nature. Today’s financial investors are plagued by sudden and notable fluctuations in the market. They cannot easily comprehend as to which stocks they should buy or sell in order to get profitable outcomes. However, with rapid advancements in machine learning, stock market prediction has become plausible. This paper proposes a stock price prediction system that utilizes an ensemble model coupled with a separate LSTM model to make predictions. The ensemble model makes use of Random Forest (RF), K-Nearest Neighbors (KNN), and Gradient Boosting (GB) classifiers to determine whether an investor should buy or sell stocks on a particular day. A separate LSTM model analyzes the historical stock data to predict the closing stock prices in the future. The combined model assists the investors to make the buy/sell call on a particular day with an approximation of the closing prices for better and safer investments.

## Project Organization
```
├── README.md                         <- A README guide for developers using this project.
├── Images
│   ├── Architecture flowchart.png    <- Project architecture flowchart.
│   ├── result1.png                   <- Buy/sell decision prediction (result of the ensemble model).
│   └── result2.png                   <- Closing stock price prediction (result of the LSTM model).
├── Dataset.zip                       <- Dataset used for building the model. It is obtained from yfinance.
│
├── Project_implementation.ipynb      <- Jupyter notebook containing full implementation.
│
├── Source_code.py                    <- Source code the of project as a Python script.
│
└── Research Paper                    <- Research Paper.
```
