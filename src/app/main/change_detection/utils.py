import matplotlib.pyplot as plt


def qtd_row_col(image):
    n_rows = len(image)
    n_cols = len(image[0])
    return (n_rows, n_cols)


def plot_image(index, image, title):
    plt.figure(index)
    imgplot = plt.imshow(image)
    plt.title(title)
    # plt.grid()
