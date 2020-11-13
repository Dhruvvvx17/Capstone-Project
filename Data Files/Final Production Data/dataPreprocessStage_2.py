"""
This program converted the stage-1 output (district_year_month) values for a particular crop
to (year_month) value for every district-crop pair.
A new file is generated for every district-crop pair.
"""

import os
import csv
import pandas as pd
import math
import utils


if __name__ == "__main__":

    # Get input first directory
    input_dir_data = utils.getInputDirectory("stage-2")

    # Get input second directory
    input_dir_ndvi = utils.getInputDirectory("stage-2")


    # Get output directory
    output_dir = utils.getOutputDirectory("stage-2")
    # Create output directory
    if not(utils.createDirectory(output_dir)):
        exit(0)

    # Stage-1 output
    # List of files to preprocess
    files_data = os.listdir(path=input_dir_data)
    files_ndvi = os.listdir(path=input_dir_ndvi)

    # To keep track of files processed
    file_count = 0      

    # Iterating over input csv files
    for file in files_data:

        # Complete path of every file to process
        stage1_csv_path = f"{input_dir_data}/{file}"

        # district name
        district_name = file[:-4].upper()

        # Get output file name
        output_file = file
        # Create output file
        output_path = f"{output_dir}/{output_file}"
        headers = ["District","Crop","Year","Season","Area(Hectare)","Production(Tonnes)","Yield","JANUARY_NDVI","FEBRUARY_NDVI","JUNE_NDVI","JULY_NDVI","AUGUST_NDVI","SEPTEMBER_NDVI","OCTOBER_NDVI","NOVEMBER_NDVI","DECEMBER_NDVI"]
        utils.createFile(output_path,headers)

        # Create dataframe
        data_df = pd.read_csv(stage1_csv_path)
        
        # Years df
        years_in_data_df = data_df[['Year']] 


        for ndvi_file in files_ndvi:
            state,monthNum,month = ndvi_file.split("_")
            month = month[:-4].upper()

            ndvi_csv_path = f"{input_dir_ndvi}/{ndvi_file}"
            # create dataframe
            ndvi_df = pd.read_csv(ndvi_csv_path, skiprows=1)
            ndvi_df = ndvi_df.rename(columns={'district':'years'})

            # Iterating over the Transposed NDVI File
            year_district_df = ndvi_df[['years',district_name]]

            # year-ndvi dictionary
            year_ndvi_dict = {}

            # Iterate over 'year_district_df' rows
            for index,row in year_district_df.iterrows():
                # Add new K-V pair to dictionary 
                key = (row['years'].strip()).replace('_','-')
                year_ndvi_dict[ key ] = row[district_name]
            # Dictionary of 13 values  (2006 - 2020) created

            # Python list, later added to the DF as a new column
            ndvi_value_column = []

            # Populating the column list
            for index,row in years_in_data_df.iterrows():

                if row['Year'].strip() in year_ndvi_dict:
                    ndvi_value_column.append( year_ndvi_dict[ row['Year'].strip() ] )
                else:
                    ndvi_value_column.append( -100 )


            # Append the list as new columns
            data_df[f'{month}_NDVI'] = ndvi_value_column


        data_df.to_csv(output_path)

        file_count += 1
        print(f"{file} processed.")

    # End of processing for all input files
    print(f"\n{file_count} files processed.\nStage-2 execution complete.\n")