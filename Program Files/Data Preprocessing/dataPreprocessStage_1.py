"""
This program creates Crop-District-Year-Month tuples over the available time range
"""

import os
import csv
import pandas as pd
import math
import utils

def resetVariables():
    current_district = ""
    total_production = 0
    mean_price = 0
    total_entries = 0
    return(current_district, total_production, mean_price, total_entries)


def validValues(production,price):

    if(production.isnumeric() and price.isnumeric()):
        # print("Valid",price,production,type(price),type(production))
        return True
    else:
        try:
            production = float(production)
            price = float(price)
            if math.isnan(production) or math.isnan(price):
                raise Exception("Nan value found.")
            # print("Valid",price,production,type(price),type(production))
            return True
        except:
            # print("inValid",price,production,type(price),type(production))
            return False


if __name__ == "__main__":

    # Get input directory
    input_dir = utils.getInputDirectory("stage-1")

    # Get output directory
    output_dir = utils.getOutputDirectory("stage-1")
    # Create output directory
    if not(utils.createDirectory(output_dir)):
        exit(0)

    # Get output file name
    output_file = utils.getOutputFileName("stage-1")
    # Create output file
    output_path = f"{output_dir}/{output_file}"
    headers = ["District","Production(Tonnes)","Mean Price(Rs./Quintal)"]
    utils.createFile(output_path,headers)
    
    # List of files to preprocess
    files = os.listdir(path=input_dir)
    # To keep track of files processed
    file_count = 0      

    # Iterating over input csv files
    for file in files:

        # Complete path of every file to process
        path = f"{input_dir}/{file}"

        # Extract the details from file name
        state,crop,year,monthNum,month = file.split('_')        
        # To remove the ".csv" extension ie; last 4 characters
        month = month[:-4]

        # Skip first 3 columns
        df = pd.read_csv(path, skiprows = 3) 
        # Drop the unnecessary rows
        new_df = df.drop(['Arrival Date','Variety','Minimum Price(Rs./Quintal)','Maximum Price(Rs./Quintal)'],axis=1)
        # Rename columns
        new_df = new_df.rename(columns={'Market':'District','Arrivals (Tonnes)':'Production','Modal Price(Rs./Quintal)':'Price'})


        # Helper variables
        current_district, total_production, mean_price, total_entries = resetVariables()
        isFirstDistrict = True

        # Iterating over the dataframes
        for index,row in new_df.iterrows():

            # New district
            if not(pd.isna(row['District'])):
                # Check if this is the first district of this new file [Border case]
                if(isFirstDistrict):
                    current_district = row['District']
                    isFirstDistrict = False
                    # Check if production and price values are numeric or NR
                    if(validValues(str(row['Production']),str(row['Price']))):
                        # Update helper variable values
                        total_production += int(row['Production'])
                        mean_price += int(row['Price'])
                        total_entries += 1

                else:
                    # A new district is found.
                    # Write the computed data for the previous district in the output csv file
                    
                    # To avoid division by 0 error
                    if not(total_entries==0):
                        mean_price /= total_entries
                        mean_price = round(mean_price)
                        current_district = current_district+"_"+year+"_"+monthNum+"_"+month
                        new_entry = [current_district, total_production, mean_price]

                        utils.appendToFile(output_path,new_entry)

                    # Reset the helper variables
                    current_district, total_production, mean_price, total_entries = resetVariables()
                    current_district = row['District']
                    if(validValues(str(row['Production']),str(row['Price']))):
                        total_production += int(row['Production'])
                        mean_price += int(row['Price'])
                        total_entries += 1

            # Continuing with previous district
            else:
                if(validValues(str(row['Production']),str(row['Price']))):
                    total_production += int(row['Production'])
                    mean_price += int(row['Price'])
                    total_entries += 1


        # No new district found, exit loop.

        # Append the last districts' production and price to output csv file
        if not(total_entries==0):
            mean_price /= total_entries
            mean_price = round(mean_price)
            current_district = current_district+"_"+year+"_"+monthNum+"_"+month
            new_entry = [current_district, total_production, mean_price]

            utils.appendToFile(output_path,new_entry)

        
        # End of processing for the current file
        file_count += 1
        print(f"{file} processed.")

    # End of processing for all input files
    print(f"\n{file_count} files processed.\nStage-1 execution complete.\n")