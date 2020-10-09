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

    # Get input directory
    input_dir = utils.getInputDirectory("stage-2")

    # Get output directory
    output_dir = utils.getOutputDirectory("stage-2")
    # Create output directory
    if not(utils.createDirectory(output_dir)):
        exit(0)

    # Enter crop name for current processing
    crop = input("Enter crop name: ")

    # To store all district-crop pairs with values as [year,month,production,price]
    district_crop_pairs = {}

    # Stage-1 output
    stage_1_csv_path = f"{input_dir}/{os.listdir(path=input_dir)[0]}"

    # Create dataframe
    stage_1_csv = pd.read_csv(stage_1_csv_path)
    # Rename columns
    stage_1_csv = stage_1_csv.rename(columns={'Production(Tonnes)':'Production','Mean Price(Rs./Quintal)':'Price'})
    
    # Iterating over the dataframes
    for index,row in stage_1_csv.iterrows():
        
        # Extract all metadata from 'district' column
        district,year,monthNum,month = row['District'].split("_")

        # Insert the value in district-crop pair dictionary
        if district not in district_crop_pairs:
            district_crop_pairs[district] = []
            district_crop_pairs[district].append( [ year, month, row['Production'], row['Price'] ] )
        else:
            district_crop_pairs[district].append( [ year, month, row['Production'], row['Price'] ] )

    # variables to keep track of file processing
    successful_processing = 0
    failed_processing = 0

    # Iterating over district-crop dictionary
    for key,values in district_crop_pairs.items():

        # New file name is the "currentCrop"_"currentDistrict".csv
        new_file_name = f"{crop}_{key}.csv"
        new_file_path = f"{output_dir}/{new_file_name}"

        # Check if file already exists
        if(os.path.isfile(new_file_path)):
            print(f"File {new_file_name} already exists in {output_dir}.")
            print(f"Skipping data preprocessing stage-2 for {key}.")
            failed_processing += 1

        else:
            headers = ["Year","Month","Production(Tonnes)","MeanPrice(Rs./Quintal)"]
            # Create a file with given headers
            utils.createFile(new_file_path,headers)
            # Append all the dict values as row entries to the new file
            utils.appendToFileList(new_file_path,values)
            
            # Success message 
            print(f"{new_file_path} data processing complete.")
            successful_processing += 1

        # End of current file processing

    # End of all file processing 
    print(f"\n{successful_processing} files processed successfully.")
    print(f"{failed_processing} files failed.\nStage-2 execution complete.\n")
