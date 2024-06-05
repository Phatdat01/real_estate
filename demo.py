import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from flask import Flask, jsonify, request
from flask_cors import CORS

from image_downloading import run
from render_report import calculate_area, merging_row
from Satellite_Image_Collector import get_custom_image, get_npy

app = Flask(__name__)
CORS(app)

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

## Download Images
@app.route("/download_img", methods=['POST'])
def download_img():
    params = request.args
    if params:
        data = {
            key: [int(x) for x in params.getlist(key)] if key == 'lst_img' else params[key]
            for key in params
        }
        province = data['province']
        district = data['district']
        ward = data['ward']
        lst_img = data['lst_img']
        geo_series = get_custom_image(province=province, district=district, ward=ward, lst_img=lst_img)
        
        for idx, bound in enumerate(geo_series):
            try:
                run(idx=lst_img[idx],bound=bound.bounds)
            except:
                run(idx=idx,bound=bound.bounds)
        return "Done"
    else:
        return "You doesn't send ward information!"


@app.route('/get_area', methods=['GET'])
def get_area():
    params = request.args.to_dict()
    if params:
        data = {key: value for key, value in params.items()}
        mask = get_npy(province=data['province'], district=data['district'], ward=data['ward'])
        new_mask = np.rot90(mask, k=1)
        # Change link img
        big_images = merge_large_img()
        big_images[new_mask == False] = 0  
        
        area = calculate_area(image=big_images, mask=new_mask)
        return jsonify({"img":big_images.tolist(), 'area': str(area)})
    else:
        return "Successfull Start!"

if __name__=="__main__":
    app.run(debug=True)