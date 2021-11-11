import matplotlib.image as mpimg
import copy
from .gray_scale import gray_scale
from .thresholding import thresholding
from .template_matching import get_template_matching, crop_image_template
from .change_detection import change_detection
from ...db_conf import mongo
import numpy as np
from .utils import plot_image
import matplotlib.pyplot as plt
from skimage import util as skimage_util
from PIL import Image
import cv2


PATH = "../src/app/static/"


def change_file_dtype(*files):
    rgb_channel = 3
    result = []
    for file in files:
        int8_image = copy.deepcopy(file[..., :rgb_channel])
        image_float = skimage_util.img_as_float(int8_image)
        result.append(image_float)
    return result


def transform_image(image):
    gray_scale(image)
    thresholding(image)


def compose_image_compared(image, pt1, pt2):
    img = image.copy()
    return cv2.rectangle(img, (pt1), pt2, 255, 1)


def match_and_compare(image1, image2, tie_point):
    img1_x, img1_y = get_template_matching(image1, tie_point)
    img2_x, img2_y = get_template_matching(image2, tie_point)

    new_img1 = crop_image_template(image1, img1_y, img1_x)
    new_img2 = crop_image_template(image2, img2_y, img2_x)
    img_change = change_detection(new_img1, new_img2)

    # pt1_img1 = img1_x[0], img1_y[0]
    # pt2_img1 = img1_x[1], img1_y[1]
    # img_a = compose_image_compared(image1, pt1_img1, pt2_img1)
    
    save_image(image1, 'big_1.png')
    save_image(image2, 'big_2.png')
    save_image(new_img1, 'small_1.png')
    save_image(new_img2, 'small_2.png')
    save_image(img_change)
    return img_change


def save_image(image, image_name="resultado_bruto.png"):
    plt.imshow(image)
    plt.savefig(f"{PATH}{image_name}")
    return True


def image_change_detection(file_source, file_template, file_tie_point):
    src_image, template_image, tie_point_image = change_file_dtype(
        file_source, file_template, file_tie_point
    )

    # transforma as images para gray scale
    transform_image(src_image)
    transform_image(template_image)
    transform_image(tie_point_image)

    img_compared = match_and_compare(src_image, template_image, tie_point_image)
    return True
