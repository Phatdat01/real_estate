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

* Run docker:
docker-compose down
docker-compose build
docker-compose up -d