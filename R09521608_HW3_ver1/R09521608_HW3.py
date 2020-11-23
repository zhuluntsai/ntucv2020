#hw3
#R09521608 土木系電輔組 蔡瑋倫

# Write a program to generate:
# (a) original image and its histogram
# (b) image with intensity divided by 3 and its histogram
# (c) image after applying histogram equalization to (b) and its histogram

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

filename = 'lena.bmp'

img = Image.open(filename)
width, height = img.size

def histogram(img, filename):
    pixel = []
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            pixel.append(img.getpixel((x, y)))
    plt.figure()
    plt.hist(pixel, 256)
    plt.xlim(right=256)
    plt.savefig(filename)

def divide_three(img):
    new_image = Image.new('L', img.size)
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            new_image.putpixel((x, y), round(img.getpixel((x, y))/3))
    histogram(new_image, 'divide_three_histogram.png')
    return new_image

def equalize(img):
    new_image = Image.new('L', img.size)

    pixel = np.zeros(256)
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            pixel[img.getpixel((x, y))] += 1

    equalized_pixel = np.round(np.cumsum(pixel) / np.cumsum(pixel)[-1] * 255)
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            new_image.putpixel((x, y), int(equalized_pixel[img.getpixel((x, y))]))
    histogram(new_image, 'equalize_histogram.png')
    return new_image

histogram(img, 'histogram.png')
divide_three(img).save(f'divide_three_{filename}')
equalize(img).save(f'equalize_{filename}')