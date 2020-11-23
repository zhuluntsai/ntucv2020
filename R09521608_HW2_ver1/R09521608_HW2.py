#hw2 
#R09521608 土木系電輔組 蔡瑋倫

# Write a program to generate:
# (a) a binary image (threshold at 128)
# (b) a histogram
# (c) connected components(regions with + at centroid, bounding box)

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

filename = 'lena.bmp'

img = Image.open(filename)
width, height = img.size

def binarize(img, threshold):
    new_image = Image.new('L', img.size)
    threshold = 128
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            new_image.putpixel((x, y), (img.getpixel((x, y)) > threshold) * 255)
    return new_image

def histogram(img):
    pixel = []
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            pixel.append(img.getpixel((x, y)))
    plt.hist(pixel, 256)
    plt.show()

def connected_components(img):

    image_array = np.zeros((width, height))
    for y in range(0, height, 1):
        for x in range(0, width, 1):
            print(x, y)
            if (img.getpixel((x, y)) > 0):
                image_array[x][y] = 1

    while 1:
        break
        forward = False
        for y in range(1, height + 1, 1):
            for x in range(1, width + 1, 1):
                if image_array[x][y] == 1:
                    temp = [image_array[x][y]]
                    if image_array[x-1][y] == 1:
                        temp.append(image_array[x-1][y])
                    if image_array[x+1][y] == 1:
                        temp.append(image_array[x+1][y])
                    if image_array[x][y-1] == 1:
                        temp.append(image_array[x][y-1])
                    if image_array[x][y+1] == 1:
                        temp.append(image_array[x][y+1])

                    if len(temp) != 0:
                        temp_min = min(temp)
                        if temp_min != image_array[x][y]:
                            forward = True
                            image_array[x][y] = temp_min

        for y in range(height,1 , -1):
            for x in range(width, 1, -1):
                if image_array[x][y] == 1:
                    temp = [image_array[x][y]]
                    if image_array[x-1][y] == 1:
                        temp.append(image_array[x-1][y])
                    if image_array[x+1][y] == 1:
                        temp.append(image_array[x+1][y])
                    if image_array[x][y-1] == 1:
                        temp.append(image_array[x][y-1])
                    if image_array[x][y+1] == 1:
                        temp.append(image_array[x][y+1])

                    if len(temp) != 0:
                        temp_min = min(temp)
                        if temp_min != image_array[x][y]:
                            forward = True
                            image_array[x][y] = temp_min

binarize(img, 128).save(f'binarize_{filename}')
histogram(img)
connected_components(Image.open(f'binarize_{filename}'))