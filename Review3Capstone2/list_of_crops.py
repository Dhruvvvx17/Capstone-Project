from constants import *
from yield_prediction import yield_prediction
from price_prediction import price_prediction
from libraries import *

def list_of_crops(monthly_mean_ndvi, district,area):
    all_details_of_crop=[]
    
    crops_and_predictedYields=yield_prediction(monthly_mean_ndvi)

    for i in crops_and_predictedYields:
        predictedPrice,flag=price_prediction(i,'Dharwar')
        if predictedPrice=="Unavailable":
            continue
        else:
            partial_details_of_crops=[i,crops_and_predictedYields[i],predictedPrice,crops_and_predictedYields[i]*float(area)]
            partial_details_of_crops.append(str(round(float(predictedPrice)*round(round(crops_and_predictedYields[i], 2)*float(area),2))))
            all_details_of_crop.append(partial_details_of_crops)

    return all_details_of_crop