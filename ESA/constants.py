
crop_mean_ndvi = {'Arecanut': 0.6885986394557823, 'Arhar/Tur': 0.6467540983606557, 'Bajra': 0.6161650165016501, 'Banana': 0.630200364298725, 'Cashewnut': 0.6929398692810458,
                  'Castor seed': 0.6334563106796116, 'Coriander': 0.6378419243986255, 'Cotton(lint)': 0.627745275888133, 'Cowpea(Lobia)': 0.6494590075512405, 'Dry chillies': 0.6435831586303284, 'Garlic': 0.6217345679012346, 
                  'Ginger': 0.6882848699763593, 'Gram': 0.650679292929293, 'Groundnut': 0.588268106162843, 'Horse-gram': 0.6618145048814504, 'Jowar': 0.63003081232493, 'Linseed': 0.9228436911487759, 'Maize': 0.6617493261455526,
                   'Moong(Green Gram)': 0.6659833333333334, 'Niger seed': 0.6421964285714286, 'Onion': 0.9229966216216216, 'Potato': 0.6413771043771044, 'Ragi': 0.6923896231032795, 'Rapeseed &Mustard': 0.6300160818713451,
                    'Rice': 0.6953418530351438, 'Safflower': 0.6282302737520129, 'Sannhamp': 0.6350303030303031, 'Sesamum': 0.6567513661202184, 'Small millets': 0.6505491698595148, 'Soyabean': 0.6430725623582766, 'Sugarcane': 0.6700593220338983, 'Sunflower': 0.6393148148148148, 'Sweet potato': 0.6832024353120243, 'Tobacco': 0.6582823315118398, 'Turmeric': 0.6674200244200245, 'Urad': 0.6674145043246839, 'Wheat': 0.6183536776212833, 'Peas & beans (Pulses)': 0.6533303303303303}

crop_season = {'Arecanut': 'Whole Year', 'Arhar/Tur': 'Kharif', 'Bajra': 'Kharif', 'Banana': 'Whole Year', 'Black pepper': 'Whole Year', 'Cashewnut': 'Whole Year', 'Castor seed': 'Kharif', 'Coriander': 'Whole Year', 'Cotton(lint)': 'Whole Year',
               'Cowpea(Lobia)': 'Kharif', 'Dry chillies': 'Kharif', 'Garlic': 'Whole Year', 'Ginger': 'Whole Year', 'Gram': 'Rabi', 'Groundnut': 'Kharif', 'Horse-gram': 'Kharif', 'Jowar': 'Kharif', 'Linseed': 'Rabi', 'Maize': 'Kharif', 'Mesta': 'Whole Year', 'Moong(Green Gram)': 'Kharif',
               'Niger seed': 'Kharif', 'Onion': 'Kharif', 'Potato': 'Kharif', 'Ragi': 'Kharif', 'Rapeseed &Mustard': 'Rabi', 'Rice': 'Kharif', 'Safflower': 'Rabi', 'Sannhamp': 'Whole Year', 'Sesamum': 'Kharif', 'Small millets': 'Kharif', 'Soyabean': 'Kharif', 'Sugarcane': 'Whole Year',
               'Sunflower': 'Kharif', 'Sweet potato': 'Whole Year', 'Tapioca': 'Whole Year', 'Tobacco': 'Whole Year', 'Turmeric': 'Whole Year', 'Urad': 'Kharif', 'Wheat': 'Rabi', 'Cardamom': 'Whole Year', 'Peas & beans (Pulses)': 'Rabi'}
default_prices = { 
"Chitradurga" : {"Arecanut": "39507", "Arhar/Tur": "5600" ,"Bajra": "1426" ,"Cotton(lint)": "5400","Garlic": "7167","Ginger": "4056" , "Groundnut": "4978", "Maize": "1280" ,"Ragi": "1950" ,"Rice": "2890","Sweet potato": "1256","Wheat": "1876" ,"Cashewnut": "80108"},
"Davangere"   : {"Arecanut": "35126", "Arhar/Tur": "4508","Bajra": "1400", "Cotton(lint)": "4661","Garlic": "7768","Ginger": "3801", "Groundnut":"4081", "Maize": "1221","Ragi": "1480","Rice": "2258","Sweet potato": "1398","Wheat": "1432" ,"Cashewnut": "69964"},
"Koppal"   : {"Arecanut": "35156", "Arhar/Tur": "4518","Bajra": "1460", "Cotton(lint)": "4761","Garlic": "7798","Ginger": "3800", "Groundnut":"4041", "Maize": "1251","Ragi": "1580","Rice": "2558","Sweet potato": "1798","Wheat": "1832" ,"Cashewnut": "69974"},      
"Dharwad"     : {"Arecanut": "35126", "Arhar/Tur": "4000" ,"Bajra":"1423" ,"Cotton(lint)": "4986" ,"Garlic": "7516","Ginger": "4007" , "Groundnut": "4150", "Maize": "1309" ,"Ragi": "1967","Rice": "2371","Sweet potato": "1400","Wheat": "2708" ,"Cashewnut": "71763" },
"Gulbarga"    : {"Arecanut": "36090", "Arhar/Tur": "4489","Bajra": "1295","Cotton(lint)": "6104","Garlic": "5565","Ginger": "1225", "Groundnut": "4804", "Maize": "1398","Ragi":"1850" ,"Rice": "3155" ,"Sweet potato": "1382","Wheat": "1996","Cashewnut": "70050" },   
"Hassan"      : {"Arecanut": "36090" ,"Arhar/Tur": "4710","Bajra": "1247" ,"Cotton(lint)": "5156","Garlic": "5616","Ginger": "1371" , "Groundnut": "4999", "Maize": "1333","Ragi": "1968","Rice": "2012","Sweet potato": "1174","Wheat": "1224","Cashewnut": "68994" },       
"Hubli"       : {"Arecanut": "36090", "Arhar/Tur": "4120" ,"Bajra": "1200","Cotton(lint)":"5476" ,"Garlic": "7111","Ginger": "3998" , "Groundnut": "4872", "Maize": "1478","Ragi": "1405","Rice": "2315","Sweet potato": "1113","Wheat": "2601" ,"Cashewnut": "58070"},      
"Kolar"       : {"Arecanut": "36090", "Arhar/Tur": "4820","Bajra": "1294" ,"Cotton(lint)": "4867","Garlic": "7234","Ginger": "3863", "Groundnut": "4493", "Maize": "1296","Ragi": "1898","Rice": "2290","Sweet potato": "1250","Wheat": "2200" ,"Cashewnut": "65003" },     
"Madhugiri"   : {"Arecanut": "36090", "Arhar/Tur": "5551" ,"Bajra": "1133" ,"Cotton(lint)": "5305","Garlic": "8106","Ginger": "3563" , "Groundnut": "4760", "Maize":"1534" ,"Ragi": "2109","Rice": "2678","Sweet potato": "1386" ,"Wheat":"1722" ,"Cashewnut": "80010"  },   
"Madekeri"    : {"Arecanut": "36090", "Arhar/Tur": "4411","Bajra": "1278", "Cotton(lint)": "6897" ,"Garlic": "5642","Ginger": "1317", "Groundnut":"4765", "Maize":"1399" ,"Ragi": "2568" ,"Rice": "2450" ,"Sweet potato": "1179" ,"Wheat":"1327"  ,"Cashewnut": "79004"},   
"Mangalore"   : {"Arecanut": "26337" , "Arhar/Tur": "6000" ,"Bajra": "1151","Cotton(lint)": "4892","Garlic": "4050","Ginger": "1569", "Groundnut": "5060", "Maize":"1338" ,"Ragi": "2778","Rice": "2240","Sweet potato": "1486","Wheat": "1621" ,"Cashewnut": "60040"},   
"Raichur"     : {"Arecanut": "36090", "Arhar/Tur": "5509","Bajra": "1472","Cotton(lint)":"4901" ,"Garlic": "7005","Ginger": "2557" , "Groundnut": "4536", "Maize": "1379","Ragi": "2436","Rice": "3098","Sweet potato": "1378","Wheat": "2420" ,"Cashewnut": "140700"},       
"Shimoga"     : {"Arecanut": "38769", "Arhar/Tur": "5892","Bajra": "1149" ,"Cotton(lint)": "5176" ,"Garlic": "8163","Ginger": "2528" , "Groundnut": "4267", "Maize": "1301" ,"Ragi": "2670" ,"Rice": "4080","Sweet potato": "1473","Wheat":  "2786","Cashewnut": "68343"},       
"Tumkur"      : {"Arecanut": "39648", "Arhar/Tur": "5994" ,"Bajra": "1085","Cotton(lint)": "5485" ,"Garlic": "4566","Ginger": "4757", "Groundnut": "4198", "Maize": "1592","Ragi": "1934","Rice": "4202","Sweet potato": "1667","Wheat": "2588" ,"Cashewnut": "77080"} ,    
"Udupi"       : {"Arecanut": "36090", "Arhar/Tur": "6021","Bajra": "1193" ,"Cotton(lint)": "5198","Garlic": "8120","Ginger": "2840", "Groundnut": "4418", "Maize": "1538" ,"Ragi": "2598","Rice":"3671" ,"Sweet potato": "1840" ,"Wheat": "1986"  ,"Cashewnut": "68005"},     
"Bangalore"   : {"Arecanut": "36090", "Arhar/Tur": "6100","Bajra": "1909" ,"Cotton(lint)": "6485","Garlic": "10074","Ginger": "5490" , "Groundnut": "6516", "Maize":"1672" ,"Ragi": "3200" ,"Rice": "4212" ,"Sweet potato": "1778" ,"Wheat": "2689" ,"Cashewnut": "70280"}}
india_modis_grid_coordinates = {
    "north_east_hdf": {
        "long_upper_left":  92.0544,
        "lat_upper_left":  30.0438
    },
    "south_hdf": {
        "long_upper_left": 74.2034,
        "lat_upper_left": 20.0210
    }
}

listOfCrops=['Arecanut' , 'Arhar/Tur' , 'Bajra' , 'Banana' , 'Black pepper' , 'Cashewnut',
 'Castor seed' , 'Coconut ' , 'Coriander' , 'Cotton(lint)' , 'Cowpea(Lobia)',
 'Dry chillies' , 'Garlic' , 'Ginger' , 'Gram' , 'Groundnut' , 'Horse-gram' , 'Jowar',
 'Linseed' , 'Maize' , 'Mesta' , 'Moong(Green Gram)' , 'Niger seed' , 'Onion',
 'Other  Rabi pulses' , 'Other Kharif pulses' , 'Peas & beans (Pulses)',
 'Potato' , 'Ragi' , 'Rapeseed &Mustard' , 'Rice' , 'Safflower' , 'Sannhamp',
 'Sesamum' , 'Small millets' , 'Soyabean' , 'Sugarcane' , 'Sunflower',
 'Sweet potato' , 'Tobacco' , 'Turmeric' , 'Urad' , 'Wheat']