from libraries import *
from constants import * 

def yield_prediction(dict_month_ndvis,district):
    #dict_month_ndvis = {'JANUARY_NDVI':0.547,'FEBRUARY_NDVI':0.274,'JUNE_NDVI':0.754,'JULY_NDVI':0.537,'AUGUST_NDVI':0.339,'SEPTEMBER_NDVI':0.098,'OCTOBER_NDVI':0.845,'NOVEMBER_NDVI':0.833,'DECEMBER_NDVI':0.539}

    file_df = pd.read_csv('/home/user1/Downloads/UI/combined_csv.csv')
    index_names = file_df[ file_df['JANUARY_NDVI'] == -100 ].index 
    # drop these row indexes 
    # from dataFrame 
    file_df.drop(index_names, inplace = True) 
    df = file_df
    dharwad_df = df.loc[df['District'].str.strip() == district.upper()]
    print('--------------------------------------------',dharwad_df)
    #highest correlated months for Dharwad 
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

    crops_and_predictedYields={}
    for i in listOfCrops:
        #listOfCrops is accessed from constants.py
        if i in dict_correlated_months:
            df = dharwad_df
            dharwad_cropdf = df.loc[((df['Crop'] == i))]
            X = dharwad_cropdf[[dict_correlated_months[i]]]
            Y = dharwad_cropdf['Yield']
            #use entire dataset for training
            x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size =0.2)
            x_train_list = x_train.to_numpy(copy=True)
            y_train_list = y_train.to_numpy(copy=True)
            x_train_list = x_train_list.flatten()
            slope, intercept, r_value, p_value, std_err = stats.linregress(x_train_list, y_train_list)
            print(r_value**2, r_value)
            model = LinearRegression()
            model.fit(x_train,y_train)
            correlated_month_NDVI_value = [[dict_month_ndvis[dict_correlated_months[i]]]]
            crops_and_predictedYields[i] = abs(round(model.predict(correlated_month_NDVI_value)[0],2))

            
        else:
            continue

    return crops_and_predictedYields

