import json
import requests
import numpy as np
import matplotlib.pyplot as plt

def download_satellite_image():
    """Send ward params to download"""
 
    url = 'http://127.0.0.1:5000/download_img'
    params = {
        'province': 'Lâm Đồng',
        'district': 'Đà Lạt',
        'ward':"12"
    }
    response = requests.post(url, params=params)
    try:
        data = json.loads(response.content)
        print(data)
    except:
        data = response.content
        print(data)

def calculate_area():
    """
    Send params to calculate area
    """
    url = 'http://127.0.0.1:5000/get_area'
    params = {
        'province': 'Lâm Đồng',
        'district': 'Đà Lạt',
        'ward':"12"
    }
    response = requests.get(url, params=params)
    try:
        data = json.loads(response.content)
        # img = data['img']
        area = data['area']
        area_dict = eval(area)
        # plt.imshow(img, cmap='viridis')
        # plt.colorbar()
        # plt.show()
        print(area_dict)
    except:
        data = response.content
        print(data)

if __name__=="__main__":
    download_satellite_image()