from ntpath import join
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
import os
import menu
import scipy.fftpack as fft

# Ex 3.1


def read_image(img_path):
    return plt.imread(img_path)


# Ex 3.2
def colormap_function(colormap_name, color1, color2):
    return clr.LinearSegmentedColormap.from_list(colormap_name, [color1, color2], 256)


# Ex 3.3
def draw_plot(text, image, colormap=None):
    plt.figure()
    if colormap is not None:
        plt.title(text)
        plt.imshow(image, cmap=colormap)
    else:
        plt.title(text)
        plt.imshow(image)


# Ex 3.4
def rgb_components(img):
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]
    return R, G, B


# if T is a matrix -> Ti = np.linalg.inv(T) to get inversed matrix
def join_RGB(R, G, B):
    matrix_inverted = np.zeros((len(R), len(R[0]), 3), dtype=np.uint8)

    matrix_inverted[:, :, 0] = R
    matrix_inverted[:, :, 1] = G
    matrix_inverted[:, :, 2] = B
    return matrix_inverted


# Ex 3.5
def show_rgb(channel_R, channel_G, channel_B):
    K = (0, 0, 0)
    R = (1, 0, 0)
    G = (0, 1, 0)
    B = (0, 0, 1)

    cm_red = colormap_function("Reds", K, R)
    cm_green = colormap_function("Greens", K, G)
    cm_blue = colormap_function("Blues", K, B)

    fig = plt.figure()

    fig.add_subplot(1, 3, 1)
    plt.title("Channel R with padding")
    plt.imshow(channel_R, cmap=cm_red)

    fig.add_subplot(1, 3, 2)
    plt.title("Channel G with padding")
    plt.imshow(channel_G, cmap=cm_green)

    fig.add_subplot(1, 3, 3)
    plt.title("Channel B with padding")
    plt.imshow(channel_B, cmap=cm_blue)


# Ex 4
def padding_function(img, lines, columns):
    original_img = img
    num_lines_to_add = 0
    num_columns_to_add = 0

    if columns % 16 != 0:
        num_columns_to_add = (16 - (columns % 16))
        array = img[:, -1:]

        aux_2 = np.repeat(array, num_columns_to_add, axis=1)
        img = np.append(img, aux_2, axis=1)

    if lines % 16 != 0:
        num_lines_to_add = (16 - (lines % 16))
        array = img[-1:]
        aux_2 = np.repeat(array, num_lines_to_add, axis=0)
        img = np.append(img, aux_2, axis=0)

    # Plotting
    fig = plt.figure()

    fig.add_subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(original_img)

    fig.add_subplot(1, 2, 2)
    plt.title("Image with padding")
    plt.imshow(img)

    return img


# passar logo n linhas e colunas
def without_padding_function(img_with_padding, lines, columns):
    img_recovered = img_with_padding[:lines, :columns, :]
    return img_recovered


# Ex 5.1
def rgb_to_ycbcr(R, G, B):
    Y = (0.299 * R) + (0.587 * G) + (0.114 * B)
    Cb = (-0.168736 * R) + (-0.331264 * G) + (0.5 * B) + 128
    Cr = (0.5 * R) + (-0.418688 * G) + (-0.081312 * B) + 128

    return Y, Cb, Cr


def ycbcr_to_rgb(Y, Cb, Cr):
    matrix = np.array([[0.299,   0.587,    0.114],
                       [-0.168736, -0.331264,     0.5],
                       [0.5, -0.418688, -0.081312]])
    T_matrix = np.linalg.inv(matrix)

    R = np.round(T_matrix[0][0] * Y + T_matrix[0][1] *
                 (Cb - 128) + T_matrix[0][2] * (Cr - 128))
    R[R < 0] = 0
    R[R > 255] = 255

    G = np.round(T_matrix[1][0] * Y + T_matrix[1][1] *
                 (Cb - 128) + T_matrix[1][2] * (Cr - 128))
    G[G < 0] = 0
    G[G > 255] = 255

    B = np.round(T_matrix[2][0] * Y + T_matrix[2][1] *
                 (Cb - 128) + T_matrix[2][2] * (Cr - 128))
    B[B < 0] = 0
    B[B > 255] = 255

    return np.uint8(R), np.uint8(G), np.uint8(B)


# Ex 5.3
def show_ycbcr(Y, Cb, Cr):
    K = (0, 0, 0)
    W = (1, 1, 1)
    cm = colormap_function("Grays", K, W)

    # Plotting
    fig = plt.figure()

    # Y
    fig.add_subplot(1, 3, 1)
    plt.title("Y")
    plt.imshow(Y, cmap=cm)

    # Cb
    fig.add_subplot(1, 3, 2)
    plt.title("Cb")
    plt.imshow(Cb, cmap=cm)

    # Cr
    fig.add_subplot(1, 3, 3)
    plt.title("Cr")
    plt.imshow(Cr, cmap=cm)


# Ex 6.1
def downsampling(Y, Cb, Cr, Yref, fatorCr, fatorCb):
    Cr_d = Cr[:, ::fatorCr]

    if fatorCb == 0:
        # Eliminates rows & columns of Cb, Cr
        Cb_d = Cb[::fatorCr, ::fatorCr]
        Cr_d = Cr_d[::fatorCr]
    else:
        # Eliminates columns of Cb
        Cb_d = Cb[:, ::fatorCb]

    return Y, Cb_d, Cr_d


def upsampling(Y_d, Cb_d, Cr_d, type):

    if type == 0:
        Cb_u = Cb_d.repeat(2, axis=0).repeat(2, axis=1)
        Cr_u = Cr_d.repeat(2, axis=0).repeat(2, axis=1)

    else:
        Cb_u = Cb_d.repeat(2, axis=1)
        Cr_u = Cr_d.repeat(2, axis=1)

    return Y_d, Cb_u, Cr_u


# Ex 7
def dct(Y_d, Cb_d, Cr_d, blocks):

    if blocks == "all":
        Y_dct = fft.dct(fft.dct(Y_d, norm="ortho").T, norm="ortho").T
        Y_dct_log = np.log(np.abs(Y_dct) + 0.0001)

        Cb_dct = fft.dct(fft.dct(Cb_d, norm="ortho").T, norm="ortho").T
        Cb_dct_log = np.log(np.abs(Cb_dct) + 0.0001)

        Cr_dct = fft.dct(fft.dct(Cr_d, norm="ortho").T, norm="ortho").T
        Cr_dct_log = np.log(np.abs(Cr_dct) + 0.0001)

    # 7.2 - fazer mais tarde
    elif blocks == "8":
        pass

    # 7.3 - fazer mais tarde
    elif blocks == "64":
        pass

    # Plotting
    gray_colormap = colormap_function("gray", [0, 0, 0], [1, 1, 1])
    fig = plt.figure()

    # Y DCT
    fig.add_subplot(1, 3, 1)
    plt.title("Y DCT")
    plt.imshow(Y_dct_log, cmap=gray_colormap)
    plt.colorbar(shrink=0.5)

    # Cb DCT
    fig.add_subplot(1, 3, 2)
    plt.title("Cb DCT")
    plt.imshow(Cb_dct_log, cmap=gray_colormap)
    plt.colorbar(shrink=0.5)

    # Cr DCT
    fig.add_subplot(1, 3, 3)
    plt.title("Cr DCT")
    plt.imshow(Cr_dct_log, cmap=gray_colormap)
    plt.colorbar(shrink=0.5)

    return Y_dct, Cb_dct, Cr_dct


def dct_inverse(Y_dct, Cb_dct, Cr_dct, blocks):

    if blocks == "all":
        Y_d = fft.idct(fft.idct(Y_dct, norm="ortho").T, norm="ortho").T
        Cb_d = fft.idct(fft.idct(Cb_dct, norm="ortho").T, norm="ortho").T
        Cr_d = fft.idct(fft.idct(Cr_dct, norm="ortho").T, norm="ortho").T

    # 7.2 - fazer mais tarde
    elif blocks == "8":
        pass

    # 7.3 - fazer mais tarde
    elif blocks == "64":
        pass

    # Plotting
    gray_colormap = colormap_function("gray", [0, 0, 0], [1, 1, 1])
    fig = plt.figure()

    # Y inverse DCT
    fig.add_subplot(1, 3, 1)
    plt.title("Y inverse_dct")
    plt.imshow(Y_d, cmap=gray_colormap)

    # Cb inverse DCT
    fig.add_subplot(1, 3, 2)
    plt.title("Cb inverse_dct")
    plt.imshow(Cb_d, cmap=gray_colormap)

    # Cr inverse DCT
    fig.add_subplot(1, 3, 3)
    plt.title("Cr inverse_dct")
    plt.imshow(Cr_d, cmap=gray_colormap)

    return Y_d, Cb_d, Cr_d


# -------------------------------------------------------------------------------------------- #
def encoder(img, lines, columns):
    # -- 4 --
    img_padded = padding_function(img, lines, columns)
    R_p, G_p, B_p = rgb_components(img_padded)
    show_rgb(R_p, G_p, B_p)

    # -- 5 --
    Y, Cb, Cr = rgb_to_ycbcr(R_p, G_p, B_p)
    show_ycbcr(Y, Cb, Cr)

    # -- 6 --
    Y_d, Cb_d, Cr_d = downsampling(Y, Cb, Cr, 4, 2, 2)
    Y_d0, Cb_d0, Cr_d0 = downsampling(Y, Cb, Cr, 4, 2, 0)

    # Plotting
    fig = plt.figure()

    # Cb original
    fig.add_subplot(3, 2, 1)
    plt.title("Cb - Original")
    plt.imshow(Cb)

    # Cr original
    fig.add_subplot(3, 2, 2)
    plt.title("Cr - Original")
    plt.imshow(Cr)

    # Cb downsampled 4:2:2
    fig.add_subplot(3, 2, 3)
    plt.title("Cb - Downsampling 4:2:2")
    plt.imshow(Cb_d)

    # Cr downsampled 4:2:2
    fig.add_subplot(3, 2, 4)
    plt.title("Cr - Downsampling 4:2:2")
    plt.imshow(Cr_d)

    # Cb downsampled 4:2:0
    fig.add_subplot(3, 2, 5)
    plt.title("Cb - Downsampling 4:2:0")
    plt.imshow(Cb_d0)

    # Cr downsampled 4:2:0
    fig.add_subplot(3, 2, 6)
    plt.title("Cr - Downsampling 4:2:0")
    plt.imshow(Cr_d0)
    
    plt.subplots_adjust(hspace=0.5)
    
    # -- 7.1 --
    Y_dct, Cb_dct, Cr_dct = dct(Y_d0, Cb_d0, Cr_d0, "all")

    return Y_dct, Cb_dct, Cr_dct


def decoder(Y_dct, Cb_dct, Cr_dct, n_lines, n_columns):
    # -- 7.1 --
    Y_d0, Cb_d0, Cr_d0 = dct_inverse(Y_dct, Cb_dct, Cr_dct, "all")

    # -- 6 --
    # Downsampling 4:2:2
    # Y, Cb, Cr = upsampling(Y_d, Cr_d, Cb_d, 1)

    # Downsampling 4:2:0
    Y, Cb, Cr = upsampling(Y_d0, Cb_d0, Cr_d0, 0)

    # -- 5 --
    # YCbCr to RGB
    R, G, B = ycbcr_to_rgb(Y, Cb, Cr)

    # Joins all channels in one matrix
    matrix_joined_rgb = join_RGB(R, G, B)

    # -- 3 --
    draw_plot("RGB channels joined with padding", matrix_joined_rgb)

    # -- 4 --
    # Remove image padding
    img_without_padding = without_padding_function(
        matrix_joined_rgb, n_lines, n_columns)
    draw_plot("Final Image", img_without_padding)

    print(f"Final shape: {img_without_padding.shape}")
# -------------------------------------------------------------------------------------------- #


def main():

    plt.close('all')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    img_name = input("Image name: ")
    img_path = dir_path + "/imagens/" + img_name + ".bmp"
    img = read_image(img_path)

    #draw_plot("Original Image", img)

    print(f"Initial shape: {img.shape}")
    (lines, columns, channels) = img.shape

    # retornar sempre o mais recente !!!
    Y_dct, Cb_dct, Cr_dct = encoder(img, lines, columns)
    decoder(Y_dct, Cb_dct, Cr_dct, lines, columns)


if __name__ == "__main__":
    main()
    plt.show()
