#hw9
#R09521608 土木系電輔組 蔡瑋倫

# You are to implement following edge detectors with thresholds :
# (a) Robert's Operator: 12
# (b) Prewitt's Edge Detector: 24
# (c) Sobel's Edge Detector: 38
# (d) Frei and Chen's Gradient Operator: 30
# (e) Kirsch's Compass Operator: 135
# (f) Robinson's Compass Operator: 43
# (g) Nevatia-Babu 5x5 Operator: 12500

from PIL import Image
import numpy as np
import math

filename = 'lena.bmp'

img = Image.open(filename)
width, height = img.size

def padding(img, padding_pixel, ):
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

def default_operator(img, thresholds, kernel1, kernel2):
    new_image = Image.new('1', img.size)
    padding_pixel = round(kernel1.shape[0]/2)
    img = padding(img, padding_pixel)

    for x in range(padding_pixel, width + padding_pixel, 1):
        for y in range(padding_pixel, height + padding_pixel, 1):

            kernel_list = []
            for j in range(kernel1.shape[0]):
                kernel_list_row = []
                for i in range(kernel1.shape[0]):
                    kernel_list_row.append(img.getpixel((x+i, y+j)))
                kernel_list.append(kernel_list_row)

            gradient_magnitude = int(math.sqrt(np.multiply(kernel_list, kernel1).sum()**2 + np.multiply(kernel_list, kernel2).sum()**2))
            if gradient_magnitude >= thresholds:
                new_image.putpixel((x-padding_pixel, y-padding_pixel), 0)
            elif gradient_magnitude < thresholds:
                new_image.putpixel((x-padding_pixel, y-padding_pixel), 1)
    return new_image

def default_compass_operator(img, thresholds, k_list, padding_pixel):
    new_image = Image.new('1', img.size)
    img = padding(img, padding_pixel)

    for x in range(padding_pixel, width + padding_pixel, 1):
        for y in range(padding_pixel, height + padding_pixel, 1):

            kernel_list = []
            for j in range(len(k_list[0])):
                kernel_list_row = []
                for i in range(len(k_list[0])):
                    kernel_list_row.append(img.getpixel((x+i-padding_pixel, y+j-padding_pixel)))
                kernel_list.append(kernel_list_row)

            gradient_magnitude_list = []
            for k in k_list:
                gradient_magnitude_list.append(np.multiply(kernel_list, k).sum())
            gradient_magnitude = max(gradient_magnitude_list)

            if gradient_magnitude >= thresholds:
                new_image.putpixel((x-padding_pixel, y-padding_pixel), 0)
            elif gradient_magnitude < thresholds:
                new_image.putpixel((x-padding_pixel, y-padding_pixel), 1)
    return new_image

def roberts_operator(img, thresholds):
    r1 = np.array([[-1, 0], [0, 1]])
    r2 = np.array([[0, -1], [1, 0]])
    return default_operator(img, thresholds, r1, r2)

def prewitts_edge_detector(img, thresholds):
    p1 = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    p2 = np.array([[-1, 0, 1]]*3)
    return default_operator(img, thresholds, p1, p2)

def sobels_edge_detector(img, thresholds):
    s1 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    s2 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    return default_operator(img, thresholds, s1, s2)

def frei_and_chens_gradient_operator(img, thresholds):
    f1 = np.array([[-1, -math.sqrt(2), -1], [0, 0, 0], [1, math.sqrt(2), 1]])
    f2 = np.array([[-1, 0, 1], [-math.sqrt(2), 0, math.sqrt(2)], [-1, 0, 1]])
    return default_operator(img, thresholds, f1, f2)

def kirschs_compass_operator(img, thresholds):
    k = [-3, -3, 5, 5, 5, -3, -3, -3]*2
    k_list = []
    for i in range(8):
        k_list.append([
            [k[i], k[i+1], k[i+2]],
            [k[i+7], 0, k[i+3]],
            [k[i+6], k[i+5], k[i+4]] ])
    return default_compass_operator(img, thresholds, k_list, 1)

def robinsons_compass_operator(img, thresholds):
    k = [-1, 0, 1, 2, 1, 0, -1, -2]*2
    k_list = []
    for i in range(8):
        k_list.append([
            [k[i], k[i+1], k[i+2]],
            [k[i+7], 0, k[i+3]],
            [k[i+6], k[i+5], k[i+4]] ])
    return default_compass_operator(img, thresholds, k_list, 1)

def nevatia_babu_5x5_operator(img, thresholds):
    k_list = []
    # 0
    k_list.append([
        [100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100],
        [0, 0, 0, 0, 0],
        [-100, -100, -100, -100, -100],
        [-100, -100, -100, -100, -100] ])
    # 30
    k_list.append([
        [100, 100, 100, 100, 100],
        [100, 100, 100, 78, -32],
        [100, 92, 0, -92, -100],
        [32, -78, -100, -100, -100],
        [-100, -100, -100, -100, -100] ])
    # 60
    k_list.append(np.array(k_list[1]).transpose().tolist())
    # -90
    k_list.append([[-100, -100, 0, 100, 100]]*5)
    # -30
    k_list.append(np.negative(np.flipud(np.array(k_list[1]))).tolist())
    # -60
    k_list.append(np.negative(np.flipud(np.array(k_list[2]))).tolist())
    return default_compass_operator(img, thresholds, k_list, 2)

roberts_operator(img, 18).save(f'roberts_operator_{filename}')
prewitts_edge_detector(img, 60).save(f'prewitts_edge_detector_{filename}')
sobels_edge_detector(img, 75).save(f'sobels_edge_detector_{filename}')
frei_and_chens_gradient_operator(img, 60).save(f'frei_and_chens_gradient_operator{filename}')
kirschs_compass_operator(img, 240).save(f'kirschs_compass_operator_{filename}')
robinsons_compass_operator(img, 75).save(f'robinsons_compass_operator_{filename}')
nevatia_babu_5x5_operator(img, 13000).save(f'nevatia_babu_5x5_operator_{filename}')