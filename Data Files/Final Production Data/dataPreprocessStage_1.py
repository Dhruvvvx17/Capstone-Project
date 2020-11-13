"""
This program creates Crop-District-Year-Month tuples over the available time range
"""

import os
import csv
import pandas as pd
import math
import utils


if __name__ == "__main__":

    # Get input directory
    input_dir = utils.getInputDirectory("stage-1")

    # Get output directory
    output_dir = utils.getOutputDirectory("stage-1")
    # Create output directory
    if not(utils.createDirectory(output_dir)):
        exit(0)
    
    # List of files to preprocess
    files = os.listdir(path=input_dir)
    # To keep track of files processed
    file_count = 0      

    # Iterating over input csv files
    for file in files:

        # Get output file name
        output_file = file
        # Create output file
        output_path = f"{output_dir}/{output_file}"
        headers = ["District","Crop","Year","Season","Area(Hectare)","Production(Tonnes)","Yield"]
        utils.createFile(output_path,headers)

        # Complete path of every file to process
        path = f"{input_dir}/{file}"

        # Extract the district details from file name
        # To remove the ".csv" extension ie; last 4 characters
        district = file[:-4]     


        # Skip first 3 rows
        df = pd.read_csv(path,skiprows = 2) 
        # Rename columns
        new_df = df.rename(columns={'State/Crop/District':'Crop', 'Area (Hectare)':'Area','Production (Tonnes)':'Production', 'Yield (Tonnes/Hectare)':'Yield'})


        # Helper variables
        # current_crop and current_year
        current_crop = ""
        current_year = ""
        skipFirstRow = True

        # Iterating over the dataframes
        for index,row in new_df.iterrows():

            if(skipFirstRow):
                skipFirstRow = False

            elif(row['Season']=="Total"):
                pass

            else:
                # New crop
                if not(pd.isna(row['Crop'])):

                    if(row['Crop'][:5] == "Total"):
                        pass

                    # elif(row['Crop'] == f'1.BANGALORE RURAL'):
                    elif(row['Crop'] == f' 1.{district.upper()}'):
                        if not(pd.isna(row['Year'])):
                            current_year = row['Year']

                        new_entry = [district, current_crop, current_year, row['Season'], row['Area'], row['Production'], row['Yield']]
                        utils.appendToFile(output_path,new_entry)

                    else:
                        current_crop = row['Crop']

                # Continuing with previous crop
                else:
                    if not(pd.isna(row['Year'])):
                        current_year = row['Year']

                    new_entry = [district, current_crop, current_year, row['Season'], row['Area'], row['Production'], row['Yield']]
                    utils.appendToFile(output_path,new_entry)

        # No new crop found, exit loop.
        
        # End of processing for the current file
        file_count += 1
        print(f"{file} processed.")

    # End of processing for all input files
    print(f"\n{file_count} files processed.\nStage-1 execution complete.\n")