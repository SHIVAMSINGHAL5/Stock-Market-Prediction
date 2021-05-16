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

## LSTM Model

## Results

## Publication

### Title - [Stock Market Prediction Using ML Algorithms](https://github.com/SHIVAMSINGHAL5/Stock-Market-Prediction/blob/main/Research_Paper.pdf)

**Abstract -** The stock market has been a topic of great deliberation due to its diverse and convoluted nature. Today’s financial investors are plagued by sudden and notable fluctuations in the market. They cannot easily comprehend as to which stocks they should buy or sell in order to get profitable outcomes. However, with rapid advancements in machine learning, stock market prediction has become plausible. This paper proposes a stock price prediction system that utilizes an ensemble model coupled with a separate LSTM model to make predictions. The ensemble model makes use of Random Forest (RF), K-Nearest Neighbors (KNN), and Gradient Boosting (GB) classifiers to determine whether an investor should buy or sell stocks on a particular day. A separate LSTM model analyzes the historical stock data to predict the closing stock prices in the future. The combined model assists the investors to make the buy/sell call on a particular day with an approximation of the closing prices for better and safer investments.

## Project Organization
├── README.md                         <- The top-level README for developers using this project.
├── Resources
│   ├── AE_output.PNG                 <- Fianl output of Auto-Encoder
│   ├── Architecture.jpeg             <- Project Architecture
│   ├── metrics.PNG                   <- Result metric of out final Model
│   ├── result.PNG                    <- Final Input Output Pipeline
│   └── gradcam.PNG                   <- Grad-Cam Output
│
├── Dataset                           <- Subset of Imagenet containing more than 200 images belonging to 1000 different classes
│
├── Dataset.zip                       <- Same Dataset Compressed in ZIP file
│
├── Full_Implementation.ipynb         <- Jupyter notebook containing full implementation
│
├── Source_Code.py                    <- Source Code of project as Python Script
│
└── Research Paper                    <- Research Paper
