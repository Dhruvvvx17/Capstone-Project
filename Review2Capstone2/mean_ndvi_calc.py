from libraries import np


def mean_ndvi_calc(region_of_interest):
    mean_ndvi = 0
    for i in range(40):
        mean_ndvi += np.mean(region_of_interest[i][:])

    mean_ndvi /= 40
    return mean_ndvi
