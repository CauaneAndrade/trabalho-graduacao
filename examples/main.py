import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import copy
import cv2

# filenames
filename = "1.png"
template_filename = "2.png"
imgs_path = "../src/data/img/"

# padrao PNG, array
src_img_array = mpimg.imread(imgs_path + filename)
template_img_array = mpimg.imread(imgs_path + template_filename)

# images - source e template
src_image = copy.deepcopy(src_img_array)
template_image = copy.deepcopy(template_img_array)


def qtd_row_col(image):
    n_rows = len(image)
    n_cols = len(image[0])
    # print(f'Number of rows: {n_rows}', end='\n')
    # print(f'Number of columns: {n_cols}', end='\n')
    return (n_rows, n_cols)


def plot_image(index, image, title):
    plt.figure(index)
    imgplot = plt.imshow(image)
    plt.title(title)
    plt.grid()


# gray level computation
def gray_scale(img, n_rows, n_cols):
    for row in range(n_rows):
        for col in range(n_cols):
            v = img[row][col]
            new_gray_level = (v[0] + v[1] + v[2]) / 3
            for index in range(3):
                img[row][col][index] = new_gray_level


def thresholding(n_rows, n_cols, img):
    level_1 = 0.3
    level_2 = 0.6
    values = range(3)
    for row in range(n_rows):
        for col in range(n_cols):
            if img[row][col][0] < level_1:
                for index in values:
                    img[row][col][index] = 0
            elif img[row][col][0] < level_2:
                for index in values:
                    img[row][col][index] = 0.5
            else:
                for index in values:
                    img[row][col][index] = 1


def template_matching(src_img, template_img):
    src_xy = {'rows': len(src_img), 'columns': len(src_img[0])}  # {rows: 50, col: 100}
    template_xy = {'rows': len(template_img), 'columns': len(template_img[0])}  # {rows: 25, col: 50}
    max_x_disp = src_xy['rows'] - template_xy['rows']  # (50 - 25) -> 25
    max_y_disp = src_xy['columns'] - template_xy['columns']  # (100 - 50) -> 50

    sum_abs_diff = []
    for row in range(max_x_disp): # max_x_disp = 25
        sum_abs_diff.append([])
        # sum_abs_diff = [[]]  # row = 0
        for col in range(max_y_disp):
            sum_abs_diff[row].append(0)
            # sum_abs_diff = [[0]]  # col = 0
            for x in range(template_xy['rows']):  # template_xy['rows'] = 25  # x = 0
                for y in range(template_xy['columns']):  # template_xy['columns'] = 50  # y = 0
                    sum_abs_diff[row][col] += abs(template_img[x][y][0] - src_img[x + row][y + col][0])
                    # sum_abs_diff[row][col] = 0
                    # template_img[x][y][0] = ?  | src_img[x + row][y + col][0] -> src_img[0][0][0] = ?

    min_error = sum_abs_diff[0][0]
    [delta_x, delta_y] = (0 , 0)
    for row in range(max_x_disp):
        for col in range(max_y_disp):
            if sum_abs_diff[row][col] < min_error:
                min_error = sum_abs_diff[row][col]
                [delta_x, delta_y] = (row, col)
    # o que o delta representa?
    # data = {'delta_x': delta_x, 'delta_y': delta_y, 'sad': sum_abs_diff }
    breakpoint()
    data = src_img[delta_x, delta_y]
    plot_image(5, data, 'Change Detection Image')
    plt.show()
    return data


def template_matching_2(src_image, template_image):
    # src_image = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    # template_image = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
    breakpoint()
    result = cv2.matchTemplate(
        src_image, template_image,
        cv2.TM_CCOEFF_NORMED  # coeficiente de correlação normalizado
        # template matching method
    )
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)  #  encontrar o local com o maior valor -> a correspondência mais provável

    # extraindo as coordenadas e bounding box
    (startX, startY) = maxLoc
    # adicionando a largura e altura do modelo às coordenadas startX e endX
    endX = startX + template_image.shape[1]
    endY = startY + template_image.shape[0]

    newImageMatch = src_image[startX:startY, endX:endY]
    return newImageMatch


def compare_images(src_img, template_img):
    src_n_rows = len(src_img)
    src_n_cols = len(src_img[0])
    # template_n_rows = len(template_img)
    # template_n_cols = len(template_img[0])

    data = np.zeros((src_n_rows, src_n_cols, 3), dtype=np.float32)
    for row in range(src_n_rows):
        for col in range(src_n_cols):
            for index in range(3):
                if src_img[row][col][index] == template_img[row][col][index]:
                    data[row][col][index] = 1
                else:
                    data[row][col][index] = 0
    return data


def main():
    # rows e columns
    n_rows = qtd_row_col(src_img_array)[0]
    n_cols = qtd_row_col(src_img_array)[1]
    n_rows_template = qtd_row_col(template_img_array)[0]
    n_cols_template = qtd_row_col(template_img_array)[1]

    # transforma as images para gray scale
    gray_scale(src_image, n_rows, n_cols)
    gray_scale(template_image, n_rows, n_cols)

    # template matching, ainda não está completa
    # imageCrop = template_matching_2(src_image, template_image)
    # imageCrop = template_matching(src_img_array, template_img_array)
    # imageCrop = template_matching(src_image, template_image)
    
    # image thresholding, supondo que as imagens sejam do mesmo tamanho (será resolvido no template matching)
    thresholding(n_rows, n_cols, src_image)
    thresholding(n_rows, n_cols, template_image)
    # thresholding(n_rows, n_cols, imageCrop)

    # compare images - gray scale images
    image_change_detection = compare_images(src_image, template_image)
    # image_change_detection = compare_images(imageCrop, template_image)

    plot_image(0, src_img_array, 'Image - Original')
    plot_image(1, src_image, 'Source Image - Grayscale')
    plot_image(2, template_image, 'Template Image - Grayscale')
    plot_image(3, src_image, 'Source Image - Thresholding')
    plot_image(4, template_image, 'Template Image - Thresholding')
    plot_image(5, image_change_detection, 'Change Detection Image')
    plt.show()

main()