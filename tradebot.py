# Import Required Libraries
import yahooquery as yq # Pull Historical and Financial Data on Tickers
import pandas as pd # Manage database
import matplotlib.pyplot as plt # Plotting/visualization
import warnings # Warnings
from math import sqrt # Square root function used in grid search for hyper parameters
from statsmodels.tsa.arima.model import ARIMA # Model for timeseries analysis
from sklearn.metrics import mean_squared_error # Metrics tools for ML model

#_-_-_-_-DATA SETUP_-_-_-_-#

# Pull 1 day price info for ticker name given below in 1 minute intervals
ticker = "MSFT"
stock = yq.Ticker(ticker)
data = stock.financial_data
historical = stock.history(period='1d', interval='1m')

# Add stock data and stock hisotrical prices to dataframes
stock_data = pd.DataFrame(data)
stock_history = pd.DataFrame(historical)
print(stock_data.head(n=5))
print(stock_history.head(n=5))

# Extract lowest price from historical dataframe
stock_low = stock_history[['low']]
print(stock_low.head(5))

# Split dataframe into training and test data
X = stock_history.index.values
Y = stock_history[['low']].values
# - Split off last 10% of data for testing
offset = int(0.10*len(stock_history))
X_train = X[:-offset]
Y_train = Y[:-offset]
X_test = X[-offset:]
Y_test = Y[-offset:]
# - Plot the data
plt.plot(range(0,len(Y_train)),Y_train, label='Train')
plt.plot(range(len(Y_train),len(Y)),Y_test,label='Test')
plt.legend()
plt.show()

#_-_-_-_-ARIMA MODEL SETUP_-_-_-_-#

# Define function to evaluate an ARIMA model for a given order (p,d,q)
def evaluate_arima_model(X, arima_order):
# Prepare training dataset
    size = offset
    train, test = Y_train, Y_test
    history = [x for x in train]
    # Make a list to store predictions
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=arima_order)
        model_fit = model.fit()
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])
    # Calculate Out of Sample Error
    rmse = sqrt(mean_squared_error(test, predictions))
    return rmse
 
# Define function to evaluate combinations of p, q and d values for ARIMA model
def eval_models(dataset, p_values, d_values, q_values):
    dataset = dataset.astype('float32')
    global best_cfg
    best_score, best_cfg = float("inf"), None
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p,d,q)
            try:
                rmse = evaluate_arima_model(dataset, order)
                if rmse < best_score:
                    best_score, best_cfg = rmse, order
                print('ARIMA%s RMSE=%.3f' % (order,rmse))
            except:
                continue
    print('Best ARIMA%s RMSE=%.3f' % (best_cfg, best_score))

# Load data
series = stock_low

# Create ranges of hyperparameters and test in grid search
p_values = [0, 1, 2, 4, 6, 8, 10]
d_values = range(0, 3)
q_values = range(0, 3)
warnings.filterwarnings("ignore")
eval_models(series.values, p_values, d_values, q_values)

# Create ARIMA model with determined hyperparameters
cfg = best_cfg
model = ARIMA(Y_train, order = cfg).fit()
forecast = model.forecast(steps=1)[0]



