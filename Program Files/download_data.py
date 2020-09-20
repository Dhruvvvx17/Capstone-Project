'''
    Python Script to download data from modis, given the modis login credentials and list of granual URLs
'''

'''
Run the following before running this script
!apt-get install build-essential python3-dev python3-numpy libhdf4-dev -y
!pip install pyhdf
'''

import requests

from pyhdf.SD import SD, SDC
from PIL import Image
from matplotlib import cm
import numpy as np
from sklearn.preprocessing import minmax_scale as scale

import cv2
import os


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


# MODIS login credentials
username = "devb"
password = "Devearthdata@183"

# Session variable using credentions with custom request class
session = SessionWithHeaderRedirection(username, password)

# List of URLs
urls = [
    "https://e4ftl01.cr.usgs.gov//DP106/MOLT/MOD13Q1.006/2020.08.28/MOD13Q1.A2020241.h25v07.006.2020261220902.hdf",
    "https://e4ftl01.cr.usgs.gov//DP106/MOLT/MOD13Q1.006/2020.08.12/MOD13Q1.A2020225.h25v07.006.2020241232304.hdf",
    "https://e4ftl01.cr.usgs.gov//DP106/MOLT/MOD13Q1.006/2020.07.27/MOD13Q1.A2020209.h25v07.006.2020226011049.hdf"
    ]


# New directory for saving image splits
all_images = "Image_splits_chikkaballapur"
path = os.path.join("/content",all_images)
os.mkdir(path)
image_count = 0


for url in urls:

    # extract the filename from the url to be used when saving the HDF file
    filename = url[url.rfind('/')+1:]
    image_date = '_'.join(url[url.rfind('/')-10:url.rfind('/')].split('.'))

    try:
        # submit the request using the session
        response = session.get(url, stream=True)
        print(f"{filename} status code: {response.status_code}")

        # raise an exception in case of http errors
        response.raise_for_status()

        '''Download and save the HDF file'''
        with open(filename, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=1024*1024):
                fd.write(chunk)

            print(filename+" Download complete!")


        '''Convert HDF to numpy arrays using pyhdf'''
        file = SD(filename, SDC.READ)

        # select the NDVI dataset from HDF file
        ndvi_obj = file.select('250m 16 days NDVI') 
        ndvi_numpy_ndarray = ndvi_obj.get()

        normalized_ndvi_ndarray = ndvi_numpy_ndarray / 10000
        # normalized_ndvi_ndarray = scale(data,feature_range=(-1,1))

        '''Save numpy array as PNG'''
        ndvi_image = Image.fromarray(np.uint8(cm.gist_earth(normalized_ndvi_ndarray)*255))
        ndvi_image.save(f"{image_date}.png")


        '''Split the PNG for a particular district'''
        main_img = cv2.imread(f"{image_date}.png")
        district_img = main_img[3360:3360+480, 2640:2640+480,:]
        cv2.imwrite(f"{image_date}_split_3360_2640.png",district_img)


        '''Create folder for the current image date''' 
        current_image_splits_dir_path = os.path.join("/content",all_images,image_date)
        os.mkdir(current_image_splits_dir_path)


        '''Splitting district image (480x480) into smaller 40x40 images'''
        img = cv2.imread(f"{image_date}_split_3360_2640.png")
        for row in range(0,img.shape[0],40):
            for col in range(0,img.shape[1],40):
                cv2.imwrite(f"{current_image_splits_dir_path}/{image_date}_split_{row}_{col}.png",img[row:row+40, col:col+40,:])


        '''Delete temporary files'''
        os.remove(f"{image_date}_split_3360_2640.png")      # District image (480x480)
        os.remove(f"{image_date}.png")                      # numpy array to PNG image (4800x4800)
        os.remove(filename)                                 # Actual HDF


        '''Logs'''
        image_count += 1
        print(f"Total number of images downloaded and extracted: {image_count}\n")

    except requests.exceptions.HTTPError as e:
        # handle any errors here
        print(filename + " Error Occured: ",e)


print("Processing complete!")