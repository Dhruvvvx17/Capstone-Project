from constants import *
from yield_prediction import yield_prediction
from price_prediction import price_prediction
from libraries import *

def list_of_crops(mean_ndvi, district,area):
    list_of_crops = find_best_crop(
        mean_ndvi, 0.05, crop_mean_ndvi)

    yields = []
    prices = []
    print(list_of_crops)

    for i in range(len(list_of_crops)):
        yields.append(yield_prediction(
            str(list_of_crops[i]), crop_season[str(list_of_crops[i])]))
        prices.append(price_prediction(str(list_of_crops[i]), district))
    res = []
    for i in range(len(list_of_crops)):
        temp = []
        temp.append(list_of_crops[i])
        temp.append(round(yields[i], 2))
        temp.append(prices[i])
        temp.append(round(round(yields[i], 2)*float(area),2))
        if prices[i]=="Price Unavailable":
            temp.append(prices[i])
        else:
            temp.append(round(float(prices[i])*round(round(yields[i], 2)*float(area),2)))
        res.append(temp)

    return res


def find_best_crop(mean_ndvi, standard_dev, crop_mean_ndvi):
    res = []
    # crop_mean_ndvi.get(mean_ndvi, data[min(data.keys(), key=lambda k: abs(k-num))])

    closest = (pd.Series(crop_mean_ndvi) -
               mean_ndvi).abs().sort_values()[:5]
    f = dict(closest)
    res = list(f.keys())

    '''for key,value in crop_mean_ndvi.items():
    if value-standard_dev <= mean_ndvi <= value+standard_dev:
      res.append(key)'''

    return res
