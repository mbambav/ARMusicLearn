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

def keyboard_region(edges, original):
    row_sum = np.sum(edges, axis=1)
    threshold = np.mean(row_sum)
    
    while True:
        rows_above_threshold = np.where(row_sum > threshold)[0]
        
        if len(rows_above_threshold) == 0:
            break
            
        y1 = int(rows_above_threshold[0])
        y2 = int(rows_above_threshold[-1])
        region_height = y2 - y1
        
        # stop when region is small enough to just be the keys
        if region_height < original.shape[0] * 0.3:
            break
            
        threshold = np.mean(row_sum[rows_above_threshold])
    
    width = original.shape[1]
    cv2.rectangle(original, (0, y1), (width, y2), (0, 255, 0), 2)
    cv2.imwrite("debug_rectangle.png", original)
    
    cropped = original[y1:y2, :]
    cv2.imshow("cropped", cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return cropped


if __name__ == "__main__":
    image = load_image("/Users/arnavgoyal/Documents/GitHub/ARMusicLearn/testImages/brown_piano.png")
    preprocessed = preprocess(image)
    mask = colour_mask(preprocessed)
    edges = detect_edges(mask)
    keyboard = keyboard_region(edges, preprocessed)
    
    # temporary FFT test - pick a row in the middle of the image
    test_row = keyboard.shape[0] // 2
    slice = preprocessed[test_row, :, 0]
    fft = np.fft.fft(slice)
    magnitude = np.abs(fft)
    freqs = np.fft.fftfreq(len(slice))

    # only plot positive frequencies
    positive = freqs > 0
    plt.plot(freqs[positive], magnitude[positive])
    plt.xlabel("frequency")
    plt.ylabel("magnitude")
    plt.show()