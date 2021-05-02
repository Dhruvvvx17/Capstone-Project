from constants import *
from yield_prediction import yield_prediction
from price_prediction import price_prediction
from libraries import *
from babel.numbers import format_currency

def list_of_crops(monthly_mean_ndvi, district,area):
    all_details_of_crop=[]
    print('222222222222')
    crops_and_predictedYields=yield_prediction(monthly_mean_ndvi,district)
    print('3333333333333',crops_and_predictedYields)
    for i in crops_and_predictedYields:
        predictedPrice,flag=price_prediction(i,district)
        print('44444444444',predictedPrice)
        if predictedPrice=="Unavailable":
            continue
        else:
            #res=format_currency(int(round(price[0][0]))*10,'INR',locale='en_IN')
            formatted_predicted_price_unit=format_currency(predictedPrice, 'INR',locale='en_IN')
            formatted_predicted_price_whole=format_currency(str(1000*round(float(predictedPrice)*round(round(crops_and_predictedYields[i], 2)*float(area),2))), 'INR',locale='en_IN')
            partial_details_of_crops=[i,crops_and_predictedYields[i],formatted_predicted_price_unit,crops_and_predictedYields[i]*float(area),formatted_predicted_price_whole]
            #partial_details_of_crops=[i,crops_and_predictedYields[i],predictedPrice,crops_and_predictedYields[i]*float(area)]

            #partial_details_of_crops.append(str(round(float(predictedPrice)*round(round(crops_and_predictedYields[i], 2)*float(area),2))))
            all_details_of_crop.append(partial_details_of_crops)

    return all_details_of_crop