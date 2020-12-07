# from constants import crop_mean_ndvi, crop_season
import requests

from pyhdf.SD import SD, SDC
from PIL import Image
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import minmax_scale as scale
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import cv2
import os
import pandas as pd
import math
from sklearn.neighbors import NearestNeighbors
from keras.models import Sequential
from keras.layers import Dense,  LSTM
from keras import metrics
