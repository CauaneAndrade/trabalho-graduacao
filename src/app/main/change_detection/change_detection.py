import numpy as np

BRANCO = 1
PRETO = 0
def change_detection(img1, img2):
    img1_rows = len(img1)
    img1_cols = len(img1[0])

    new_image = np.zeros((img1_rows, img1_cols, 3), dtype=np.float32)
    for col in range(img1_cols):
        for row in range(img1_rows):
            for index in range(3):
                if img1[row][col][index] == img2[row][col][index]:
                    new_image[row][col][index] = BRANCO
                else:
                    new_image[row][col][index] = PRETO
                
    return new_image