import json
import requests
import matplotlib.pyplot as plt


def main():
    response = requests.get('http://127.0.0.1:5000/get_area')
    data = json.loads(response.content)
    img = data['total']
    plt.imshow(img, cmap='viridis')
    plt.colorbar()
    plt.show()

if __name__=="__main__":
    main()