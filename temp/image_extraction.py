from libraries import *
from constants import india_modis_grid_coordinates


def extraction(filename, lat_in, long_in):

    print("Converting HDF to numpy array...")
    '''Convert HDF to numpy arrays using pyhdf'''
    file = SD(filename, SDC.READ)

    # select the NDVI dataset from HDF file
    ndvi_obj = file.select('250m 16 days NDVI')
    ndvi_numpy_ndarray = ndvi_obj.get()

    normalized_ndvi_ndarray = ndvi_numpy_ndarray / 10000

    print("Normalized NDVI array: \n", normalized_ndvi_ndarray)

    # extract the 10x10sqkm area around the given latitude and longitude
    latitude_input = math.floor(float(lat_in))
    longitude_input = math.floor(float(long_in))

    # Hard-coded values for north east india MODIS image

    # could be a diff file:

    long_upper_left = india_modis_grid_coordinates["south_hdf"]["long_upper_left"]
    lat_upper_left = india_modis_grid_coordinates["south_hdf"]["lat_upper_left"]

    long_diff = abs(long_upper_left - longitude_input)
    lat_diff = abs(lat_upper_left - latitude_input)

    # Calculate distance
    # long_dist_kms is kilometers per longitude
    long_dist_kms = (2 * math.pi / 360) * 6378 * \
        math.cos(math.radians(latitude_input))
    lat_dist_kms = 111

    displacement_right_kms = long_diff * abs(long_dist_kms)
    displacement_down_kms = lat_diff * lat_dist_kms

    print("Displacement in kms Down:", displacement_down_kms,
          " Right: ", displacement_right_kms)

    # Calculate Pixels
    displacement_right_pixels = displacement_right_kms * 4
    displacement_down_pixels = displacement_down_kms * 4

    print("Displacement in pixels Down:", displacement_down_pixels,
          " Right: ", displacement_right_pixels)

    slice_point_top_left_x = math.floor(displacement_right_pixels - 20)
    slice_point_top_left_y = math.floor(displacement_down_pixels - 20)

    print("Slice point x:", slice_point_top_left_x,
          " y: ", slice_point_top_left_y)

    region_of_interest = normalized_ndvi_ndarray[slice_point_top_left_x: slice_point_top_left_x +
                                                 40, slice_point_top_left_y: slice_point_top_left_y + 40]

    print(region_of_interest)
    print(np.shape(region_of_interest))

    '''Save numpy array as PNG'''
    ndvi_image = Image.fromarray(
        np.uint8(cm.gist_earth(region_of_interest)*255))
    ndvi_image.save("roi.png")
    ndvi_image = Image.fromarray(
        np.uint8(cm.gist_earth(normalized_ndvi_ndarray)*255))
    ndvi_image.save("entire_image.png")

    return region_of_interest
