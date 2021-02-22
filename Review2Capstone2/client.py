from constants import *
from download import download_hdf
from hdf_links import urls
from image_extraction import extraction
from libraries import *
from list_of_crops import list_of_crops
from mean_ndvi_calc import mean_ndvi_calc


def suggest_crops(lat_in, long_in, district,area):

    #hdf_filename = download_hdf(urls)
    hdf_filename_list =['./hdfs/Jan.hdf','./hdfs/Feb.hdf','./hdfs/June.hdf','./hdfs/July.hdf','./hdfs/Aug.hdf','./hdfs/Sept.hdf','./hdfs/Oct.hdf','./hdfs/Nov.hdf','./hdfs/Dec.hdf']
    # returns an ndarray
    mean_ndvi=[]
    
    for i in range(len(hdf_filename_list)):
        region_of_interest=extraction(hdf_filename_list[i], lat_in, long_in)
        mean_ndvi.append( mean_ndvi_calc(region_of_interest))

    dict_month_ndvis = {'JANUARY_NDVI':mean_ndvi[0],'FEBRUARY_NDVI':mean_ndvi[1],'JUNE_NDVI':mean_ndvi[2],'JULY_NDVI':mean_ndvi[3],'AUGUST_NDVI':mean_ndvi[4],'SEPTEMBER_NDVI':mean_ndvi[5],'OCTOBER_NDVI':mean_ndvi[6],'NOVEMBER_NDVI':mean_ndvi[7],'DECEMBER_NDVI':mean_ndvi[8]}
        

    for j in range(len(mean_ndvi)):
        print(
            f"mean_ndvi at latitude = {lat_in} and longitude = {long_in} is: {mean_ndvi[j]}")

    # crops + yeilds + price [[,,]...]
    final_result = list_of_crops(dict_month_ndvis, district,area)

    return final_result

#print(suggest_crops(15.45,75.00,'Dharwad',2))