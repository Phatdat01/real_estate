import numpy as np
import geopandas as gpd
from typing import List
import matplotlib.pyplot as plt
from geo_func import split_polygon, read_geopandas_data

def get_npy(province: str, district: str, ward: str):
    geo= read_geopandas_data(province=province, district=district, ward=ward)
    G = np.random.choice(geo.geometry.values)
    return G

def get_custom_image(province: str, district: str, ward: str, lst_img: List[int] = []):
    G = get_npy(province=province, district=district, ward=ward)
    squares   = split_polygon(G,shape='square',thresh=0,side_length=0.005)
    if len(lst_img) > 0:
        lst_squares = [squares[i] for i in lst_img]
    else:
        lst_squares = squares
    geo_series = gpd.GeoSeries(lst_squares)

    # # Create a figure and an axes object.
    # fig, ax = plt.subplots()
    # # Display the GeoSeries object on the axes object.
    # geo_series.plot(color = 'red', ax=ax)
    # geo.exterior.plot(color='blue', ax= ax)
    # plt.show()
    return geo_series