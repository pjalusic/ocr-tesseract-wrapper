import cv2


def auto_threshold(image):
    try:
        if len(image.shape) >= 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return gray
    except cv2.error:
        return image
