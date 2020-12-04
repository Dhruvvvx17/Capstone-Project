

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