'''
Python Script to download data from modis, given the modis login credentials and list of granual URLs
'''

import requests

from pyhdf.SD import SD, SDC
from PIL import Image
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import minmax_scale as scale
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import cv2
import os
import pandas as pd
import math
from sklearn.neighbors import NearestNeighbors
from keras.models import Sequential
from keras.layers import Dense,  LSTM
from keras import metrics

class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'

    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

   # Overrides from the library to keep headers when redirected to or from
   # the NASA auth host.
    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url

        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)
            if (original_parsed.hostname != redirect_parsed.hostname) and redirect_parsed.hostname != self.AUTH_HOST and original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
        return

def find_best_crop(mean_ndvi,standard_dev,crop_category_mean_ndvi):
  res = []
  #crop_category_mean_ndvi.get(mean_ndvi, data[min(data.keys(), key=lambda k: abs(k-num))])

  closest = (pd.Series(crop_category_mean_ndvi) - mean_ndvi).abs().sort_values()[:5]
  f=dict(closest)
  res=list(f.keys())


  '''for key,value in crop_category_mean_ndvi.items():
    if value-standard_dev <= mean_ndvi <= value+standard_dev:
      res.append(key)'''

  return res

def list_of_crops(lat_in,long_in,district):
    # MODIS login credentials
    username = "devb"
    password = "Devearthdata@183"

    # Session variable using credentions with custom request class
    session = SessionWithHeaderRedirection(username, password)

    # List of URLs
    urls = [ "https://e4ftl01.cr.usgs.gov//DP106/MOLT/MOD13Q1.006/2020.09.29/MOD13Q1.A2020273.h25v07.006.2020291075331.hdf"]  # South India Oct 2020


    crop_category_mean_ndvi ={'Arecanut': 0.6885986394557823, 'Arhar/Tur': 0.6467540983606557, 'Bajra': 0.6161650165016501, 'Banana': 0.630200364298725, 'Black pepper': 0.688358585858586, 'Cashewnut': 0.6729398692810458,
     'Castor seed': 0.6334563106796116, 'Coriander': 0.6378419243986255, 'Cotton(lint)': 0.627745275888133, 'Cowpea(Lobia)': 0.6494590075512405, 'Dry chillies': 0.6435831586303284, 'Garlic': 0.6217345679012346, 'Ginger': 0.6882848699763593, 'Gram': 0.650679292929293, 'Groundnut': 0.658268106162843, 'Horse-gram': 0.6618145048814504, 'Jowar': 0.63003081232493, 'Linseed': 0.6228436911487759, 'Maize': 0.6617493261455526,
     'Mesta': 0.6055652173913042, 'Moong(Green Gram)': 0.6659833333333334, 'Niger seed': 0.6421964285714286, 'Onion': 0.6229966216216216, 'Potato': 0.6413771043771044, 'Ragi': 0.6523896231032795, 'Rapeseed &Mustard': 0.6300160818713451, 'Rice': 0.6403418530351438, 'Safflower': 0.6282302737520129, 'Sannhamp': 0.6350303030303031, 'Sesamum': 0.6567513661202184, 'Small millets': 0.6505491698595148, 'Soyabean': 0.6430725623582766, 'Sugarcane': 0.6700593220338983, 'Sunflower': 0.6393148148148148, 'Sweet potato': 0.6832024353120243, 'Tapioca': 0.7126690821256039, 'Tobacco': 0.6582823315118398, 'Turmeric': 0.6674200244200245, 'Urad': 0.6674145043246839, 'Wheat': 0.6183536776212833, 'Cardamom': 0.7257387387387387, 'Peas & beans (Pulses)': 0.6533303303303303}

    crop_season={'Arecanut': 'Whole Year', 'Arhar/Tur': 'Kharif', 'Bajra': 'Kharif' , 'Banana': 'Whole Year', 'Black pepper': 'Whole Year', 'Cashewnut': 'Whole Year', 'Castor seed': 'Kharif', 'Coriander': 'Whole Year', 'Cotton(lint)': 'Whole Year', 
    'Cowpea(Lobia)': 'Kharif', 'Dry chillies': 'Kharif', 'Garlic': 'Whole Year', 'Ginger': 'Whole Year', 'Gram': 'Rabi', 'Groundnut': 'Kharif', 'Horse-gram': 'Kharif', 'Jowar': 'Kharif', 'Linseed': 'Rabi', 'Maize': 'Kharif', 'Mesta': 'Whole Year', 'Moong(Green Gram)': 'Kharif', 
    'Niger seed': 'Kharif', 'Onion': 'Kharif', 'Potato': 'Kharif', 'Ragi': 'Kharif', 'Rapeseed &Mustard': 'Rabi', 'Rice': 'Kharif', 'Safflower': 'Rabi', 'Sannhamp': 'Whole Year', 'Sesamum': 'Kharif', 'Small millets': 'Kharif', 'Soyabean': 'Kharif', 'Sugarcane': 'Whole Year', 
    'Sunflower': 'Kharif', 'Sweet potato': 'Whole Year', 'Tapioca': 'Whole Year', 'Tobacco': 'Whole Year', 'Turmeric': 'Whole Year', 'Urad': 'Kharif', 'Wheat': 'Rabi', 'Cardamom': 'Whole Year', 'Peas & beans (Pulses)': 'Rabi'}


    for url in urls:

        # extract the filename from the url to be used when saving the HDF file
        filename = url[url.rfind('/')+1:]
        image_date = '_'.join(url[url.rfind('/')-10:url.rfind('/')].split('.'))

        try:
            # submit the request using the session
            '''response = session.get(url, stream=True)
            print(f"{filename} status code: {response.status_code}")

            # raise an exception in case of http errors
            response.raise_for_status()'''

            '''Download and save the HDF file'''
            '''with open(filename, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    fd.write(chunk)

                print(filename+" Download complete!")'''

            print("Converting HDF to numpy array...")
            '''Convert HDF to numpy arrays using pyhdf'''
            file = SD(filename, SDC.READ)

            # select the NDVI dataset from HDF file
            ndvi_obj = file.select('250m 16 days NDVI') 
            ndvi_numpy_ndarray = ndvi_obj.get()

            normalized_ndvi_ndarray = ndvi_numpy_ndarray / 10000

            print("Normalized NDVI array: \n",normalized_ndvi_ndarray)


            # extract the 10x10sqkm area around the given latitude and longitude
            latitude_input = math.floor(float(lat_in))
            longitude_input = math.floor(float(long_in))

            # Hard-coded values for north east india MODIS image
            modis_grid_coordinates = {
                "north_east" : {
                    "long_upper_left" :  92.0544, 
                    "lat_upper_left" :  30.0438
                },
                "south" : {
                    "long_upper_left" : 74.2034,
                    "lat_upper_left" : 20.0210
                }
            }

            long_upper_left = modis_grid_coordinates["south"]["long_upper_left"]
            lat_upper_left = modis_grid_coordinates["south"]["lat_upper_left"]

            long_diff = abs(long_upper_left - longitude_input)
            lat_diff = abs(lat_upper_left - latitude_input)
            
            # Calculate distance
            long_dist_kms = (2 * math.pi / 360) * 6378 * math.cos(math.radians(latitude_input))    #long_dist_kms is kilometers per longitude
            lat_dist_kms = 111

            displacement_right_kms = long_diff * abs(long_dist_kms)
            displacement_down_kms = lat_diff * lat_dist_kms

            print("Displacement in kms Down:",displacement_down_kms," Right: ",displacement_right_kms)

            # Calculate Pixels
            displacement_right_pixels = displacement_right_kms * 4 
            displacement_down_pixels = displacement_down_kms * 4 

            print("Displacement in pixels Down:",displacement_down_pixels," Right: ",displacement_right_pixels)

            slice_point_top_left_x = math.floor(displacement_right_pixels - 20)
            slice_point_top_left_y = math.floor(displacement_down_pixels - 20)

            print("Slice point x:",slice_point_top_left_x," y: ",slice_point_top_left_y)

            region_of_interst = normalized_ndvi_ndarray[slice_point_top_left_x : slice_point_top_left_x + 40,slice_point_top_left_y : slice_point_top_left_y + 40]
            
            print(region_of_interst)
            print(np.shape(region_of_interst))

            mean_ndvi = 0
            for i in range(40):
                mean_ndvi += np.mean(region_of_interst[i][:])

            mean_ndvi /= 40
            print(f"mean_ndvi at latitude = {latitude_input} and longitude = {longitude_input} is: {mean_ndvi}")

            '''Save numpy array as PNG'''
            ndvi_image = Image.fromarray(np.uint8(cm.gist_earth(region_of_interst)*255))
            ndvi_image.save("roi.png")
            ndvi_image = Image.fromarray(np.uint8(cm.gist_earth(normalized_ndvi_ndarray)*255))
            ndvi_image.save("entire_image.png")

            list_of_crops = find_best_crop(mean_ndvi,0.05,crop_category_mean_ndvi)
            #yield pred call
            yields=[]
            prices=[]
            print(list_of_crops)
            #temp_prices=['Arecanut','Arhar','Bajra','Rice','Wheat']
            for i in range(len(list_of_crops)):
                yields.append(yield_prediction(str(list_of_crops[i]),crop_season[str(list_of_crops[i])]))
                prices.append(price_pred(str(list_of_crops[i]),district))
            res=[]
            for i in range(len(list_of_crops)):
                temp=[]
                temp.append(list_of_crops[i])
                temp.append(round(yields[i],2))
                temp.append(prices[i])
                res.append(temp)

            #print(res)
            return res

        except requests.exceptions.HTTPError as e:
            # handle any errors here
            print(filename + " Error Occured: ",e)

    print("Execution Complete!")

#____________________________________________________________________
#YIELD PREDICTION
def yield_prediction(crop,season):
    file_df = pd.read_csv('/home/user1/Downloads/UI/combined_csv.csv')
    #print(file_df)
    index_names = file_df[ file_df['JANUARY_NDVI'] == -100 ].index 
    # drop these row indexes 
    # from dataFrame 
    file_df.drop(index_names, inplace = True) 
    df = file_df
    #print(df)
    df = df.loc[((df['Crop'] == crop) & (df['Season'].str.strip() == season) )]
    #print(df['Yield'].min())
    

    # df = pd.DataFrame(np.random.randn(100, 3))

    # Removing the outliers:

    q = df["Yield"].quantile(0.75)
    p = df["Yield"].quantile(0.25)


    df = df[(df["Yield"] < q) & (df["Yield"] > p)]

    X = df[['JANUARY_NDVI','FEBRUARY_NDVI','JUNE_NDVI','JULY_NDVI','AUGUST_NDVI','SEPTEMBER_NDVI','OCTOBER_NDVI','NOVEMBER_NDVI','DECEMBER_NDVI']]
    Y = df['Yield']
    print(X,Y)

    x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size =0.2,train_size=0.8)
    model = LinearRegression()
    model.fit(x_train,y_train)

    y_pred = model.predict(x_test)
    return y_pred[-1]
'''
    from sklearn import metrics
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

    # y_test = pd.DataFrame(y_test)
    # y_pred = pd.DataFrame(y_pred)
    # df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    # df

    # pd.concat([d.reset_index(drop=True) for d in [y_test, y_pred]], axis=1)
    df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    df

    import matplotlib.pyplot as plt
    plt.scatter(df['Actual'], df['Predicted'])
    plt.show() # Depending on whether you use IPython or interactive mode, etc.

'''

def price_pred(crop,district):
    crops_list=os.listdir("Karnataka")
    if not (crop in crops_list):
        return default_prices[district][crop]

    list_of_districts=os.listdir(f'Karnataka/{crop}')
    if not (f"{crop}_{district}.csv" in list_of_districts):
        return default_prices[district][crop]
    df = pd.read_csv(f'Karnataka/{crop}/{crop}_{district}.csv')

    rows=len(df)
    price = df.loc[:,'MeanPrice(Rs./Quintal)']
    l = len(df)
    price = np.array(price)
    price = price.reshape(-1,1)
    #plt.plot(price)
    #plt.xticks(range(0,df.shape[0]),df['Year'],rotation=90)
    #plt.show(block= False)
    X1= price[0:l-3,:] # 1st till 3rd last value
    X2=price[1:l-2,:]  # 2nd till 2nd last value  
    X3=price[2:l-1,:]  # 3rd till last value
    price = price[3:l,:]
    X= np.concatenate([X1,X2,X3],axis=1)
    print(f'X shape is {X.shape}')
    print(f'price shape is {price.shape}')
    scaler = MinMaxScaler() # scaling between 0 to 1
    scaler.fit(X)
    X = scaler.transform(X)
    scaler1 = MinMaxScaler()
    scaler1.fit(price)
    price = scaler1.transform(price)
    a,b,c=price[-3],price[-2],price[-1]
    X= np.reshape(X, (X.shape[0],1,X.shape[1])) # list of lists of lists (36,1,3)
    X_train=X[:int(0.8*rows)]
    X_test = X[int(0.2*rows)::-1]
    price_train = price[:int(0.8*rows)]
    price_test = price[int(0.2*rows)::-1]
    inv_scaler = MinMaxScaler()
    inv_scaler.min_ = scaler.min_[0]
    inv_scaler.scale_ = scaler.scale_[0]

    model = Sequential()
    model.add(LSTM(15,activation = 'tanh',input_shape = (1,3),recurrent_activation= 'hard_sigmoid'))

    model.add(Dense(1,activation='tanh'))
    model.compile(loss= 'mean_squared_error',optimizer = 'rmsprop', metrics=[metrics.MeanSquaredError()])
    model.fit(X_train,price_train,epochs=250,verbose=2)
    Predict = model.predict(X_test)

    newPredict = model.predict([[[a[0],b[0],c[0]]]])
    # print(X_test)

    # print(newPredict)

    price=inv_scaler.inverse_transform(newPredict)

    print(f"The predicted price per quintal of {crop} is: Rs",round(price[0][0],2))

    # plt.figure(figsize=(15,10))
    # plt.plot(price_test,label = 'Test')
    # plt.plot(Predict, label = 'Prediction')
    # plt.legend(loc='best')
    # plt.show()
    return str(round(price[0][0],2))
