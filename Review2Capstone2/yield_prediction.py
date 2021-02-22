# from libraries import *


# def yield_prediction(crop, season):
    
#     file_df = pd.read_csv('/home/user1/Downloads/UI/combined_csv.csv')
#     # print(file_df)
#     index_names = file_df[file_df['JANUARY_NDVI'] == -100].index
#     # drop these row indexes
#     # from dataFrame
#     file_df.drop(index_names, inplace=True)
#     df = file_df
#     # print(df)
#     df = df.loc[((df['Crop'] == crop) & (df['Season'].str.strip() == season))]
#     # print(df['Yield'].min())

#     # df = pd.DataFrame(np.random.randn(100, 3))

#     # Removing the outliers:

#     q = df["Yield"].quantile(0.75)
#     p = df["Yield"].quantile(0.25)

#     df = df[(df["Yield"] < q) & (df["Yield"] > p)]

#     X = df[['JANUARY_NDVI', 'FEBRUARY_NDVI', 'JUNE_NDVI', 'JULY_NDVI', 'AUGUST_NDVI',
#             'SEPTEMBER_NDVI', 'OCTOBER_NDVI', 'NOVEMBER_NDVI', 'DECEMBER_NDVI']]
#     Y = df['Yield']
#     print(X, Y)

#     x_train, x_test, y_train, y_test = train_test_split(
#         X, Y, test_size=0.2, train_size=0.8)
#     model = LinearRegression()
#     model.fit(x_train, y_train)

#     y_pred = model.predict(x_test)
#     return y_pred[-1]





from libraries import *
from constants import * 

def yield_prediction(dict_month_ndvis):
    #dict_month_ndvis = {'JANUARY_NDVI':0.547,'FEBRUARY_NDVI':0.274,'JUNE_NDVI':0.754,'JULY_NDVI':0.537,'AUGUST_NDVI':0.339,'SEPTEMBER_NDVI':0.098,'OCTOBER_NDVI':0.845,'NOVEMBER_NDVI':0.833,'DECEMBER_NDVI':0.539}

    file_df = pd.read_csv('/home/user1/Downloads/UI/combined_csv.csv')
    index_names = file_df[ file_df['JANUARY_NDVI'] == -100 ].index 
    # drop these row indexes 
    # from dataFrame 
    file_df.drop(index_names, inplace = True) 
    df = file_df
    dharwad_df = df.loc[df['District'].str.strip() == 'DHARWAD']


    dict_correlated_months = {
        'Arhar/Tur':'OCTOBER_NDVI',
        'Cashewnut':'JUNE_NDVI',
        'Castor seed':'DECEMBER_NDVI',
        'Coriander':'JANUARY_NDVI',
        'Cotton(lint)':'FEBRUARY_NDVI',
        'Garlic':'JUNE_NDVI',
        'Ginger':'NOVEMBER_NDVI',
        'Gram':'DECEMBER_NDVI',
        'Groundnut':'SEPTEMBER_NDVI',
        'Horse-gram':'DECEMBER_NDVI',
        'Jowar':'NOVEMBER_NDVI',
        'Linseed':'FEBRUARY_NDVI',
        'Moong(Green Gram)':'SEPTEMBER_NDVI',
        'Ragi':'NOVEMBER_NDVI',
        'Rapeseed &Mustard':'DECEMBER_NDVI',
        'Safflower':'FEBRUARY_NDVI',
        'Sugarcane':'JULY_NDVI',
        'Tobacco':'SEPTEMBER_NDVI',
        'Turmeric':'JUNE_NDVI',
        'Wheat':'OCTOBER_NDVI'
    }

    y_pred={}
    for i in listOfCrops:
        if i in dict_correlated_months:
            df = dharwad_df
            # df = df.loc[df['District'].str.strip() == 'DHARWAD']
            dharwad_cropdf = df.loc[((df['Crop'] == i))]
            #print(f'Dataframe for crop {i}: ')
            # print(dharwad_cropdf)
            X = dharwad_cropdf[[dict_correlated_months[i]]]
            Y = dharwad_cropdf['Yield']
            x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size =0.2)
            x_train_list = x_train.to_numpy(copy=True)
            y_train_list = y_train.to_numpy(copy=True)
            x_train_list = x_train_list.flatten()
            slope, intercept, r_value, p_value, std_err = stats.linregress(x_train_list, y_train_list)
            # print(r_value**2, r_value)
            model = LinearRegression()
            model.fit(x_train,y_train)
            # temp = dict_month_ndvis[dict_correlated_months[i]].reshape(1,-1)
            # temp = [np.array(dict_month_ndvis[dict_correlated_months[i]])]
            # temp.reshape(1,-1)
            # replace with corresponding month ndvi
            temp = [[dict_month_ndvis[dict_correlated_months[i]]]]
            y_pred[i] = round(model.predict(temp)[0],2)
            #print(y_pred)
            
        else:
            continue

    return y_pred

