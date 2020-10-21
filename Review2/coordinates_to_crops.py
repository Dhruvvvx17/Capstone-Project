'''
Python Script to download data from modis, given the modis login credentials and list of granual URLs
'''

import requests

from pyhdf.SD import SD, SDC
from PIL import Image
from matplotlib import cm
import numpy as np
from sklearn.preprocessing import minmax_scale as scale

import cv2
import os

import math


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
  for key,value in crop_category_mean_ndvi.items():
    if value-standard_dev <= mean_ndvi <= value+standard_dev:
      res.append(key)

  return res

def list_of_crops(lat_in,long_in):
    # MODIS login credentials
    username = "devb"
    password = "Devearthdata@183"

    # Session variable using credentions with custom request class
    session = SessionWithHeaderRedirection(username, password)

    # List of URLs
    urls = [ "https://e4ftl01.cr.usgs.gov//DP106/MOLT/MOD13Q1.006/2020.09.29/MOD13Q1.A2020273.h25v07.006.2020291075331.hdf"]  # South India Oct 2020


    crop_category_mean_ndvi = {
    "Fully Irrigated Maize" : 0.576,
    "Partially Irrigated Maize" : 0.477,
    "Potato" : 0.6,
    "Ragi" : 0.688,
    #"double_triple" : 0.705,
    "Apple Orchard" : 0.692,
    "Sugarcane" : 0.612,
    "Coffee" : 0.40,
    "Rice" : 0.74
  
    }


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
            return(list_of_crops)

        except requests.exceptions.HTTPError as e:
            # handle any errors here
            print(filename + " Error Occured: ",e)

    print("Execution Complete!")
