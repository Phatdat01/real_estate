import numpy as np
import matplotlib.pyplot as plt

def visualize_mask(mask):
    plt.pcolormesh(mask, cmap="binary")  # Reshape for plotting
    # Optional: Add labels and title
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("2D Array Visualization")
    plt.savefig("my_mask_visualization.png")

def calculate_area(image, mask):
	unique_values, counts = np.unique(image[mask], return_counts=True)

	area={}
	for i in range(len(unique_values)):
		area[unique_values[i]] = counts[i]*0.3*0.3
	print(area)

#edit here
#split the big mask to 64 small ones
#mask size depend on the image on dataset
#link dataset: https://drive.google.com/drive/folders/1HUd84yzf88tOZmYqmIrJKK7QrD2dwGMx
def split_mask(mask, rows=8, cols =8):
	height, width = mask.shape
	small = []

	for i in reversed(range(rows)):
		if i%2==0:
			col_indices=range(cols)

def main():
	mask = np.load('mask.npy')
	visualize_mask(mask)
	# image = plt.imread("./re_training/images/img_1018.png")
	# calculate_area(image, mask)
	# split_mask(mask)

if __name__ == '__main__':
	main()
