# Import tensorflow
import tensorflow as tf
tf.__version__

#import library
import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import yfinance as yf

# Install yfinance
!pip install yfinance

# Download BBRI.JK File
A_df = yf.download('BBRI.JK')

# Show dataset
A_df

# Import datetime
import datetime

# Install Datetime
!pip install datetime

# Time range
start = datetime.datetime(2019,1,20)
end = datetime.datetime(2023,6,15)

# Download BBRI.JK file
A_df = yf.download('BBRI.JK', start=start, end=end)

# Show dataset
A_df

# Show shape
A_df.shape

# Plot the prediction results on the training data
plt.figure(figsize=(16,8))
plt.title('Close Price History')
plt.plot(A_df['Close'])
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price USD($)',fontsize=18)
plt.show()

# Data conversion into numpy array form
data=A_df.filter(['Close'])
dataset=data.values
training_data_len=math.ceil(len(dataset)*.8)

# Scale the data
scaler=MinMaxScaler(feature_range=(0,1))
scaled_data=scaler.fit_transform(dataset)
scaled_data

# Show shape
A_df.shape

# Create training data set
train_data=scaled_data[0:training_data_len,:]

# Split the data into x_train and y_train data sets
x_train=[]
y_train=[]

################### 過去６０日分のデータでYを説明する、という形##################
for i in range(60,len(train_data)):
    x_train.append(train_data[i-60:i,0])
    y_train.append(train_data[i,0])
    if i<=60:
        print(x_train)
        print(y_train)
        print()

# Show shape
A_df.shape

#convert train data to numpy arrays
x_train,y_train=np.array(x_train),np.array(y_train)

#Reshape
x_train.shape

# Train Shape
x_train=np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))
x_train.shape

# Build LSTM model
model=Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(LSTM(50,return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam',loss='mean_squared_error')

# Train the model
model.fit(x_train,y_train,batch_size=1,epochs=1)

# Create the testing data set
test_data=scaled_data[training_data_len-60:,:]

# Create the data sets x_test and y_test
x_test=[]
y_test=dataset[training_data_len:,:]
for i in range(60,len(test_data)):
    x_test.append(test_data[i-60:i,0])

# Convert the data to a numpy array
x_test=np.array(x_test)

# Reshape
x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

# Get the models predicted price values
predictions=model.predict(x_test)
predictions=scaler.inverse_transform(predictions)

# Get the root mean squared error(RMSE)
rmse=np.sqrt( np.mean((predictions - y_test)**2))

# Print RMSE
rmse

# Train prediction dataset
train=data[:training_data_len]
valid=data[training_data_len:]
valid['Predictions']=predictions

# Visualize the data
plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price RP(Rp)',fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close','Predictions']])
plt.legend(['Train','Val','Predictions'],loc='lower right')
plt.show()

# Show the valid and predicted prices
 valid

# Get the quote
apple_quote=A_df = yf.download('BBRI.JK')

# Create a new dataframe
new_df=apple_quote.filter(['Close'])

# Get the last 60 day closing price values and convert the dataframe to an array
last_60_days=new_df[-60:].values

# Scale the data to be values between 0 and 1
last_60_days_scaled=scaler.transform(last_60_days)

# Create an empty list
X_test=[]

# Append the past 60 days
X_test.append(last_60_days_scaled)

# Convert the X_test data to a numpy array
X_test=np.array(X_test)

# Reshape
X_test=np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))

# Get the predicted scaled price
pred_price=model.predict(X_test)

# Undo the scaling
pred_price=scaler.inverse_transform(pred_price)
print(pred_price)

# Get the quote
apple_quote2=A_df = yf.download('BBRI.JK')
print(apple_quote2['Close'])