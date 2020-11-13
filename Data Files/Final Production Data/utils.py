"""
Helper functions for directory and file management operations
"""

import os
import csv

def getInputDirectory(stage):
    ip_dir = input(f"Enter input directory name (Directory containing files for {stage} preprocessing): ")
    if not os.path.exists(ip_dir):
        print(f"Directory {ip_dir} does not exist.")
        print("No data preprocessed.\nExiting\n")
        exit(0)
    else:
        return ip_dir


def getOutputFileName(stage):
        output_file = input(f"Enter output file name (File to store results of {stage} processing): ")
        if not output_file[-4:] == ".csv":
            output_file += ".csv"
        return output_file


def getOutputDirectory(stage):
    op_dir = input(f"Enter output directory name (Directory to save the {stage} processing results): ")
    return op_dir


def createDirectory(directory_path):
    # Check if directory already exists
    # If not then create directory
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created {directory_path}")
        return True

    # Else, check if directory is empty
    else:
        files = os.listdir(path=directory_path)
        file_count = len(files)

        # If not empty
        if file_count>0:
            print(f"Directory {directory_path} exists but is not empty.")
            clear = input(f"Clear {directory_path} contents? [Y/N]: ")

            # If user allows to clear the directory, then os.remove() all files.
            if(clear.lower()=="y" or clear.lower()=="yes"):
                for file in files:
                    os.remove(f"{directory_path}/{file}")
                print(f"Directory {directory_path} cleared.")
                return True

            # else.. exit program
            else:
                print("Cannot proceed with a non-empty directory.\nExiting\n")
                return False
        
        # Else, as it exists and is empty
        return True


def createFile(file_path,headers):
    with open(file_path,"w",newline='') as fileObj:
        # Insert header
        file_writer = csv.writer(fileObj)
        file_writer.writerow(headers)
    print(f"{file_path} created.")
    

def appendToFile(file_path,new_entry):
    with open(file_path,'a+',newline='') as fileObj:
        file_writer =  csv.writer(fileObj)
        file_writer.writerow(new_entry)

def appendToFileList(file_path,list_of_entries):
    with open(file_path,'a+',newline='') as fileObj:
        file_writer =  csv.writer(fileObj)
        for entry in list_of_entries:
            file_writer.writerow(entry)