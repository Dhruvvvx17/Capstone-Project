from libraries import *


def price_pred(crop, district):
    crops_list = os.listdir("Karnataka")
    if not (crop in crops_list):
        return "Price Unavailable"

    list_of_districts = os.listdir(f'Karnataka/{crop}')
    if not (f"{crop}_{district}.csv" in list_of_districts):
        return "Price Unavailable"
    df = pd.read_csv(f'Karnataka/{crop}/{crop}_{district}.csv')

    rows = len(df)
    price = df.loc[:, 'MeanPrice(Rs./Quintal)']
    l = len(df)
    price = np.array(price)
    price = price.reshape(-1, 1)
    # plt.plot(price)
    # plt.xticks(range(0,df.shape[0]),df['Year'],rotation=90)
    #plt.show(block= False)
    X1 = price[0:l-3, :]  # 1st till 3rd last value
    X2 = price[1:l-2, :]  # 2nd till 2nd last value
    X3 = price[2:l-1, :]  # 3rd till last value
    price = price[3:l, :]
    X = np.concatenate([X1, X2, X3], axis=1)
    print(f'X shape is {X.shape}')
    print(f'price shape is {price.shape}')
    scaler = MinMaxScaler()  # scaling between 0 to 1
    scaler.fit(X)
    X = scaler.transform(X)
    scaler1 = MinMaxScaler()
    scaler1.fit(price)
    price = scaler1.transform(price)
    a, b, c = price[-3], price[-2], price[-1]
    # list of lists of lists (36,1,3)
    X = np.reshape(X, (X.shape[0], 1, X.shape[1]))
    X_train = X[:int(0.8*rows)]
    X_test = X[int(0.2*rows)::-1]
    price_train = price[:int(0.8*rows)]
    price_test = price[int(0.2*rows)::-1]
    inv_scaler = MinMaxScaler()
    inv_scaler.min_ = scaler.min_[0]
    inv_scaler.scale_ = scaler.scale_[0]

    model = Sequential()
    model.add(LSTM(15, activation='tanh', input_shape=(
        1, 3), recurrent_activation='hard_sigmoid'))

    model.add(Dense(1, activation='tanh'))
    model.compile(loss='mean_squared_error', optimizer='rmsprop',
                  metrics=[metrics.MeanSquaredError()])
    model.fit(X_train, price_train, epochs=250, verbose=2)
    Predict = model.predict(X_test)

    newPredict = model.predict([[[a[0], b[0], c[0]]]])
    # print(X_test)

    # print(newPredict)

    price = inv_scaler.inverse_transform(newPredict)

    print(f"The predicted price per quintal of {crop} is: Rs", round(
        price[0][0], 2))

    # plt.figure(figsize=(15,10))
    # plt.plot(price_test,label = 'Test')
    # plt.plot(Predict, label = 'Prediction')
    # plt.legend(loc='best')
    # plt.show()
    return str(round(price[0][0], 2))
