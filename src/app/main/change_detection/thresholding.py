from .utils import qtd_row_col


BRANCO = 1
PRETO = 0
CINZA =  0.5
def thresholding(img):
    n_rows, n_cols = qtd_row_col(img)
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
            elif img[row][col][0] < level_2:
                for index in values:
                    img[row][col][index] = CINZA
            else:
                for index in values:
                    img[row][col][index] = BRANCO
