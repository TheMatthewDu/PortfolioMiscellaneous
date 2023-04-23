from helpers import *
import cv2 as cv
import numpy as np
from cv2.data import haarcascades

write_output = False
debug = True


def _index_largest_area(bounds):
    areas = [region[2] * region[3] for region in bounds]
    return areas.index(max(areas))


def run_thresh(masked_img):
    def nothing(x):
        pass

    cv.namedWindow('image')
    cv.createTrackbar('low', 'image', 0, 255, nothing)
    cv.createTrackbar('high', 'image', 0, 255, nothing)

    temp = np.copy(masked_img)
    while True:
        temp_show = cv.resize(temp, None, fx=0.25, fy=0.25, interpolation=cv.INTER_LINEAR)
        cv.imshow('image', temp_show)
        k = cv.waitKey(1)
        if k == ord('q'):
            break

        # get current positions of four trackbars
        low = cv.getTrackbarPos('low', 'image')
        high = cv.getTrackbarPos('high', 'image')

        _, temp = cv.threshold(masked_img, low, high, cv.THRESH_BINARY)
    cv.destroyWindow('image')
    return temp


def draw_image(h, masked_img, sketch, w, x, y):
    cv.rectangle(sketch, (x, y), (x + w, y + h), (255, 255, 255), -1)
    cv.rectangle(masked_img, (x, y), (x + w, y + h), 0, 20)  # Remove border of mask

    contours, _ = cv.findContours(masked_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    lines = [np.array([c[0] for c in cont]) for cont in contours]
    for line in lines:
        for i in range(line.shape[0] - 1):
            cv.line(sketch, line[i], line[i + 1], 0, thickness=5)
        cv.line(sketch, line[-1], line[0], 0, thickness=5)


def run_canny(masked_img):
    def nothing(x):
        pass

    cv.namedWindow('image')
    cv.createTrackbar('low', 'image', 0, 255, nothing)
    cv.createTrackbar('high', 'image', 0, 255, nothing)

    temp = np.copy(masked_img)
    while True:
        temp_show = cv.resize(temp, None, fx=0.25, fy=0.25, interpolation=cv.INTER_LINEAR)
        cv.imshow('image', temp_show)
        k = cv.waitKey(1)
        if k == ord('q'):
            break

        # get current positions of four trackbars
        low = cv.getTrackbarPos('low', 'image')
        high = cv.getTrackbarPos('high', 'image')

        temp = cv.Canny(masked_img, low, high)
    cv.destroyWindow('image')
    return temp


def read_face(img: np.ndarray, sketch: np.ndarray, saved: dict) -> np.ndarray:
    face_cascade = cv.CascadeClassifier(f'{haarcascades}/haarcascade_frontalface_default.xml')

    faces = face_cascade.detectMultiScale(img, 1.1, 5)

    x, y, w, h = faces[0]

    # Correct for error from haar
    y -= 450
    h += 700

    face_mask_clone = np.copy(img)
    cv.rectangle(face_mask_clone, (x, y), (x + w, y + h), 255, 5)
    display(face_mask_clone)

    masked_img = get_masked_region(img, x, y, w, h)
    if debug:
        display(masked_img)

    saved["Face"] = (x, y, w, h)

    masked_img = cv.Canny(masked_img, 50, 100)
    if debug:
        display(masked_img)

    draw_image(h, masked_img, sketch, w, x, y)

    display(sketch)
    return sketch


def read_hair(img: np.ndarray, sketch: np.ndarray, saved: dict) -> np.ndarray:
    face_cascade = cv.CascadeClassifier(f'{haarcascades}/haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img, 1.1, 11)

    hair_img = np.full(img.shape, 255, dtype=np.uint8)
    for x, y, w, h in faces:
        # Correct for error from haar
        y -= 140
        h += 100

        masked_img = get_masked_region(img, x, y, w, h)
        if debug:
            display(masked_img)

        masked_img = run_thresh(masked_img)
        masked_img = run_canny(masked_img)
        draw_image(h, masked_img, sketch, w, x, y)

    k = 20 * sketch.shape[0] // 100
    sketch[:k, :] = hair_img[:k, :]
    display(sketch)

    return sketch


def read_mouth(img: np.ndarray, sketch: np.ndarray, saved: dict) -> np.ndarray:
    smile_cascade = cv.CascadeClassifier(f'{haarcascades}/haarcascade_smile.xml')

    x, y, w, h = saved["Face"]
    face_mask = get_masked_region(img, x, y, w, h)

    # Detect mouths
    mouths = smile_cascade.detectMultiScale(face_mask, 1.1, 11)

    x, y, w, h = mouths[_index_largest_area(mouths)]
    mouth_mask = get_masked_region(face_mask, x, y, w, h)

    # mouth_mask = cv.cvtColor(mouth_mask, cv.COLOR_BGR2GRAY)
    if debug:
        display(mouth_mask)

    mouth_mask = run_thresh(mouth_mask)
    mouth_mask = run_canny(mouth_mask)

    draw_image(h, mouth_mask, sketch, w, x, y)
    display(sketch)

    return sketch


def read_eyes(img: np.ndarray, sketch: np.ndarray, saved: dict) -> np.ndarray:
    eyes_cascade = cv.CascadeClassifier(f'{haarcascades}/haarcascade_eye.xml')

    x, y, w, h = saved["Face"]
    face_mask = get_masked_region(img, x, y, w, h)

    # Detect Eyes
    eyes = eyes_cascade.detectMultiScale(face_mask, 1.1, 4)
    for x, y, w, h in eyes:
        x -= 40
        w += 150
        h -= 10
        y += 10

        eye_mask = get_masked_region(face_mask, x, y, w, h)
        if debug:
            display(eye_mask)

        eye_mask = run_thresh(eye_mask)
        eye_mask = run_canny(eye_mask)
        draw_image(h, eye_mask, sketch, w, x, y)

    display(sketch)

    return sketch


def read_body(img: np.ndarray, sketch: np.ndarray, saved: dict) -> np.ndarray:
    canny_output = run_canny(img)
    
    contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    mask = np.full(img.shape, 255, dtype=np.uint8)
    cv.drawContours(mask, contours, -1, (0, 0, 0), 4)

    if debug:
        k = 70 * sketch.shape[0] // 100

        view = np.full(mask.shape, 255, dtype=np.uint8)
        view[k:, :] = mask[k:, :]

        display(view)

    k = 70 * sketch.shape[0] // 100
    sketch[k:, :] = mask[k:, :]
    display(sketch)
    
    return sketch


def main():
    img = cv.imread('../data/img.png', 0)
    sketch = np.full(img.shape, 255, dtype=np.uint8)
    
    saved_images = {}
    
    processes = [
        read_face,
        read_hair,
        read_mouth,
        read_eyes,
        read_body
    ]
    
    for process in processes:
        sketch = process(img, sketch, saved_images)
    
    if write_output:
        cv.imwrite("result.png", sketch)


if __name__ == "__main__":
    main()
