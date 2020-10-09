import os 
import sys
  
directory = sys.argv[1]

months_dict = {
    "January" : 1,
    "February" : 2,
    "March" : 3,
    "April" : 4,
    "May": 5,
    "June" : 6,
    "July" : 7,
    "August" : 8,
    "September" : 9,
    "October" : 10,
    "November" : 11,
    "December" : 12
}

for file in os.listdir(directory): 
    src = file
    print(src)
    if src[-4:] == '.xls':
        state,crop,year,month = src.split('_')
        month = month[:-4]
        dst = state+"_"+crop+"_"+year+"_"+str(months_dict[month])+"_"+month+".xls"
        os.rename(directory+"/"+src,directory+"/"+dst)  