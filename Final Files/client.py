from constants import *
from download import download_hdf
from hdf_links import urls
from image_extraction import extraction
from libraries import *
from list_of_crops import list_of_crops
from mean_ndvi_calc import mean_ndvi_calc


def suggest_crops(lat_in, long_in, district,area):

    #hdf_filename = download_hdf(urls)
    hdf_filename ='MOD13Q1.A2020273.h25v07.006.2020291075331.hdf'
    # returns an ndarray

    region_of_interest = extraction(hdf_filename, lat_in, long_in)

    mean_ndvi = mean_ndvi_calc(region_of_interest)

    print(
        f"mean_ndvi at latitude = {lat_in} and longitude = {long_in} is: {mean_ndvi}")

    # crops + yeilds + price [[,,]...]
    final_result = list_of_crops(mean_ndvi, district,area)

    return final_result
