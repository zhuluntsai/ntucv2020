#hw6
#R09521608 土木系電輔組 蔡瑋倫

# Write a program which counts the Yokoi connectivity number on a downsampled image(lena.bmp).

from PIL import Image

import numpy as np

filename = 'lena.bmp'

img = Image.open(filename)
width, height = img.size

def binarize(img, threshold):
    new_image = Image.new('L', img.size)
    for x in range(0, width, 1):
        for y in range(0, height, 1):
            new_image.putpixel((x, y), (img.getpixel((x, y)) >= threshold) * 255)
    return new_image

def down_sample(img, pixel):
    ratio = pixel / width
    new_image = Image.new('1', (pixel, pixel))
    for x in range(0, pixel, 1):
        for y in range(0, pixel, 1):
            new_image.putpixel((x, y), img.getpixel((x / ratio, y / ratio)))
    return new_image

def f(a1, a2, a3, a4):
    f = 0
    f = [a1, a2, a3, a4].count('q')
    if [a1, a2, a3, a4].count('r') == 4:
        f = 5
    if f == 0:
        f = ' '
    return f

def h(b, c, d, e):
    if b == c and (b != d or b != e):
        return 'q'
    if b == c and (b == d and b == e):
        return 'r'
    if b != c:
        return 's'

def padding(img):
    width, height = img.size
    new_image = Image.new('1', (width+2, height+2))
    for x in range(0, width, 1):
        for y in range(0, height, 1):
            new_image.putpixel((x+1, y+1), img.getpixel((x, y)))
    return new_image

def yokoi_connectivity_number(img):
    width, height = img.size
    img = padding(img)
    yokoi_txt = open('yokoi.txt', 'w')

    i = [1, 0, -1, 0]*2
    j = [1, 1, -1, -1]*2

    for y in range(1, height+1, 1):

        line = ''
        for x in range(1, width+1, 1):
            
            if img.getpixel((x, y)) == 0:
                line += ' '
            else:
                f_list = [None]*4
                for k in range(0, 4, 1):

                    b = (x, y)
                    c = (x+i[k], y+i[k+1])
                    d = (x+j[k+1], y+j[k+2])
                    e = (x+i[k+1], y+i[k+2])

                    f_list[k] = h(img.getpixel(b), img.getpixel(c), img.getpixel(d), img.getpixel(e))
                
                line += str(f(f_list[0], f_list[1], f_list[2], f_list[3]))
        
        yokoi_txt.writelines(line + '\n') 
    
    yokoi_txt.close()

binarize_img = binarize(img, 128)
down_sampled_img = down_sample(binarize_img, 64)
yokoi_connectivity_number(down_sampled_img)