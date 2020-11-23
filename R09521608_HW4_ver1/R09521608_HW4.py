#hw4
#R09521608 土木系電輔組 蔡瑋倫

# Write programs which do binary morphology on a binary image:
# (a) Dilation
# (b) Erosion
# (c) Opening
# (d) Closing
# (e) Hit-and-miss transform

from PIL import Image
import numpy as np

filename = 'lena.bmp'

img = Image.open(filename)
width, height = img.size

kernel = np.array([
    [0, 1, 1, 1, 0],                 
    [1, 1, 1, 1, 1], 
    [1, 1, 1, 1, 1], 
    [1, 1, 1, 1, 1], 
    [0, 1, 1, 1, 0]])
kernel_center = [int(kernel.shape[0]/2), int(kernel.shape[1]/2)]

kernel_j = np.array([
    [1, 0], 
    [1, 1]])
kernel_center_j = (1, 0)

kernel_k = np.array([
    [1, 0], 
    [1, 1]])
kernel_center_k = (0, 1)

def binarize(img, threshold):
    new_image = Image.new('L', img.size)
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            new_image.putpixel((x, y), (img.getpixel((x, y)) > threshold) * 255)
    return new_image

def reverse(img):
    new_image = Image.new('L', img.size)
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            pixel = img.getpixel((x, y))
            if pixel == 0:
                pixel = 255
            elif pixel == 255:
                pixel = 0
            new_image.putpixel((x, y), pixel)
    return new_image

def dilation(img, kernel, kernel_center):
    new_image = Image.new('1', img.size)
    for x in range(1 + kernel_center[0], width - kernel_center[0], 1):
        for y in range(1 + kernel_center[0], height - kernel_center[0], 1):
            pixel = img.getpixel((x, y))

            if pixel != 0:
                for i in range(0, kernel.shape[0], 1):
                    for j in range(0, kernel.shape[1], 1):

                        if kernel[i, j] == 1:
                            put_pixel_x = x + i - kernel_center[0]
                            put_pixel_y = y + j - kernel_center[1]
                            new_image.putpixel((put_pixel_x, put_pixel_y), 1)
    return new_image

def erosion(img, kernel, kernel_center):
    new_image = Image.new('1', img.size)
    for x in range(1 + kernel_center[0], width - kernel_center[0], 1):
        for y in range(1 + kernel_center[0], height - kernel_center[0], 1):
            
            kernel_list = []
            for i in range(0, kernel.shape[0], 1):
                for j in range(0, kernel.shape[1], 1):
                    if kernel[i, j] == 1:
                        put_pixel_x = x + i - kernel_center[0]
                        put_pixel_y = y + j - kernel_center[1]
                        try:
                            kernel_list.append(img.getpixel((put_pixel_x, put_pixel_y)))
                        except:
                            pass

            if all(kernel_list):
                new_image.putpixel((x, y), 1)
                
    return new_image

def opening(img, kernel, kernel_center):
    new_image = dilation(erosion(img, kernel, kernel_center), kernel, kernel_center)
    return new_image

def closing(img, kernel, kernel_center):
    new_image = erosion(dilation(img, kernel, kernel_center), kernel, kernel_center)
    return new_image

def hit_and_miss(img, kernel_j, kernel_center_j, kernel_k, kernel_center_k):

    A = erosion(img, kernel_j, kernel_center_j)
    A_c = erosion(reverse(img), kernel_k, kernel_center_k)

    new_image = Image.new('1', img.size)
    for x in range(1 , width, 1):
        for y in range(1 , height, 1):

            if A.getpixel((x, y)) == 1 and A_c.getpixel((x, y)) == 1:
                new_image.putpixel((x, y), 1)
            else:
                new_image.putpixel((x, y), 0)
                
    return new_image
    
binarize_img = binarize(img, 128)
dilation(binarize_img, kernel, kernel_center).save(f'dilation_{filename}')
erosion(binarize_img, kernel, kernel_center).save(f'erosion_{filename}')
opening(binarize_img, kernel, kernel_center).save(f'opening_{filename}')
closing(binarize_img, kernel, kernel_center).save(f'closing_{filename}')
hit_and_miss(binarize_img, kernel_j, kernel_center_j, kernel_k, kernel_center_k).save(f'hit_and_miss_{filename}')