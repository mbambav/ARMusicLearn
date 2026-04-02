import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_image(path):
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    return image

def preprocess(image):
    # resize to manageable width
    height, width = image.shape[:2]
    new_width = 800
    new_height = int(height * (new_width / width))
    image = cv2.resize(image, (new_width, new_height))
    # blur to reduce noise
    image = cv2.GaussianBlur(image, (5, 5), 0)
    return image

def colour_mask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # white keys
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    # black keys
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])
    black_mask = cv2.inRange(hsv, lower_black, upper_black)
    # combine both masks
    combined_mask = cv2.bitwise_or(white_mask, black_mask)
    return combined_mask

def detect_edges(image):
    median = np.median(image)
    low = median * 0.66
    high = median * 1.33
    edges = cv2.Canny(image, low, high)
    return edges

def keyboard_region(image):
    row_sum = np.sum(image, axis=1)
    plt.plot(row_sum)
    plt.show()
    return image

if __name__ == "__main__":
    image = load_image("/Users/arnavgoyal/Documents/GitHub/ARMusicLearn/testImages/brown_piano.png")
    preprocessed = preprocess(image)
    mask = colour_mask(preprocessed)
    edges = detect_edges(mask)
    region = keyboard_region(edges)
    cv2.imshow("edges", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()