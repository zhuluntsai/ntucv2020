#hw10
#R09521608 土木系電輔組 蔡瑋倫

# Implement 2 Laplacian Mask, Minimum Variance Laplacian, Laplacian of Gaussian, and Difference of Gaussian(inhibitory sigma=3, excitatory sigma=1, kernel size 11x11).
# Please list the kernels and the thresholds(for zero crossing) you used.
# Threshold Values listed below are for reference:
# Laplace Mask1 (0, 1, 0, 1, -4, 1, 0, 1, 0): 15
# Laplace Mask2 (1, 1, 1, 1, -8, 1, 1, 1, 1)
# Minimum variance Laplacian: 20
# Laplace of Gaussian: 3000
# Difference of Gaussian: 1

from PIL import Image
import numpy as np
import math

filename = 'lena.bmp'

img = Image.open(filename)
width, height = img.size

def padding(img, padding_pixel):
    width, height = img.size
    new_image = Image.new('L', (width+padding_pixel*2, height+padding_pixel*2))
    for x in range(0, width, 1):
        for y in range(0, height, 1):
            new_image.putpixel((x+padding_pixel, y+padding_pixel), img.getpixel((x, y)))

    # padding edge
    for y in range(padding_pixel):
        for x in range(width):
            new_image.putpixel((x+padding_pixel, y), img.getpixel((x, 0)))
            new_image.putpixel((x+padding_pixel, y+height+padding_pixel), img.getpixel((x, height-1)))
    for x in range(padding_pixel):
        for y in range(height + padding_pixel):
            new_image.putpixel((x, y), new_image.getpixel((padding_pixel, y)))
            new_image.putpixel((x+width+padding_pixel, y), new_image.getpixel((width+padding_pixel-1, y)))
 
    return new_image

def default_operator(img, thresholds, kernel):
    new_image_array = np.zeros(img.size)
    padding_pixel = round(kernel.shape[0]/2)
    img = padding(img, padding_pixel)
    for x in range(padding_pixel, width + padding_pixel, 1):
        for y in range(padding_pixel, height + padding_pixel, 1):

            kernel_list = []
            for j in range(kernel.shape[0]):
                kernel_list_row = []
                for i in range(kernel.shape[0]):
                    kernel_list_row.append(img.getpixel((x+i-padding_pixel, y+j-padding_pixel)))
                kernel_list.append(kernel_list_row)

            gradient_magnitude = np.multiply(kernel_list, kernel).sum()
            if gradient_magnitude >= thresholds:
                new_image_array[x-padding_pixel, y-padding_pixel] = 1
            elif gradient_magnitude <= thresholds:
                new_image_array[x-padding_pixel, y-padding_pixel] = -1
            elif -thresholds < gradient_magnitude < thresholds:
                new_image_array[x-padding_pixel, y-padding_pixel] = 0
    return new_image_array

def laplace_mask1(img, thresholds):
    l = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    return default_operator(img, thresholds, l), l

def laplace_mask2(img, thresholds):
    l = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])/3
    return default_operator(img, thresholds, l), l

def minimum_variance_laplacian(img, thresholds):
    l = np.array([[2, -1, 2], [-1, -4, -1], [2, -1, 2]])/3
    return default_operator(img, thresholds, l), l

def laplace_of_gaussian(img, thresholds):
    k = np.array([[0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0],
				[0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
				[0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
				[-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
				[-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
				[-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],
				[-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
				[-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
				[0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
				[0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
				[0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]])
    return default_operator(img, thresholds, k), k

def difference_of_gaussian(img, thresholds):
    k = np.array([[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
				[-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
				[-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
				[-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
				[-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
				[-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],
				[-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
				[-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
				[-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
				[-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
				[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1]])
    return default_operator(img, thresholds, k), k

def zero_cross_edge_detector(new_image_array, kernel):
    new_image = Image.new('1', img.size)
    padding_pixel = round(kernel.shape[0]/2)
    for x in range(0, width, 1):
        for y in range(0, height, 1):

            kernel_list = []
            for j in range(kernel.shape[0]):
                kernel_list_row = []
                for i in range(kernel.shape[0]):
                    try:
                        kernel_list_row.append(new_image_array[x+i-padding_pixel, y+j-padding_pixel])
                    except:
                        pass
                kernel_list.append(kernel_list_row)

            if (new_image_array[x, y] == 1) and any(-1 in sublist for sublist in kernel_list):
                new_image.putpixel((x, y), 0)
            else:
                new_image.putpixel((x, y), 1)
            
    return new_image

new_image_array, kernel = laplace_mask1(img, 25)
zero_cross_edge_detector(new_image_array, kernel).save(f'laplace_mask1_{filename}')

new_image_array, kernel = laplace_mask2(img, 18)
zero_cross_edge_detector(new_image_array, kernel).save(f'laplace_mask2_{filename}')

new_image_array, kernel = minimum_variance_laplacian(img, 18)
zero_cross_edge_detector(new_image_array, kernel).save(f'minimum_variance_laplacian_{filename}')

new_image_array, kernel = laplace_of_gaussian(img, 3600)
zero_cross_edge_detector(new_image_array, kernel).save(f'laplace_of_gaussian_{filename}')

new_image_array, kernel = difference_of_gaussian(img, 1)
zero_cross_edge_detector(new_image_array, kernel).save(f'difference_of_gaussian_{filename}')