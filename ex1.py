import numpy as np
import matplotlib.pyplot as plt
from demo import merge_large_img, sub
# Assuming you have "matrix" and "img" already defined
model = np.load('mask.npy').reshape(14598, 15408)

big_images = merge_large_img()
plt.imshow(big_images)
plt.show()

model = sub(image=model, x1=0, y1=12000,x2=2000,y2=10000)

big_images = sub(image=big_images, x1=0, y1=12000,x2=2000,y2=10000)
plt.imshow(big_images)
plt.show()

big_images[np.arange(len(big_images)), np.sum(model, axis=1)] = 0
result = np.where(model, big_images, 0)
plt.imshow(result)
plt.show()

# mask = np.uint8(model) * 255
# mask_inv = cv2.bitwise_not(mask)
# masked_img = cv2.bitwise_and(big_images, big_images, mask=mask_inv)
# result = cv2.bitwise_or(masked_img, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR))

# Display the result
# cv2.imshow("Result", result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()