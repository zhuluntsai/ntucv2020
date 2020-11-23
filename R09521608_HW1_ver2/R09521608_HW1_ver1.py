#hw1 
#R09521608 土木系電輔組 蔡瑋倫

# Part1. Write a program to do the following requirement.
# (a) upside-down lena.bmp
# (b) right-side-left lena.bmp
# (c) diagonally flip lena.bmp

# Part2. Write a program or use software to do the following requirement.
# (d) rotate lena.bmp 45 degrees clockwise
# (e) shrink lena.bmp in half
# (f) binarize lena.bmp at 128 to get a binary image

from PIL import Image

filename = 'lena.bmp'

img = Image.open(filename)
width, height = img.size

#region Part1.

def upside_down(img):
    new_image = Image.new('L', img.size)
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            new_image.putpixel((x, height - y), img.getpixel((x, y)))
    return new_image

def right_side_left(img):
    new_image = Image.new('L', img.size)
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            new_image.putpixel((width - x, y), img.getpixel((x, y)))
    return new_image

def diagonally_flip(img):
    new_image = Image.new('L', img.size)
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            new_image.putpixel((width - x, height - y), img.getpixel((x, y)))
    return new_image

upside_down(img).save(f'a_upside_down_{filename}')
right_side_left(img).save(f'b_right_side_left_{filename}')
diagonally_flip(img).save(f'c_diagonally_flip_{filename}')

#endregion

#region Part2.

def rotate_45_degrees_clockwise(img):
    new_image = img.rotate(45, expand=1)
    return new_image

def shrink_half(img):
    new_image = Image.new('L', (int(width / 2), int(height / 2)))
    for x in range(1, int(width / 2), 1):
        for y in range(1, int(height / 2), 1):
            new_image.putpixel((x, y), img.getpixel((x * 2, y * 2)))
    return new_image

def binarize(img, threshold):
    new_image = Image.new('L', img.size)
    threshold = 128
    for x in range(1, width, 1):
        for y in range(1, height, 1):
            new_image.putpixel((x, y), (img.getpixel((x, y)) > threshold) * 255)
    return new_image

rotate_45_degrees_clockwise(img).save(f'rotate_45_degrees_clockwise_{filename}')
shrink_half(img).save(f'shrink_half_{filename}')
binarize(img, 128).save(f'binarize_{filename}')

#endregion