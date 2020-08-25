https://earthdata.nasa.gov/

Points of Importance:

1. Introduction

"...compute an overall measure of relative vegetation health compared to the mean on a per-pixel basis over select subregions in every African country, thus evaluating whether dense farmingareas can be used as representative samples of larger regions to increase computational efficiency. ...it does not depend on special tuning for the particular crop, region, or climate of interest."

"Relatively low-resolution pixels of the Moderate Resolution Imaging Spectroradiometer (MODIS) decrease the amount of data that must be processed, making this system cheaper and more efficient"

"Crop masks are not used in this model"

The goal : "see how well crop yields may be predicted using extremely straightforward methods based on simple averages and differences of common indices over dense farming regions and the resulting correlations"

"The index developed here is similar to Vegetation Condition Index (VCI)"

2. Method:

"Python code was written to obtain satellite images, mask out clouds, calculate vegetation and water indices (VI), compute monthly VI anomalies since 2000, and correlate the anomalies with crop yield anomalies for every county in Illinois, which served as a proof of concept due to large amounts of ground truth data in the US"

"To measure the health of crops throughout the growing season, three VIs were computed:  Normalized Difference Vegetation Index (NDVI), Enhanced Vegetation Index (EVI), and Normalized
Difference Water Index (NDWI). ... these range between -1 to 1"

"Areas containing dense vegetation show high NDVI and EVI values (between 0.4 and 0.8), desert sands will register at about zero, and snow and clouds are negative. All of these VIs are
sensitive to the same biophysical variables (LAI, leaf angle, soil brightness, chlorophyll content, etc.). Although the indices are similar, it is valuable to examine all three, as they may perform differently under various environmental conditions"

Set of formulae on pg 6 and 7

"Annual crop yield data was downloaded for every county in Illinois for 2000–2016 for three crops, corn, soybeans, and sorghum, from USDA county estimate reports available online through Quickstats [1]. These crops were chosen because they are three of the largest food crops in Illinois with 4.5 million, 4.3 million, and 7.3 thousands hectares planted, respectively [57–59]. Because each county has different growing conditions (soil quality, hills, proximity to large water bodies, etc.), the mean was subtracted out of each county’s crop yield to find the yield anomaly, Yield Anomi,y = Yieldi,y − Yieldy"

"Correlations were found between each county’s yield anomaly and the three VIs for five months, May–September. To find the highest possible correlation amongst these variables and months, a multivariate regression was fit to each month and index for a total of 15 variables (5 months × 3 VIs)."

"African crop yields were downloaded from Index Mundi, a comprehensive data portal with country-level statistics compiled from multiple sources, but the production data were originally collected by the USDA Foreign Agricultural Service (FAS)"

"The VI anomalies and averages from these regions were then correlated to national crop production data"

"First, the bands were retrieved from the Descartes Platform. NDVI, EVI, and NDWI were computed, and cloudy pixels were masked out. The climatology for each pixel was subtracted to
obtain monthly anomalies as well as averages of all three indices, resulting six variables for correlation analysis: NDVI average, NDVI anomaly, EVI average, EVI anomaly, NDWI average, and NDWI anomaly (Equations (1)–(4)). Next, correlations were computed between the six indices of the month at the height of the growing season and the crop production. The height of the growing season is defined as the month in the growing season that the NDVI average peaks."


Error formula on page 9

3. Results

"Correlations were computed in Illinois between the anomalies of NDVI, EVI, and NDWI, and three crops: corn, soybeans, and sorghum; all were found to have high correlations"

"It was found that NDVI and EVI both have positive relationships to crop yields, while NDWI is inversely related. This is because the NDWI formulation includes a negative NIR, while NDVI and EVI have positive NIR values."
