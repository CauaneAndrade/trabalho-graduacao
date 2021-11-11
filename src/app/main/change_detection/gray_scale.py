from .utils import qtd_row_col

# gray level computation
def gray_scale(img):
    n_rows = qtd_row_col(img)[0]
    n_cols = qtd_row_col(img)[1]

    for row in range(n_rows):
        for col in range(n_cols):
            v = img[row][col]
            new_gray_level = (v[0] + v[1] + v[2]) / 3
            for index in range(3):
                img[row][col][index] = new_gray_level