import json
import requests
import numpy as np
import matplotlib.pyplot as plt



def process_path(text: str):
    parts = text.split('/')
    if parts[-1] == "":
        parts = parts[:-1]
    return parts[-3], parts[-2], parts[-1]


def download_satellite_image():
    """Send ward params to download"""
 
    url = 'http://127.0.0.1:5000/download_img'
    # params = {
    #     'province': 'Lâm Đồng',
    #     'district': 'Đà Lạt',
    #     'ward':"6",
    #     'lst_img': []
    # }
    # params = {
    #     'province': 'Hồ Chí Minh city',
    #     'district': 'Quận 1',
    #     'ward':"Nguyễn Cư Trinh",
    #     'lst_img': []
    # }
    params = {
        'province': 'Đồng Nai',
        'district': 'Tân Phú',
        'ward':"Phú Lập",
        'lst_img': [],
        'W_num':8
    }
    # params = {
    #     'province': 'Lâm Đồng',
    #     'district': 'Đà Lạt',
    #     'ward':"12",
    #     'lst_img': []
    # }

    # params = {
    #     'province': 'Hồ Chí Minh city',
    #     'district': 'Quận 8',
    #     'ward':"06"
    # }

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
    # params = {
    #     'province': 'Lâm Đồng',
    #     'district': 'Đà Lạt',
    #     'ward':"12"
    # }
    
    # params = {
    #     'province': 'Lâm Đồng',
    #     'district': 'Đà Lạt',
    #     'ward':"6"
    # }

    # params = {
    #     'province': 'Hồ Chí Minh city',
    #     'district': 'Quận 1',
    #     'ward':"Nguyễn Cư Trinh"
    # }
    params = {
        'province': 'Đồng Nai',
        'district': 'Tân Phú',
        'ward':"Phú Lập"
    }
    response = requests.post(url, params=params)
    try:
        data = json.loads(response.content)
        area = data['area']
        area_dict = eval(area)
        # plt.imshow(img, cmap='viridis')
        # plt.colorbar()
        # plt.show()
        print(area_dict)
    except:
        data = response.content
        print(data)


def predict():
    """
    Send APO predict label
    """
    url = 'http://127.0.0.1:5000/predict_data'
    # params = {
    #     'province': 'Lâm Đồng',
    #     'district': 'Đà Lạt',
    #     'ward':"12"
    # }
    # params = {
    #     'province': 'Lâm Đồng',
    #     'district': 'Đà Lạt',
    #     'ward':"6"
    # }
    # params = {
    #     'province': 'Hồ Chí Minh city',
    #     'district': 'Quận 1',
    #     'ward':"Nguyễn Cư Trinh"
    # }
    params = {
        'province': 'Đồng Nai',
        'district': 'Tân Phú',
        'ward':"Phú Lập"
    }
    response = requests.post(url, params=params)
    data = response.content
    print(data)


def custom_calculate_area():
    """
    Send params to calculate area
    """
    url = 'http://127.0.0.1:5000/get_area'

    annotations = "data/annotation/Lâm Đồng/Đà Lạt/12"
    province, district, ward = process_path(text=annotations)

    # dont wanna change, just comment mask
    mask = "data/mask/Hồ Chí Minh city/Quận 1/Nguyễn Cư Trinh"
    province_mask, district_mask, ward_mask = process_path(text=mask)

    params = {
        'province': province,
        'district': district,
        'ward': ward,
        'province_mask': province_mask,
        'district_mask': district_mask,
        'ward_mask': ward_mask
    }
    response = requests.post(url, params=params)
    try:
        data = json.loads(response.content)
        area = data['area']
        area_dict = eval(area)
        print(area_dict)
    except:
        data = response.content
        print(data)

def send_2_text():
    url = 'http://127.0.0.1:5000/get_area'

    annotations = "data/annotations/Lâm Đồng/Đà Lạt/12"
    mask = "data/mask/Hồ Chí Minh city/Quận 1/Nguyễn Cư Trinh"

    params = {
        'annotations': annotations,
        'mask': mask
    }

    response = requests.post(url, params=params)
    try:
        data = json.loads(response.content)
        area = data['area']
        area_dict = eval(area)
        print(area_dict)
    except:
        data = response.content
        print(data)

if __name__=="__main__":
    download_satellite_image()
    predict()
    calculate_area()