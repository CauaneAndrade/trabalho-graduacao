import matplotlib.pyplot as plt
import matplotlib.image as mpimg


IMAGE_PATH = '../src/data/img/'
template_img = mpimg.imread(f'{IMAGE_PATH}template.png')
full_image = mpimg.imread(f'{IMAGE_PATH}full.png')


def match_template(template_img, full_img):
    template_prop = {'rows': len(template_img), 'columns': len(template_img[0])}
    full_image_prop = {'rows': len(full_img), 'columns': len(full_img[0])}
    max_y_displacement = full_image_prop['columns'] - template_prop['columns']
    max_x_displacement = full_image_prop['rows'] - template_prop['rows']
    sum_absolute_differences = []
    for row_disp in range(max_x_displacement):
        sum_absolute_differences.append([])
        for column_disp in range(max_y_displacement):
            sum_absolute_differences[row_disp].append(0)
            for x in range(template_prop['rows']):
                for y in range(template_prop['columns']):
                    sum_absolute_differences[row_disp][column_disp] += abs(template_img[x][y][0] - full_img[x+row_disp][y+column_disp][0])

    min_error = sum_absolute_differences[0][0]
    [delta_x, delta_y] = (0 , 0)
    for x in range(max_x_displacement):
        for y in range(max_y_displacement):
            if sum_absolute_differences[x][y] < min_error:
                min_error = sum_absolute_differences[x][y]
                [delta_x, delta_y] = (x, y)

    return {'delta_x': delta_x, 'delta_y': delta_y, 'sad': sum_absolute_differences }


answer = match_template(template_img, full_image)
print('Delta X: ' + str(answer['delta_x']))
print('Delta Y: ' + str(answer['delta_y']))
