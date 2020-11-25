#hw7
#R09521608 土木系電輔組 蔡瑋倫

# Write a program which does thinning on a downsampled image (lena.bmp).

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

def padding_img(img):
    width, height = img.size
    new_image = Image.new('1', (width+2, height+2))
    for x in range(0, width, 1):
        for y in range(0, height, 1):
            new_image.putpixel((x+1, y+1), img.getpixel((x, y)))
    return new_image

def padding_txt(txt):
    new_txt = []
    for y in range(0, len(txt), 1):
        new_txt.append(' ' + txt[y][:-1] + ' ')
    new_txt.insert(0, ' '*(len(txt[0])+1))
    new_txt.append(' '*(len(txt[0])+1))
    return new_txt

def yokoi_connectivity_number(img):
    width, height = img.size
    img = padding_img(img)
    yokoi_txt = []

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
        
        yokoi_txt.append(line + '\n') 

    return yokoi_txt

def pair_relationship_operator(img, yokoi_txt):

    yokoi_txt = padding_txt(yokoi_txt)
    pair_txt = []
    i = [1, 0, -1, 0]*2
    for y in range(1, len(yokoi_txt)-1, 1):
        line = ''
        for x in range(1, len(yokoi_txt[0])-1, 1):

            if yokoi_txt[y][x] == '1':
                f_list = []
                for k in range(0, 4, 1):
                    if yokoi_txt[y+i[k+1]][x+i[k]] == yokoi_txt[y][x]:
                        h = 1
                    else:
                        h = 0
                    f_list.append(h)
                if sum(f_list) >= 1:
                    line += 'p'
                else:
                    line += 'q'
            elif yokoi_txt[y][x] != '1' and yokoi_txt[y][x] != ' ':
                line += 'q'
            else:
                line += ' '

        pair_txt.append(line) 

    return pair_txt

def thinning(img):

    yokoi_txt = yokoi_connectivity_number(img)
    marked_image = pair_relationship_operator(img, yokoi_txt)

    for y in range(0, img.size[1], 1):
        for x in range(0, img.size[0], 1):

            if yokoi_txt[y][x] == '1' and marked_image[y][x] == 'p':
                img.putpixel((x, y), 0)
                yokoi_txt = yokoi_connectivity_number(img)

    return img

def thinning_operator(img):

    thinning_img = thinning(img)
    same_image = False
    i = 0

    while not same_image:
        i += 1
        new_thinning_img = thinning(thinning_img.copy())

        same_image = compare_images(thinning_img, new_thinning_img)
        thinning_img = new_thinning_img
        thinning_img.save(f'thinning_iter{i}_{filename}')

    return new_thinning_img

def compare_images(image1, image2):
    for x in range(image1.size[0]):
        for y in range(image1.size[1]):
            if image1.getpixel((x, y)) != image2.getpixel((x, y)):
                return False
    return True

binarize_img = binarize(img, 128)
down_sampled_img = down_sample(binarize_img, 64)
down_sampled_img.save(f'thinning_iter0_{filename}')
thinning_operator(down_sampled_img).save(f'thinning_final_{filename}')