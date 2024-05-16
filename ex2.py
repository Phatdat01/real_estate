import numpy as np

image = np.array([[1, 1, 2, 2],
                  [1, 1, 2, 2],
                  [3, 3, 4, 4],
                  [3, 3, 4, 4]])

mask = np.array([[True, False, True, False],
                 [False, True, False, True],
                 [True, False, True, False],
                 [False, True, False, True]])

# Set the last value in each row of the "image" array to 0
last_nonzero_indices = np.argmax(mask[:, ::-1], axis=1)

for i, index in enumerate(last_nonzero_indices):
    image[i, index] = 0

print(image)