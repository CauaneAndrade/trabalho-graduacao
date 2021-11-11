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
    delta_x = 0
    delta_y = 0

    for row in range(max_x_disp):
        for col in range(max_y_disp):
            if sum_abs_diff[row][col] < min_error:
                # nem sempre o sad vai dar tem que ser o menor
                min_error = sum_abs_diff[row][col]
                [delta_x, delta_y] = (row, col)

    return (delta_x, delta_y)  # row, col


def crop_image_template(image, x, y):
    return image[x[0]:x[1], y[0]:y[1]]


# def get_template_matching(image, tie_point, xy=None):
#     rows, cols = tie_point.shape[0], tie_point.shape[1]
#     if xy:
#         x, y = xy
#     else:
#         x, y = template_matching(image, tie_point)
#     print('--------------------', x, y)

#     x_max = rows + x
#     y_min = y + 1
#     y_max = cols + y
#     return (x, x_max), (y_min, y_max)


def get_template_matching(image, tie_point, xy=None):
    rows, cols = tie_point.shape[0], tie_point.shape[1]
    if xy:
        x, y = xy
    else:
        x, y = template_matching(image, tie_point)
    print(f'--------------------{x}, {y}')

    y_top = x
    y_bottom = rows + y_top
    x_left =  y + 1
    x_right =  cols + y
    return (x_left, x_right), (y_top, y_bottom)
    