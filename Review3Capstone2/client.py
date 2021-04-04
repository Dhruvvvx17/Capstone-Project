from constants import *
from download import download_hdf
from hdf_links import urls
from image_extraction import extraction
from libraries import *
from list_of_crops import list_of_crops
from mean_ndvi_calc import mean_ndvi_calc


def suggest_crops(lat_in, long_in, district,area):
    hdf_filename_list =['./hdfs/Jan.hdf','./hdfs/Feb.hdf','./hdfs/June.hdf','./hdfs/July.hdf','./hdfs/Aug.hdf','./hdfs/Sept.hdf','./hdfs/Oct.hdf','./hdfs/Nov.hdf','./hdfs/Dec.hdf']
    monthly_mean_ndvi=[]
    
    for i in range(len(hdf_filename_list)):
        region_of_interest=extraction(hdf_filename_list[i], lat_in, long_in)
        monthly_mean_ndvi.append( mean_ndvi_calc(region_of_interest))

    dict_month_ndvis = {'JANUARY_NDVI':monthly_mean_ndvi[0],'FEBRUARY_NDVI':monthly_mean_ndvi[1],'JUNE_NDVI':monthly_mean_ndvi[2],'JULY_NDVI':monthly_mean_ndvi[3],'AUGUST_NDVI':monthly_mean_ndvi[4],'SEPTEMBER_NDVI':monthly_mean_ndvi[5],'OCTOBER_NDVI':monthly_mean_ndvi[6],'NOVEMBER_NDVI':monthly_mean_ndvi[7],'DECEMBER_NDVI':monthly_mean_ndvi[8]}
        

    for j in range(len(monthly_mean_ndvi)):
        print(
            f"monthly_mean_ndvi at latitude = {lat_in} and longitude = {long_in} is: {monthly_mean_ndvi[j]}")

    final_result = list_of_crops(dict_month_ndvis, district,area)

    return final_result
