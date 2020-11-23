#hw5
#R09521608 土木系電輔組 蔡瑋倫

# Write programs which do gray-scale morphology on a gray-scale image(lena.bmp):
# (a) Dilation
# (b) Erosion
# (c) Opening
# (d) Closing

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

def binarize(img, threshold):
    new_image = Image.new('L', img.size)
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            new_image.putpixel((x, y), (img.getpixel((x, y)) > threshold) * 255)
    return new_image

def dilation(img, kernel, kernel_center):
    new_image = Image.new('L', img.size)
    for x in range(0, width, 1):
        for y in range(0, height, 1):
            pixel = img.getpixel((x, y))

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
            
            new_image.putpixel((x, y), max(kernel_list))
    
    return new_image

def erosion(img, kernel, kernel_center):
    new_image = Image.new('L', img.size)
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            
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

            new_image.putpixel((x, y), min(kernel_list))                
    
    return new_image

def opening(img, kernel, kernel_center):
    new_image = dilation(erosion(img, kernel, kernel_center), kernel, kernel_center)
    return new_image

def closing(img, kernel, kernel_center):
    new_image = erosion(dilation(img, kernel, kernel_center), kernel, kernel_center)
    return new_image
    
dilation(img, kernel, kernel_center).save(f'dilation_{filename}')
erosion(img, kernel, kernel_center).save(f'erosion_{filename}')
opening(img, kernel, kernel_center).save(f'opening_{filename}')
closing(img, kernel, kernel_center).save(f'closing_{filename}')
