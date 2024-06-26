import os
import cv2
import json
import torch
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from flask import Flask, jsonify, request
from flask_cors import CORS

from Satellite_Image_Collector import check_json
from image_downloading import run, check_dir_tree
from render_report import calculate_area, merging_row
from Satellite_Image_Collector import get_custom_image, get_npy, save_npy, read_size

app = Flask(__name__)
CORS(app)

# import torch
from mmengine.model.utils import revert_sync_batchnorm
from mmseg.apis import init_model, inference_model, show_result_pyplot
config_file = 'segformer_mit-b5_8xb2-160k_loveda-640x640.py'
checkpoint_file = 'segformer.pth'
# build the model from a config file and a checkpoint file
model = init_model(config_file, checkpoint_file, device='cpu')
if not torch.cuda.is_available():
    model = revert_sync_batchnorm(model)

def merge_large_img(data: json = {}):
    # Check tree
    if data == {}:
        root = "annotations"
        flag = True
    else:
        anno_keys = ("province", "district", "ward")
        if all(check_json(key, data) for key in anno_keys):
            root,flag = check_dir_tree(dir_tree= ["data","annotations", data['province'], data["district"],data["ward"]])
        else:
            flag = True
            root = data['annotations'].replace("\\","/")
    try:
        if flag:
            size_path = root.replace("annotations","mask")
            W, H = read_size(root=size_path)

            index = []
            for i in range(H,1, -1):
                index.append([x for x in range(W*i-W, W*i)])
            index.append(np.arange(W-1,-1,-1))
            # index1=[i for i in range(56,64)]
            # index2=[i for i in range(48,56)]
            # index3=[i for i in range(40,48)]
            # index4=[i for i in range(32,40)]
            # index5=[i for i in range(24,32)]
            # index6=[i for i in range(16,24)]
            # index7=[i for i in range(8,16)]
            # index8 = np.arange(7, -1, -1)
            # index = [index1, index2, index3, index4, index5, index6, index7, index8]
            big_images=merging_row(index[0], folder_path=root)
            for i in index[1:]:
                try:
                    image=merging_row(i, folder_path=root)
                    big_images = np.concatenate((big_images, image))
                except:
                    image=merging_row(i, folder_path=root, flag=False)
                    big_images = np.concatenate((big_images, image))
            return big_images
        else:
            print("Can't load annotations")
            return False
    except:
        print("Can't load annotations")
        return False


def get_area_total(big_images,mask):
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

        geo_series, G = get_custom_image(data=data)
        if "lst_img" not in data or data["lst_img"]==[]:
            save_npy(geo_series,G, data)
        for idx, bound in enumerate(geo_series):
            try:
                run(idx=data['lst_img'][idx],bound=bound.bounds, data=data)
            except:
                run(idx=idx,bound=bound.bounds,data=data)
        return "Done"
    else:
        return "You doesn't send ward information!"


@app.route('/get_area', methods=['POST'])
def get_area():
    params = request.args.to_dict()
    if params:
        data = {key: value for key, value in params.items()}
        mask = get_npy(data=data)
        big_images = merge_large_img(data=data)
        # Change link img
        if isinstance(mask, np.ndarray) and isinstance(big_images, np.ndarray):
            new_mask = np.rot90(mask, k=1)
            if new_mask.shape == big_images.shape:
                resized_mask = new_mask
            else:
                new_mask_shape = new_mask.shape
                # Resize new_mask to match big_images if dimensions differ
                resized_big_images = cv2.resize(big_images, (new_mask_shape[1], new_mask_shape[0]))

            resized_big_images[new_mask == False] = False 
            area = calculate_area(image=resized_big_images, mask=new_mask)
            return ({'area': str(area)})
            # return jsonify({"img":big_images.tolist(), 'area': str(area)})
        else:
            return "Not having annotations or images!!!"
    else:
        return "Successfull Start!"


@app.route('/predict_data', methods=['POST'])
def predict_data():
    params = request.args.to_dict()
    if params:
        try:
            data = {key: value for key, value in params.items()}
            root, flag = check_dir_tree(["data","images",data["province"],data["district"],data["ward"]])
            if flag:
                save_dir,_ = check_dir_tree(["data","annotations",data["province"], data["district"],data["ward"]])
                save_dir = save_dir.replace("\\","/")

                for filename in os.listdir(root):
                    image_path = os.path.join(root, filename).replace("\\","/")

                    result = inference_model(model, image_path)
                    vis_iamge = show_result_pyplot(model, image_path, result, out_file=f"{save_dir}/{filename}",
                                                opacity=1.0, show=False,  draw_gt=True, with_labels=False)
                return "Done predict image!"
            else:
                return "Still doesn't download images!!"
        except:
            return "Error when predict"
    return "Problem with url"

@app.route('/', methods=['GET'])
def home():
    return "Hello World!"

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)