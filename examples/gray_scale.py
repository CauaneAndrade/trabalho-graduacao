import copy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# import numpy as np


IMAGE_PATH = '../src/data/img/'
template_img = mpimg.imread(f'{IMAGE_PATH}template.png')
full_image = mpimg.imread(f'{IMAGE_PATH}full.png')

template_image_grayscale = copy.deepcopy(template_img)
full_image_grayscale = copy.deepcopy(full_image)

boeing_image_test = mpimg.imread(f'{IMAGE_PATH}test2.jpg')
boeing_image_test_grayscale = copy.deepcopy(boeing_image_test)

def img_rows_and_columns(img: mpimg.imread):
    print('Reading the number of rows and columns... \n')
    number_rows = len(img)
    number_columns = len(img[0])
    print(f'Rows: {number_rows} - Columns: {number_columns}')
    return (number_rows, number_columns)


def plot_image(f_number: int, img, title: str):
    plt.figure(f_number)
    imgplot = plt.imshow(img)
    plt.title(title)
    plt.grid()
    plt.show()


def gray_scale_level(img):
    rows_and_columns = img_rows_and_columns(img)
    number_rows = rows_and_columns[0]
    number_columns = rows_and_columns[1]

    for row in range(number_rows):
        for column in range(number_columns):
            x = img[row][column]
            new_gray_level = (x[0] + x[1] + x[2]) / 3
            for k in range(3):
                img[row][column][k] = int(new_gray_level)

    plot_image(1, img, 'Grayscale image')

# plot_image(0, boeing_image_test, 'Original image')
gray_scale_level(boeing_image_test_grayscale)