import os
import csv
import pandas as pd
import utils


if __name__ == "__main__":

    # Get input first directory
    input_dir = utils.getInputDirectory("NDVI Files")

    # Get output directory
    output_dir = utils.getOutputDirectory("NDVI Formatted Files")
    # Create output directory
    if not(utils.createDirectory(output_dir)):
        exit(0)


    ndvi_files = os.listdir(path=input_dir)

    for file in ndvi_files:

        input_path = f"{input_dir}/{file}"
        output_path = f"{output_dir}/{file}"

        df = pd.read_csv(input_path,skiprows = 1)
        new_df = df.drop(["state_name","2020_21"],axis=1)

        transposed_df = new_df.T

        transposed_df.to_csv(output_path)