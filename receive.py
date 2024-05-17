import json
import requests
import numpy as np
import matplotlib.pyplot as plt


def main():
    url = 'http://127.0.0.1:5000/get_area'
    params = {
        'x1': 0,
        'y1': 12000,
        'x2': 2000,
        'y2': 10000
    }
    response = requests.get(url, params=params)

    data = json.loads(response.content)
    img = data['img']
    area = data['area']
    area_dict = eval(area)
    plt.imshow(img, cmap='viridis')
    plt.colorbar()
    plt.show()
    print(area_dict)

if __name__=="__main__":
    main()