from libraries import *


def yield_prediction(crop, season):
    file_df = pd.read_csv('/home/user1/Downloads/UI/combined_csv.csv')
    # print(file_df)
    index_names = file_df[file_df['JANUARY_NDVI'] == -100].index
    # drop these row indexes
    # from dataFrame
    file_df.drop(index_names, inplace=True)
    df = file_df
    # print(df)
    df = df.loc[((df['Crop'] == crop) & (df['Season'].str.strip() == season))]
    # print(df['Yield'].min())

    # df = pd.DataFrame(np.random.randn(100, 3))

    # Removing the outliers:

    q = df["Yield"].quantile(0.75)
    p = df["Yield"].quantile(0.25)

    df = df[(df["Yield"] < q) & (df["Yield"] > p)]

    X = df[['JANUARY_NDVI', 'FEBRUARY_NDVI', 'JUNE_NDVI', 'JULY_NDVI', 'AUGUST_NDVI',
            'SEPTEMBER_NDVI', 'OCTOBER_NDVI', 'NOVEMBER_NDVI', 'DECEMBER_NDVI']]
    Y = df['Yield']
    print(X, Y)

    x_train, x_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.2, train_size=0.8)
    model = LinearRegression()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    return y_pred[-1]
