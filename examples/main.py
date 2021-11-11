import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import copy
import cv2

# filenames
filename = "source.png"
template_filename = "template1.png"
imgs_path = "../src/data/img/comparar/"

# padrao PNG, array
src_img_array = mpimg.imread(imgs_path + filename)
template_img_array = mpimg.imread(imgs_path + template_filename)

# images - source e template
src_image = copy.deepcopy(src_img_array)
template_image = copy.deepcopy(template_img_array)


def qtd_row_col(image):
    n_rows = len(image)
    n_cols = len(image[0])
    return (n_rows, n_cols)


def plot_image(index, image, title):
    plt.figure(index)
    imgplot = plt.imshow(image)
    plt.title(title)
    # plt.grid()


# gray level computation
def gray_scale(img, n_rows, n_cols):
    for row in range(n_rows):
        for col in range(n_cols):
            v = img[row][col]
            new_gray_level = (v[0] + v[1] + v[2]) / 3
            for index in range(3):
                img[row][col][index] = new_gray_level

BRANCO = 1
PRETO = 0
def thresholding(n_rows, n_cols, img):
    """
    segmenting the image
    binary image
    """
    level_1 = 0.3
    level_2 = 0.6
    values = range(3)
    for row in range(n_rows):
        for col in range(n_cols):
            if img[row][col][0] < level_1:
                for index in values:
                    img[row][col][index] = PRETO
            # elif img[row][col][0] < level_2:
            #     for index in values:
            #         img[row][col][index] = 0.5
            else:
                for index in values:
                    img[row][col][index] = BRANCO


def template_matching(src_img, template_img):
    src_xy = {'rows': len(src_img), 'cols': len(src_img[0])}
    template_xy = {'rows': len(template_img), 'cols': len(template_img[0])}
    max_x_disp = src_xy['rows'] - template_xy['rows']
    max_y_disp = src_xy['cols'] - template_xy['cols']
    
    print(f"""
        src_xy: {src_xy} \n
        template_xy: {template_xy}\n
        max_x_disp: {max_x_disp}\n
        max_y_disp: {max_y_disp}\n
    """)

    sum_abs_diff = []
    for row in range(max_x_disp):
        sum_abs_diff.append([])
        for col in range(max_y_disp):
            sum_abs_diff[row].append(0)
            for x in range(template_xy['rows']):
                for y in range(template_xy['cols']):
                    sum_abs_diff[row][col] += abs(template_img[x][y][0] - src_img[x + row][y + col][0])
    
    min_error = sum_abs_diff[0][0]  # SAD: sum of average difference
    delta_x = delta_y = 0

    for row in range(max_x_disp):
        for col in range(max_y_disp):
            if sum_abs_diff[row][col] < min_error:
                # nem sempre o sad vai dar tem que ser o menor
                min_error = sum_abs_diff[row][col]
                [delta_x, delta_y] = (row, col)
    print("-------------------------")
    print(delta_x, delta_y)

    return (delta_x, delta_y)  # row, col


BRANCO = 1
PRETO = 0
def change_detection(img1, img2):
    img1_rows = len(img1)  # 68
    img1_cols = len(img1[0])  # 108

    new_image = np.zeros((img1_rows, img1_cols, 3), dtype=np.float32)
    for col in range(img1_cols):
        for row in range(img1_rows):
            for index in range(3):
                if img1[row][col][index] == img2[row][col][index]:
                    new_image[row][col][index] = BRANCO
                else:
                    new_image[row][col][index] = PRETO
                
    return new_image


def main():
    # rows e columns
    n_rows = qtd_row_col(src_img_array)[0]
    n_cols = qtd_row_col(src_img_array)[1]
    n_rows_tplt = qtd_row_col(template_img_array)[0]
    n_cols_tplt = qtd_row_col(template_img_array)[1]
    import pdb; pdb.set_trace()
    
    print('transformando images em gray scale')

    # transforma as images para gray scale
    gray_scale(src_image, n_rows, n_cols)
    gray_scale(template_image, n_rows_tplt, n_cols_tplt)
    
    print('thresholding')
    # image thresholding
    thresholding(n_rows, n_cols, src_image)
    thresholding(n_rows_tplt, n_cols_tplt, template_image)

    print('template matching')
    # comparar images
    x, y = template_matching(src_image, template_image)
    src_image_cp = src_image.copy()
    cropped_img = src_image_cp[x:n_rows_tplt + x, y + 1:n_cols_tplt + y + 1]
    image_change_detection = change_detection(cropped_img, template_image)

    # plot_image(0, src_img_array, 'Source Image - Original')
    # plot_image(1, template_img_array, 'Template Image - Original')
    # plot_image(2, src_image, 'Source Image - Grayscale')
    # plot_image(3, template_image, 'Template Image - Grayscale')
    # plot_image(4, src_image, 'Source Image - Thresholding')
    # plot_image(5, template_image, 'Template Image - Thresholding')
    plot_image(6, cropped_img, 'Cropped Image')
    plot_image(7, image_change_detection, 'Change Detection Result')
    plt.show()

main()
