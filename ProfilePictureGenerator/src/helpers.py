import cv2 as cv
import numpy as np


def display(img: np.ndarray) -> None:
    img_show = cv.resize(img, None, fx=0.25, fy=0.25, interpolation=cv.INTER_LINEAR)
    cv.imshow("img_show", img_show)
    cv.waitKey()


def get_masked_region(img_gray: np.ndarray, x: int, y: int, w: int, h: int):
    # assert len(img_gray.shape) == 2

    mask = np.zeros(img_gray.shape, dtype=np.uint8)
    mask[y:y+h, x:x+w] = img_gray[y:y+h, x:x+w]

    return mask


if __name__ == "__main__":
    img_ = cv.imread("../data/new_profile.png", 0)
    img_ = get_masked_region(img_, 132, 235, 123, 136)
    display(img_)
