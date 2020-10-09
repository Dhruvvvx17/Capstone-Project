import openpyxl
import os

state = input("Enter state: ")
crop = input("Enter crop: ")

start_year = int(input("Enter start year: "))
end_year = int(input("Enter end year: "))

months_dict = {
    1:  "January",
    2:  "February",
    3:  "March",
    4:  "April",
    5:  "May",
    6:  "June",
    7:  "July",
    8:  "August",
    9:  "September",
    10: "October",
    11: "November",
    12: "December"
}

available_months_num = list(map(int,input("Enter available months [1-12] (space separated): ").split()))
available_months = []

for month in available_months_num:
    available_months.append(months_dict[month])

# Create directory
dirName = f"./Formatted{crop}"
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print(f"Directory {dirName} Created ")
else:    
    print(f"Directory {dirName} already exists")

# Create files
count = 0
for year in range(start_year,end_year+1):
    for month in available_months:
        new_excel_filepath = f"./Formatted{crop}/{state}_{crop}_{year}_{month}.xlsx"
        
        wb = openpyxl.Workbook()
        curr_sheet = wb['Sheet']
        curr_sheet.title = f"{state}_{crop}_{year}_{month}"
        wb.save(new_excel_filepath)
        
        print(f"Created new file {state}_{crop}_{year}_{month}.xlsx")
        count += 1

print(f"Execution complete. {count} new files created.")