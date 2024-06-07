import numpy as np
import matplotlib.pyplot as plt

def visualize_mask(mask):
    try:
        plt.imshow(image, cmap='jet', alpha=0.5)
        plt.imshow(mask, cmap='gray', alpha=0.5)
        plt.show()
    except:
        plt.pcolormesh(mask, cmap="binary")  # Reshape for plotting
        # Optional: Add labels and title
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.title("2D Array Visualization")
        plt.savefig("my_mask_visualization.png")

def calculate_area(image, mask):
    unique_values, counts = np.unique(image[mask], return_counts=True)
    print(unique_values, counts)
    area = {}
    for i in range(len(unique_values)):
        area[unique_values[i]] = counts[i] * 0.3 * 0.3

    return area

# Example usage
image = np.array([[1, 1, 2, 2],
                  [1, 1, 2, 2],
                  [3, 3, 4, 4],
                  [3, 3, 4, 4]])


mask = np.array([[True, False, True, False],
                 [False, True, False, True],
                 [True, False, True, False],
                 [False, True, False, True]])

# visualize_mask(image)
# result = calculate_area(image, mask)
image[np.arange(len(image)), np.sum(mask, axis=1)] = 0

# Keep the values in "image" where the corresponding elements in "mask" are True
result = np.where(mask, image, 0)

print(result)