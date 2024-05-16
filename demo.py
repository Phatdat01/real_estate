from flask import Flask
from flask_cors import CORS

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from render_report import *

app = Flask(__name__)
CORS(app)
mask = np.load('mask.npy').reshape(14598, 15408)


def merge_large_img():
    folder_path = "annotations"
    index1=[i for i in range(56,64)]
    index2=[i for i in range(48,56)]
    index3=[i for i in range(40,48)]
    index4=[i for i in range(32,40)]
    index5=[i for i in range(24,32)]
    index6=[i for i in range(16,24)]
    index7=[i for i in range(8,16)] 
    index8 = np.arange(7, -1, -1)
    index = [index1, index2, index3, index4, index5, index6, index7, index8]
    big_images=merging_row(index[0], folder_path=folder_path)
    for i in index[1:]:
        image=merging_row(i, folder_path=folder_path)
        big_images = np.concatenate((big_images, image))
    return big_images

def get_area_total():
    print(calculate_area(big_images, mask))
    unique_values, counts = np.unique(mask, return_counts=True)
    print(unique_values, counts)
    total_sum = sum(calculate_area(big_images, mask).values())
    return total_sum


def sub(image: np.ndarray,x1:int, y1:int, x2:int, y2:int)-> np.ndarray:
    submatrix = [row[x1:x2] for row in image[y2:y1]]
    resized_submatrix = np.resize(submatrix,(y1 - y2, x2 - x1))
    return resized_submatrix

def calculate(matrix: np.ndarray):
    ## Just True point
    count = np.count_nonzero(matrix)
    area = count*0.3**2
    print(area)
    ## All point
    rows, cols = matrix.shape
    print(rows*cols*0.3**2)

def main(x1: int, x2:int,y1:int,y2:int):
    # mask = np.load('mask.npy')
    # # rotated_image = image.rotate(-90).resize(mask.shape).transpose(Image.FLIP   _LEFT_RIGHT)
    # # image_array = np.array(rotated_image)
    # matrix = sub(image=mask, x1=x1, y1=y1,x2=x2,y2=y2)
    # # img = sub(image=image_array, x1=0,y1=12000,x2=2000,y2=10000)
    # # calculate_area(image=img, mask=matrix)
    # calculate(matrix=matrix)
    # plt.pcolormesh(matrix, cmap="binary")
    # plt.xlabel("X-axis")
    # plt.ylabel("Y-axis")
    # plt.title("2D Array Visualization")
    # plt.show()
    get_total_area = get_area_total()
    return {"statistic": get_total_area}
    

@app.route('/get_area', methods=['GET'])
def get_area():
    json_data = main(x1=0, y1=12000,x2=2000,y2=10000)
    return json_data


big_images = merge_large_img()

if __name__=="__main__":
    app.run(debug=True)