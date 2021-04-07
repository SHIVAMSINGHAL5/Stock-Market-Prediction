# Stock-Market-Prediction
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


