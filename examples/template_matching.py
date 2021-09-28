import matplotlib.pyplot as plt
import matplotlib.image as mpimg


IMAGE_PATH = '../src/data/img/'
template_img = mpimg.imread(f'{IMAGE_PATH}template.png')
source_img = mpimg.imread(f'{IMAGE_PATH}full.png')


def match_template(template_img, source_img):
    template_xy = {'rows': len(template_img), 'columns': len(template_img[0])}
    source_xy = {'rows': len(source_img), 'columns': len(source_img[0])}
    max_y_displacement = source_xy['columns'] - template_xy['columns']
    max_x_displacement = source_xy['rows'] - template_xy['rows']
    sum_absolute_diff = []
    for row in range(max_x_displacement):
        sum_absolute_diff.append([])
        for col in range(max_y_displacement):
            sum_absolute_diff[row].append(0)
            for x in range(template_xy['rows']):
                for y in range(template_xy['columns']):
                    sum_absolute_diff[row][col] += abs(template_img[x][y][0] - source_img[x+row][y+col][0])

    min_error = sum_absolute_diff[0][0]
    [delta_x, delta_y] = (0 , 0)
    for row in range(max_x_displacement):
        for col in range(max_y_displacement):
            if sum_absolute_diff[row][col] < min_error:
                min_error = sum_absolute_diff[row][col]
                [delta_x, delta_y] = (row, col)

    return {'delta_x': delta_x, 'delta_y': delta_y, 'sad': sum_absolute_diff }


answer = match_template(template_img, source_img)
print('Delta X: ' + str(answer['delta_x']))
print('Delta Y: ' + str(answer['delta_y']))
