import cv2

def read_image_file(image_file):
    img = cv2.imread(image_file)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)