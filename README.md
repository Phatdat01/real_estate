# Explan parameter
province: province name
district: district name
ward: ward name
lst_img: index of image download
W: num img for width

# /download_img: {province: str, district: str, ward: str, lst_img: List[int], W: int}
* Input
- if W None: it auto calculate, but can be wrong cause din't know `W x H` or `W x H`
- if lst_img is [] or not exist, download mask and full image, else just download custom index image
* Works:
- save img
- save mask vs size( num height vs num width img of big image)

# get_area: {province: str, district: str, ward: str}

* Works:
- begon size file, mask file, parameters calculate area vs return json

# Install on Windows
* pip install torch==1.13.0+cpu torchvision==0.14.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu
* pip install mmcv-lite==2.0.0rc4 --extra-index-url https://download.openmmlab.com/mmcv/dist/cpu/torch1.13/index.html
* pip install mmcv==2.0.0rc4 --extra-index-url https://download.openmmlab.com/mmcv/dist/cpu/torch1.13/index.html
* pip install -r requirements.txt

- Access to configs folder, edit _base_: 

```
_base_ = [
    'configs/_base_/models/segformer_mit-b0.py',
    'configs/_base_/datasets/loveda.py',
    'configs/_base_/default_runtime.py',
    'configs/_base_/schedules/schedule_160k.py']
```

# Run docker:
docker-compose down
docker-compose build
docker-compose up -d